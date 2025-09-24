from telegram import Update
from telegram.ext import ContextTypes
from telegram import ReplyKeyboardMarkup

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
        
        # Простая клавиатура для начала
        keyboard = ReplyKeyboardMarkup([
            ['👣 Исследовать город', '🍻 Найти бар'],
            ['📊 Мой статус', '🎒 Инвентарь']
        ], resize_keyboard=True)
        
        await update.message.reply_text(welcome_text, parse_mode='Markdown')
        await update.message.reply_text("Выбери действие:", reply_markup=keyboard)
        
        print(f"✅ Start command processed for user {user_name} (chat_id: {chat_id})")
        
    except Exception as e:
        print("❌ Error in start handler:", e)
        await update.message.reply_text("Произошла ошибка. Попробуйте позже.")

# Заглушки для остальных команд
async def explore_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏙️ Исследование города... (в разработке)")

async def go_to_bar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🍻 Идем в бар... (в разработке)")

async def show_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📊 Статус персонажа... (в разработке)")

async def show_inventory(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎒 Инвентарь... (в разработке)")
