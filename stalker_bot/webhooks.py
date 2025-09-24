from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import json

@csrf_exempt
def webhook(request):
    if request.method == 'POST':
        # Пока просто логируем входящие сообщения
        try:
            data = json.loads(request.body)
            print("Received update:", data)
            
            # Простой ответ для теста
            return JsonResponse({'status': 'ok', 'message': 'Webhook received'})
        except Exception as e:
            print("Error:", e)
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)
