from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Импортируем наши обработчики
from bot.handlers import start

# Глобальная переменная для приложения
application = None

def setup_bot():
    global application
    if application is None:
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not token:
            print("❌ TELEGRAM_BOT_TOKEN not set!")
            return None
            
        print("✅ Initializing bot application...")
        application = Application.builder().token(token).build()
        
        # Добавляем обработчик команды /start
        application.add_handler(CommandHandler("start", start))
        
        print("✅ Bot setup completed")
    
    return application

@csrf_exempt
def webhook(request):
    if request.method == 'POST':
        try:
            # Парсим входящее обновление от Telegram
            data = json.loads(request.body)
            print("📨 Received Telegram update")
            
            # Настраиваем бота если еще не настроен
            app = setup_bot()
            if app is None:
                return JsonResponse({'status': 'error', 'message': 'Bot not configured'})
            
            # Создаем объект Update
            update = Update.de_json(data, app.bot)
            
            # Обрабатываем обновление через run_until_complete
            async def process_update():
                async with app:
                    await app.process_update(update)
            
            # Запускаем асинхронную обработку
            if app.running:
                asyncio.create_task(process_update())
            else:
                asyncio.run(process_update())
            
            print("✅ Update processed successfully")
            return JsonResponse({'status': 'ok'})
            
        except Exception as e:
            print("❌ Error in webhook:", str(e))
            import traceback
            print("Full traceback:", traceback.format_exc())
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)
