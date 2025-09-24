from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler

# Кэш для приложения
_bot_app = None

def get_bot_application():
    global _bot_app
    if _bot_app is None:
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not token:
            raise ValueError("TELEGRAM_BOT_TOKEN not set")
        
        _bot_app = Application.builder().token(token).build()
        
        # Добавляем обработчики
        from bot.handlers import start
        _bot_app.add_handler(CommandHandler("start", start))
        
    return _bot_app

@csrf_exempt
def webhook(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("📨 Received Telegram update")
            
            app = get_bot_application()
            update = Update.de_json(data, app.bot)
            
            # Простой синхронный обработчик
            async def handle_update():
                await app.initialize()
                await app.process_update(update)
            
            # Запускаем обработку
            asyncio.run(handle_update())
            
            print("✅ Update processed")
            return JsonResponse({'status': 'ok'})
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)
