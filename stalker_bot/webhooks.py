from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler

# Глобальное приложение
_app = None

async def create_app():
    """Создает и настраивает приложение"""
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN not set")
    
    # Создаем приложение
    application = Application.builder().token(token).build()
    
    # Импортируем и добавляем обработчики
    from bot.handlers import start
    application.add_handler(CommandHandler("start", start))
    
    # Инициализируем
    await application.initialize()
    await application.start()
    
    return application

def get_app():
    """Получает или создает приложение"""
    global _app
    if _app is None:
        # Создаем приложение синхронно
        _app = asyncio.run(create_app())
    return _app

@csrf_exempt
def webhook(request):
    if request.method == 'POST':
        try:
            # Получаем приложение
            app = get_app()
            
            # Парсим обновление
            data = json.loads(request.body)
            update = Update.de_json(data, app.bot)
            
            print("📨 Processing update...")
            
            # Обрабатываем обновление асинхронно
            async def process():
                await app.process_update(update)
            
            # Запускаем в существующем event loop или создаем новый
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            if loop.is_running():
                asyncio.create_task(process())
            else:
                loop.run_until_complete(process())
            
            print("✅ Update queued")
            return JsonResponse({'status': 'ok'})
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)
