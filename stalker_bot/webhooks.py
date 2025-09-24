from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler

# Глобальное приложение
app = None

def init_bot():
    global app
    if app is None:
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        app = Application.builder().token(token).build()
        
        from bot.handlers import start
        app.add_handler(CommandHandler("start", start))
        
        # Запускаем приложение
        app.initialize()
        print("✅ Bot initialized")

@csrf_exempt
def webhook(request):
    if request.method == 'POST':
        try:
            if app is None:
                init_bot()
            
            data = json.loads(request.body)
            update = Update.de_json(data, app.bot)
            
            # Используем update_queue для обработки
            app.update_queue.put_nowait(update)
            
            print("✅ Update queued successfully")
            return JsonResponse({'status': 'ok'})
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)
