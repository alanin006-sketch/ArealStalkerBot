from telegram import Update
from telegram.ext import ContextTypes
from telegram import ReplyKeyboardMarkup

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_name = update.effective_user.first_name or "Сталкер"
        
        welcome_text = f"""
*ДНЕВНИК НОВИЧКА* 🚉

Привет, {user_name}! Ты прибыл в Хармонт...

Бот успешно запущен! Функциональность в разработке.

*Доступные команды:*
/start - начать игру
        """
        
        await update.message.reply_text(welcome_text, parse_mode='Markdown')
        print(f"✅ Start command processed for {user_name}")
        
    except Exception as e:
        print("❌ Error in start:", e)
        await update.message.reply_text("Произошла ошибка.")
