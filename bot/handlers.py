from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext

def start(update: Update, context: CallbackContext):
    try:
        chat_id = update.effective_chat.id
        user_name = update.effective_user.first_name or "Сталкер"
        
        welcome_text = f"""
*ДНЕВНИК НОВИЧКА* 🚉

Привет, {user_name}! Ты прибыл в Хармонт...

*Дата прибытия:* Сегодня
*Цель:* Разбогатеть или найти смысл? Пока не знаю.

Я слышал истории - одни возвращаются из Зоны с пустыми карманами и полными глазами ужаса. 
Другие... другие становятся богачами в одночасье. "Выкидыши" они называют эти штуки - артефакты, 
которые меняют реальность. Или просто сводят с ума.

Мне нужно понять, с чего начать. Город Хармонт выглядит как врата в другой мир...
        """
        
        # Простая клавиатура
        keyboard = ReplyKeyboardMarkup([
            ['👣 Исследовать город', '🍻 Найти бар'],
            ['📊 Мой статус', '🎒 Инвентарь']
        ], resize_keyboard=True)
        
        update.message.reply_text(welcome_text, parse_mode='Markdown')
        update.message.reply_text("Выбери действие:", reply_markup=keyboard)
        
        print(f"✅ Start command processed for user {user_name}")
        
    except Exception as e:
        print("❌ Error in start handler:", e)
        update.message.reply_text("Произошла ошибка. Попробуйте позже.")

# Заглушки для остальных команд
def explore_city(update: Update, context: CallbackContext):
    update.message.reply_text("🏙️ Исследование города... (в разработке)")

def go_to_bar(update: Update, context: CallbackContext):
    update.message.reply_text("🍻 Идем в бар... (в разработке)")

def show_status(update: Update, context: CallbackContext):
    update.message.reply_text("📊 Статус персонажа... (в разработке)")

def show_inventory(update: Update, context: CallbackContext):
    update.message.reply_text("🎒 Инвентарь... (в разработке)")
