from django.db import models

class Player(models.Model):
    chat_id = models.BigIntegerField(unique=True)
    name = models.CharField(max_length=100, default="Новичок")
    health = models.IntegerField(default=100)
    luck = models.IntegerField(default=50)
    money = models.IntegerField(default=100)
    reputation = models.IntegerField(default=0)
    
    # Локация
    LOCATION_CHOICES = [
        ('train_station', 'Вокзал Хармонта'),
        ('bar', 'Бар "У Бурбуна"'),
        ('market', 'Черный рынок'),
        ('outskirts', 'Окраины города'),
    ]
    location = models.CharField(max_length=50, choices=LOCATION_CHOICES, default='train_station')
    
    # Инвентарь
    inventory = models.JSONField(default=list)
    
    # Состояния
    is_drunk = models.BooleanField(default=False)
    has_license = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.chat_id})"

class GameState(models.Model):
    player = models.OneToOneField(Player, on_delete=models.CASCADE)
    current_quest = models.CharField(max_length=100, default="arrival")
    completed_quests = models.JSONField(default=list)
    story_flags = models.JSONField(default=dict)
    
    def __str__(self):
        return f"Состояние {self.player.name}"
