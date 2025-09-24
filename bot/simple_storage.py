# Простое хранилище в памяти (потом заменим на базу)
players = {}

def get_player(chat_id):
    if chat_id not in players:
        players[chat_id] = {
            'name': 'Новичок',
            'health': 100,
            'money': 100,
            'location': 'train_station',
            'inventory': [],
            'reputation': 0
        }
    return players[chat_id]

def update_player(chat_id, updates):
    player = get_player(chat_id)
    player.update(updates)
    return player
