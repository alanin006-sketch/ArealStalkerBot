from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
import os
from bot.handlers import *
from bot.states import *

@csrf_exempt
def webhook(request):
    if request.method == 'POST':
        # Инициализация приложения
        application = Application.builder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()
        
        # Создаем обработчик диалога
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
        
        # Обработка обновления
        update = Update.de_json(request.json, application.bot)
        application.initialize()
        application.process_update(update)
        
        return JsonResponse({'status': 'ok'})
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)
