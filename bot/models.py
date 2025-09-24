from django.db import models

class Player(models.Model):
    chat_id = models.BigIntegerField(unique=True)
    name = models.CharField(max_length=100, default="Новичок")
    health = models.IntegerField(default=100)
    money = models.IntegerField(default=100)
    location = models.CharField(max_length=50, default='train_station')
    inventory = models.JSONField(default=list)
    
    def __str__(self):
        return f"{self.name} ({self.chat_id})"
