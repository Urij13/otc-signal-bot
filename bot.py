
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from datetime import datetime

BOT_TOKEN = os.getenv("BOT_TOKEN")
USER_ID_WHITELIST = os.getenv("USER_ID_WHITELIST", "")
LANGUAGE = os.getenv("LANGUAGE", "uk")
TIME_START = os.getenv("TIME_START", "18:00")
TIME_END = os.getenv("TIME_END", "00:00")

WHITELIST_IDS = [int(x) for x in USER_ID_WHITELIST.split(",") if x.strip().isdigit()]

texts = {
    "uk": {
        "start": "👋 Привіт! Надішли сигнал (⬆️ або ⬇️) + пара.",
        "not_allowed": "❌ У тебе немає доступу.",
        "invalid": "⚠️ Надішли сигнал ⬆️ або ⬇️ разом з назвою пари.",
        "out_of_time": "⏰ Зараз бот не приймає сигнали (лише з 18:00 до 00:00)."
    },
    "en": {
        "start": "👋 Hi! Send a signal (⬆️ or ⬇️) with the pair.",
        "not_allowed": "❌ You are not allowed to use this bot.",
        "invalid": "⚠️ Send signal ⬆️ or ⬇️ with pair name.",
        "out_of_time": "⏰ Bot only accepts signals from 18:00 to 00:00."
    }
}

def is_in_time():
    now = datetime.now().time()
    start = datetime.strptime(TIME_START, "%H:%M").time()
    end = datetime.strptime(TIME_END, "%H:%M").time()
    return start <= now <= end if start < end else now >= start or now <= end

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in WHITELIST_IDS:
        await update.message.reply_text(texts[LANGUAGE]["not_allowed"])
        return
    await update.message.reply_text(texts[LANGUAGE]["start"])

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in WHITELIST_IDS:
        return

    if not is_in_time():
        await update.message.reply_text(texts[LANGUAGE]["out_of_time"])
        return

    text = update.message.text.strip()
    if not (("⬆️" in text or "⬇️" in text) and len(text.split()) >= 1):
        await update.message.reply_text(texts[LANGUAGE]["invalid"])
        return

    for uid in WHITELIST_IDS:
        if uid != update.effective_user.id:
            await context.bot.send_message(chat_id=uid, text=text)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
