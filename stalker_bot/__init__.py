import os
import requests
from django.apps import AppConfig

class StalkerBotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stalker_bot'
    
    def ready(self):
        if os.environ.get('RUN_MAIN'):
            # Запускается только один раз при старте сервера
            token = os.getenv('TELEGRAM_BOT_TOKEN')
            webhook_url = os.getenv('RENDER_EXTERNAL_URL', '') + '/webhook/'
            
            if token and webhook_url and 'onrender.com' in webhook_url:
                try:
                    response = requests.get(
                        f'https://api.telegram.org/bot{token}/setWebhook',
                        params={'url': webhook_url},
                        timeout=10
                    )
                    print(f"Webhook set: {response.json()}")
                except Exception as e:
                    print(f"Webhook setup failed: {e}")
