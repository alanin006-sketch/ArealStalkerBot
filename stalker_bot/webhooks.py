from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
import os
import json
import asyncio

# Импортируем наши обработчики
from bot.handlers import start, explore_city, go_to_bar, order_beer, ask_about_zone, show_status, show_inventory, cancel
from bot.states import ARRIVAL, BAR_CHOICE
from bot.keyboards import get_main_keyboard

# Глобальная переменная для приложения
application = None

def setup_bot():
    global application
    if application is None:
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not token:
            print("❌ TELEGRAM_BOT_TOKEN not set!")
            return None
            
        application = Application.builder().token(token).build()
        
        # Создаем обработчик диалога
        from bot.states import ARRIVAL, BAR_CHOICE
        
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', start)],
            states={
                ARRIVAL: [
                    MessageHandler(filters.Regex('👣 Исследовать город'), explore_city),
                    MessageHandler(filters.Regex('🍻 Найти бар'), go_to_bar),
                    MessageHandler(filters.Regex('📊 Мой статус'), show_status),
                    MessageHandler(filters.Regex('🎒 Инвентарь'), show_inventory),
                ],
                BAR_CHOICE: [
                    MessageHandler(filters.Regex('🍺 Заказать пиво'), order_beer),
                    MessageHandler(filters.Regex('👂 Расспросить о Зоне'), ask_about_zone),
                    MessageHandler(filters.Regex('⬅️ Выйти из бара'), cancel),
                ],
            },
            fallbacks=[CommandHandler('cancel', cancel)]
        )
        
        application.add_handler(conv_handler)
        application.initialize()
        print("✅ Bot application setup completed")
    
    return application

@csrf_exempt
def webhook(request):
    if request.method == 'POST':
        try:
            # Парсим входящее обновление от Telegram
            data = json.loads(request.body)
            print("📨 Received update:", data)
            
            # Настраиваем бота если еще не настроен
            app = setup_bot()
            if app is None:
                return JsonResponse({'status': 'error', 'message': 'Bot not configured'})
            
            # Создаем объект Update
            update = Update.de_json(data, app.bot)
            
            # Обрабатываем обновление
            async def process_update():
                await app.process_update(update)
            
            # Запускаем асинхронную обработку
            asyncio.run(process_update())
            
            print("✅ Update processed successfully")
            return JsonResponse({'status': 'ok'})
            
        except Exception as e:
            print("❌ Error in webhook:", str(e))
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)
