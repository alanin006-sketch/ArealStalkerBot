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
            text = message.get('text', '')
            chat_id = message.get('chat', {}).get('id')
            
            print(f"📨 Received: '{text}' from {chat_id}")
            
            token = os.getenv('TELEGRAM_BOT_TOKEN')
            
            if text == '/start':
                welcome_text = """
*ДНЕВНИК НОВИЧКА* 🚉

Привет! Ты прибыл в Хармонт...

Бот работает! Базовая функциональность подключена.
Разработка продолжается...
                """
                
                requests.post(
                    f"https://api.telegram.org/bot{token}/sendMessage",
                    json={
                        'chat_id': chat_id,
                        'text': welcome_text,
                        'parse_mode': 'Markdown'
                    }
                )
            
            return JsonResponse({'status': 'ok'})
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)
