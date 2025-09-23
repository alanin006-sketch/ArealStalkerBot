from telegram import ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard():
    return ReplyKeyboardMarkup([
        ['👣 Исследовать город', '🍻 Найти бар'],
        ['🏪 Черный рынок', '🎫 Узнать про пропуск'],
        ['📊 Мой статус', '🎒 Инвентарь']
    ], resize_keyboard=True)

def get_bar_keyboard():
    return ReplyKeyboardMarkup([
        ['🍺 Заказать пиво', '🥃 Заказать виски'],
        ['👂 Расспросить о Зоне', '💼 Предложить дело'],
        ['⬅️ Выйти из бара']
    ], resize_keyboard=True)

def get_market_keyboard():
    return ReplyKeyboardMarkup([
        ['🛒 Купить снаряжение', '💰 Продать что-то'],
        ['📰 Спросить новости', '👥 Найти проводника'],
        ['⬅️ Уйти с рынка']
    ], resize_keyboard=True)

def get_exploration_keyboard():
    return ReplyKeyboardMarkup([
        ['🏢 Центр города', ['🏭 Промзона', '🚉 Вокзал']],
        ['🌲 Окраины', ['🏚️ Заброшки', '🚷 КПП в Зону']],
        ['⬅️ Вернуться']
    ], resize_keyboard=True)
