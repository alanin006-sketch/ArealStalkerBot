import os
import requests
from django.apps import AppConfig

class StalkerBotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stalker_bot'
    
    def ready(self):
        # Устанавливаем webhook только при запуске в production
        if os.environ.get('RUN_MAIN') and not os.environ.get('DEBUG'):
            token = os.getenv('TELEGRAM_BOT_TOKEN')
            webhook_url = os.getenv('RENDER_EXTERNAL_URL')
            
            if token and webhook_url:
                try:
                    full_webhook_url = f"{webhook_url}/webhook/"
                    response = requests.get(
                        f'https://api.telegram.org/bot{token}/setWebhook',
                        params={'url': full_webhook_url},
                        timeout=10
                    )
                    print(f"✅ Webhook установлен: {full_webhook_url}")
                    print(f"Ответ Telegram: {response.json()}")
                except Exception as e:
                    print(f"❌ Ошибка установки webhook: {e}")
