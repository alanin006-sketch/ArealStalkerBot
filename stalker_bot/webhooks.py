from bot.simple_storage import get_player, update_player
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
import os

@csrf_exempt
def webhook(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('message', {})
            text = message.get('text', '').strip()
            chat_id = message.get('chat', {}).get('id')
            
            print(f"📨 Received: '{text}' from {chat_id}")
            
            token = os.getenv('TELEGRAM_BOT_TOKEN')
            
            if text == '/start':
                welcome_text = """
*ДНЕВНИК НОВИЧКА* 🚉

Привет, сталкер! Ты прибыл в Хармонт - город на краю Зоны.

*Твои цели:*
• Изучить город
• Найти опытных сталкеров
• Раздобыть снаряжение
• Проникнуть в Зону
• Найти артефакты

*Доступные команды:*
/start - начать игру
/status - твой статус
/explore - исследовать город
/bar - найти бар сталкеров
                """
                
                # Клавиатура с кнопками
                keyboard = {
                    'keyboard': [
                        ['👣 Исследовать город', '🍻 Найти бар'],
                        ['📊 Мой статус', '🎒 Инвентарь']
                    ],
                    'resize_keyboard': True
                }
                
                requests.post(
                    f"https://api.telegram.org/bot{token}/sendMessage",
                    json={
                        'chat_id': chat_id,
                        'text': welcome_text,
                        'parse_mode': 'Markdown',
                        'reply_markup': keyboard
                    }
                )
            
            elif text == '/status' or text == '📊 Мой статус':
                status_text = """
*ТВОЙ СТАТУС* 📊

👤 Имя: Новичок
❤️ Здоровье: 100/100
💰 Деньги: 100 руб.
🎒 Инвентарь: 2 предмета

📍 Локация: Вокзал Хармонта
⭐ Репутация: 0

*Система сохранения в разработке...*
                """
                requests.post(
                    f"https://api.telegram.org/bot{token}/sendMessage",
                    json={
                        'chat_id': chat_id,
                        'text': status_text,
                        'parse_mode': 'Markdown'
                    }
                )
            
            elif text == '/explore' or text == '👣 Исследовать город':
                explore_text = """
*ИССЛЕДОВАНИЕ ХАРМОНТА* 🏙️

Ты выходишь на улицы города. Хармонт живет странной жизнью - смесь обычных людей и тех, кто видел Зону.

*Куда направишься?*
• 🏢 Центр города - учреждения и магазины
• 🏭 Промзона - заброшенные заводы
• 🚉 Вокзал - ворота в город
• 🌲 Окраины - ближе к Зоне
                """
                requests.post(
                    f"https://api.telegram.org/bot{token}/sendMessage",
                    json={
                        'chat_id': chat_id,
                        'text': explore_text,
                        'parse_mode': 'Markdown'
                    }
                )
            
            elif text == '/bar' or text == '🍻 Найти бар':
                bar_text = """
*БАР "У БУРБУНА"* 🍻

Ты находишь неприметную дверь с вывеской "У Бурбуна". Внутри - полумрак, запах табака и алкоголя.

За стойкой стоит массивный бармен с шрамом на щеке. За столиками - люди с усталыми, но цепкими взглядами.

*Что будешь делать?*
• 🍺 Заказать пиво (20 руб.)
• 👂 Расспросить о Зоне
• 💼 Найти работу
                """
                requests.post(
                    f"https://api.telegram.org/bot{token}/sendMessage",
                    json={
                        'chat_id': chat_id,
                        'text': bar_text,
                        'parse_mode': 'Markdown'
                    }
                )
            
            elif text == '🎒 Инвентарь':
                inventory_text = """
*ТВОЙ ИНВЕНТАРЬ* 🎒

Твой рюкзак пока пуст. Тебе нужно:
• 🔦 Фонарь
• 🧭 Компас
• 💊 Аптечка
• 🎯 Детектор аномалий
• 🍞 Продукты

Найди снаряжение в городе!
                """
                requests.post(
                    f"https://api.telegram.org/bot{token}/sendMessage",
                    json={
                        'chat_id': chat_id,
                        'text': inventory_text,
                        'parse_mode': 'Markdown'
                    }
                )
            
            return JsonResponse({'status': 'ok'})
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)
