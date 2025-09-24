# Простое хранилище в памяти для игроков
players = {}

def get_player(chat_id):
    """Получает данные игрока или создает нового"""
    if chat_id not in players:
        players[chat_id] = {
            'name': 'Новичок',
            'health': 100,
            'money': 100,
            'location': 'Вокзал Хармонта',
            'inventory': ['Рюкзак', 'Карта города'],
            'reputation': 0
        }
    return players[chat_id]

def update_player(chat_id, updates):
    """Обновляет данные игрока"""
    player = get_player(chat_id)
    player.update(updates)
    players[chat_id] = player
    return player

def get_all_players():
    """Возвращает всех игроков (для отладки)"""
    return players
