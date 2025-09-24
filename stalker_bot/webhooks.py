from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler
import threading

# Глобальные переменные
bot = None
dispatcher = None

def setup_bot():
    global bot, dispatcher
    if bot is None:
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not token:
            print("❌ TELEGRAM_BOT_TOKEN not set!")
            return False
            
        print("✅ Initializing bot...")
        bot = Bot(token=token)
        dispatcher = Dispatcher(bot, None, workers=0)
        
        # Добавляем обработчики
        from bot.handlers import start
        dispatcher.add_handler(CommandHandler("start", start))
        
        print("✅ Bot setup completed")
        return True
    return True

@csrf_exempt
def webhook(request):
    if request.method == 'POST':
        try:
            if not setup_bot():
                return JsonResponse({'status': 'error', 'message': 'Bot not configured'})
            
            # Парсим обновление
            body = request.body.decode('utf-8')
            data = json.loads(body)
            update = Update.de_json(data, bot)
            
            print("📨 Processing update...")
            
            # Обрабатываем обновление в отдельном потоке
            def process_update():
                try:
                    dispatcher.process_update(update)
                    print("✅ Update processed successfully")
                except Exception as e:
                    print(f"❌ Error processing update: {e}")
            
            thread = threading.Thread(target=process_update)
            thread.start()
            
            return JsonResponse({'status': 'ok'})
            
        except Exception as e:
            print(f"❌ Error in webhook: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)
