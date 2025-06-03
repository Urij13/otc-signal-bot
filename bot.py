import re
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = 
def parse_signal(text):
    text = text.lower()

    direction = None
    if "⬆" in text or "вгору" in text or "вверх" in text or "up" in text or re.search(r'\^+', text):
        direction = "⬆️"
    elif "⬇" in text or "вниз" in text or "down" in text or re.search(r'v+', text):
        direction = "⬇️"

    match = re.search(r"([A-Z]{3}/[A-Z]{3})", text.upper())
    pair = match.group(1) if match else None

    return pair, direction

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Привіт! Надішли сигнал (⬆️ або ⬇️) + назву пари.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    pair, direction = parse_signal(user_input)

    if pair and direction:
        await update.message.reply_text(f"✅ Сигнал прийнято:\nПара: {pair}\nНапрямок: {direction}")
    else:
        await update.message.reply_text("⚠️ Надішли сигнал ⬆️ або ⬇️ разом з назвою пари (наприклад: EUR/USD OTC ⬆️)")

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
