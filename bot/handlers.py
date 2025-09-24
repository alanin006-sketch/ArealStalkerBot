from telegram import Update
from telegram.ext import ContextTypes
from .models import Player  # убираем GameState пока
from .keyboards import get_main_keyboard, get_bar_keyboard
from .states import ARRIVAL, BAR_CHOICE

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    
    try:
        # Создаем или получаем игрока
        player, created = Player.objects.get_or_create(
            chat_id=chat_id,
            defaults={
                'name': update.effective_user.first_name or 'Новичок',
                'location': 'train_station'
            }
        )
        
        if created:
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
        
        # Описание локации
        location_text = """
🚉 *Вокзал города Хармонт*

Ты выходишь из душного вагона на перрон. Воздух пахнет угольной пылью, дымом и чем-то... металлическим. 
Город выглядит серым и уставшим, но в глазах некоторых прохожих ты замечаешь странный блеск. 

*"Именно здесь,"* - думаешь ты, *"где-то рядом та самая Зона, о которой ходят легенды."*
        """
        
        await update.message.reply_text(location_text, parse_mode='Markdown')
        await update.message.reply_text("Выбери действие:", reply_markup=get_main_keyboard())
        
        return ARRIVAL
        
    except Exception as e:
        await update.message.reply_text("Произошла ошибка. Попробуйте позже.")
        print("Error in start:", e)
        return ARRIVAL

async def explore_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    exploration_text = """
🏙️ *Исследование Хармонта*

Город живет странной жизнени. Здесь смешались обычные люди и те, кто видел Зону. 
В их взглядах читается тоска и жадность одновременно.

Пока доступно только главное меню. Функциональность в разработке.
"""
    await update.message.reply_text(exploration_text, parse_mode='Markdown')
    await update.message.reply_text("Выбери действие:", reply_markup=get_main_keyboard())
    return ARRIVAL

async def go_to_bar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    
    try:
        player = Player.objects.get(chat_id=chat_id)
        player.location = 'bar'
        player.save()
        
        bar_text = """
🍻 *Бар "У Бурбуна"*

Ты заходишь в полутемное помещение. Воздух густой от табачного дыма и запаха дешевого алкоголя. 
За столиками сидятся люди с усталыми, но цепкими взглядами.

Пока доступно только главное меню. Функциональность в разработке.
"""
        await update.message.reply_text(bar_text, parse_mode='Markdown')
        await update.message.reply_text("Выбери действие:", reply_markup=get_main_keyboard())
        
        return ARRIVAL
        
    except Exception as e:
        await update.message.reply_text("Произошла ошибка.")
        print("Error in go_to_bar:", e)
        return ARRIVAL

# Упрощенные заглушки
async def order_beer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🍺 Функция в разработке. Возвращаемся в главное меню.", reply_markup=get_main_keyboard())
    return ARRIVAL

async def ask_about_zone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👂 Функция в разработке. Возвращаемся в главное меню.", reply_markup=get_main_keyboard())
    return ARRIVAL

async def show_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    try:
        player = Player.objects.get(chat_id=chat_id)
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
    except Exception as e:
        await update.message.reply_text("❌ Ошибка загрузки статуса")
    
    await update.message.reply_text("Выбери действие:", reply_markup=get_main_keyboard())
    return ARRIVAL

async def show_inventory(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    try:
        player = Player.objects.get(chat_id=chat_id)
        if player.inventory:
            inventory_text = "🎒 *Твой инвентарь:*\n" + "\n".join(f"• {item}" for item in player.inventory)
        else:
            inventory_text = "🎒 *Твой рюкзак пуст.* Пора его наполнить!"
        await update.message.reply_text(inventory_text, parse_mode='Markdown')
    except Exception as e:
        await update.message.reply_text("❌ Ошибка загрузки инвентаря")
    
    await update.message.reply_text("Выбери действие:", reply_markup=get_main_keyboard())
    return ARRIVAL

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Возвращаемся к главному меню...", reply_markup=get_main_keyboard())
    return ARRIVAL
