import os
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from django.conf import settings
from .models import Player, GameState
from .keyboards import *
from .states import *

# Текстовые константы
SCENE_DESCRIPTIONS = {
    'train_station': """
🚉 *Вокзал города Хармонт*

Ты выходишь из душного вагона на перрон. Воздух пахнет угольной пылью, дымом и чем-то... металлическим. 
Город выглядит серым и уставшим, но в глазах некоторых прохожих ты замечаешь странный блеск. 

*"Именно здесь,"* - думаешь ты, *"где-то рядом та самая Зона, о которой ходят легенды."*
""",
    
    'bar': """
🍻 *Бар "У Бурбуна"*

Ты заходишь в полутемное помещение. Воздух густой от табачного дыма и запаха дешевого алкоголя. 
За столиками сидятся люди с усталыми, но цепкими взглядами. В углу кто-то тихо наигрывает на гитаре. 

Бармен, массивный мужчина с шрамом на щеке, лениво протирает стакан.
"""
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    
    # Создаем или получаем игрока
    player, created = Player.objects.get_or_create(
        chat_id=chat_id,
        defaults={
            'name': update.effective_user.first_name or 'Новичок',
            'location': 'train_station'
        }
    )
    
    # Создаем состояние игры
    game_state, _ = GameState.objects.get_or_create(player=player)
    
    if created:
        # Первый запуск - начальная сцена
        welcome_text = """
*ДНЕВНИК НОВИЧКА*
        
Дата прибытия: Сегодня.
Цель: Разбогатеть или найти смысл? Пока не знаю.

Я слышал истории - одни возвращаются из Зоны с пустыми карманами и полными глазами ужаса. 
Другие... другие становятся богачами в одночасье. "Выкидыши" они называют эти штуки - артефакты, 
которые меняют реальность. Или просто сводят с ума.

Мне нужно понять, с чего начать. Город Хармонт выглядит как врата в другой мир...
        """
        
        await update.message.reply_text(welcome_text, parse_mode='Markdown')
        await update.message.reply_text(SCENE_DESCRIPTIONS['train_station'], 
                                      parse_mode='Markdown',
                                      reply_markup=get_main_keyboard())
    else:
        # Продолжение игры
        location_text = SCENE_DESCRIPTIONS.get(player.location, "Ты осматриваешься вокруг.")
        await update.message.reply_text(f"*Возвращение в игру*\n\n{location_text}", 
                                      parse_mode='Markdown',
                                      reply_markup=get_main_keyboard())
    
    return ARRIVAL

async def explore_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    player = Player.objects.get(chat_id=update.effective_chat.id)
    
    exploration_text = """
🏙️ *Исследование Хармонта*

Город живет странной жизнью. Здесь смешались обычные люди и те, кто видел Зону. 
В их взглядах читается тоска и жадность одновременно.

*Куда направишься?*
"""
    
    await update.message.reply_text(exploration_text, 
                                  parse_mode='Markdown',
                                  reply_markup=get_exploration_keyboard())
    return EXPLORE_CITY

async def go_to_bar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    player = Player.objects.get(chat_id=update.effective_chat.id)
    player.location = 'bar'
    player.save()
    
    await update.message.reply_text(SCENE_DESCRIPTIONS['bar'], 
                                  parse_mode='Markdown',
                                  reply_markup=get_bar_keyboard())
    
    # Первый визит в бар - особый диалог
    game_state = GameState.objects.get(player=player)
    if 'first_bar_visit' not in game_state.story_flags:
        await update.message.reply_text(
            "Бармен смотрит на тебя оценивающе: *'Новичок, да? Сначала купи, потом вопросы задавай.'*",
            parse_mode='Markdown'
        )
        game_state.story_flags['first_bar_visit'] = True
        game_state.save()
    
    return BAR_CHOICE

async def order_beer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    player = Player.objects.get(chat_id=update.effective_chat.id)
    
    if player.money >= 20:
        player.money -= 20
        player.is_drunk = True
        player.save()
        
        response = """
🍺 *Ты заказываешь пиво*

Бармен ставит перед тобой мутную кружку. Пиво горькое и теплое, но после дороги - то что надо.

*'За новичка!'* - хрипло смеется кто-то за соседним столиком. 
Теперь бармен смотрит на тебя чуть менее подозрительно.
        """
    else:
        response = "💸 *Не хватает денег.* Бармен презрительно хмыкает: *'Сначала заработай, потом пей.'*"
    
    await update.message.reply_text(response, parse_mode='Markdown')
    return BAR_CHOICE

async def ask_about_zone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    player = Player.objects.get(chat_id=update.effective_chat.id)
    game_state = GameState.objects.get(player=player)
    
    if player.is_drunk or game_state.story_flags.get('first_bar_visit'):
        response = """
👂 *Ты расспрашиваешь о Зоне*

Бармен понижает голос: *'Слушай, новичок. Зона - она не для любопытных. Туда идут либо от безысходности, либо от жадности.'*

*'Тебе нужен пропуск. И проводник. Без этого - вернешься в мешке. Если вернешься.'*

Он отходит обслуживать других посетителей, оставляя тебя с мыслями.
        """
        
        # Открываем новый квест
        if 'learned_about_pass' not in game_state.story_flags:
            game_state.story_flags['learned_about_pass'] = True
            game_state.save()
            
    else:
        response = "Бармен игнорирует тебя: *'Сначала стань клиентом, потом поговорим.'*"
    
    await update.message.reply_text(response, parse_mode='Markdown')
    return BAR_CHOICE

async def show_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    player = Player.objects.get(chat_id=update.effective_chat.id)
    
    status_text = f"""
📊 *ТВОЙ СТАТУС*

👤 Имя: {player.name}
❤️ Здоровье: {player.health}/100
🍀 Удача: {player.luck}/100
💰 Деньги: {player.money} руб.
⭐ Репутация: {player.reputation}

📍 Локация: {player.get_location_display()}
🎒 Инвентарь: {len(player.inventory)} предметов
    """
    
    await update.message.reply_text(status_text, parse_mode='Markdown')
    return ARRIVAL

async def show_inventory(update: Update, context: ContextTypes.DEFAULT_TYPE):
    player = Player.objects.get(chat_id=update.effective_chat.id)
    
    if player.inventory:
        inventory_text = "🎒 *Твой инвентарь:*\n" + "\n".join(f"• {item}" for item in player.inventory)
    else:
        inventory_text = "🎒 *Твой рюкзак пуст.* Пора его наполнить!"
    
    await update.message.reply_text(inventory_text, parse_mode='Markdown')
    return ARRIVAL

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Возвращаюсь к главному меню.",
        reply_markup=get_main_keyboard()
    )
    return ARRIVAL
