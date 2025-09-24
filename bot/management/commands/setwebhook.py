from django.core.management.base import BaseCommand
import requests
import os

class Command(BaseCommand):
    help = 'Set Telegram webhook'
    
    def handle(self, *args, **options):
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        webhook_url = os.getenv('RENDER_EXTERNAL_URL') + '/webhook/'
        
        if not token:
            self.stdout.write(self.style.ERROR('TELEGRAM_BOT_TOKEN not found'))
            return
            
        if not webhook_url:
            self.stdout.write(self.style.ERROR('RENDER_EXTERNAL_URL not found'))
            return
        
        response = requests.get(
            f'https://api.telegram.org/bot{token}/setWebhook',
            params={'url': webhook_url}
        )
        
        if response.status_code == 200:
            self.stdout.write(
                self.style.SUCCESS(f'Webhook set successfully: {webhook_url}')
            )
            self.stdout.write(f'Response: {response.json()}')
        else:
            self.stdout.write(
                self.style.ERROR(f'Error setting webhook: {response.text}')
            )
