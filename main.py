import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("TOKEN")

# Keyboard menu
keyboard = [
    ["🧠 Think"],
    ["🎯 Tasks"],
    ["⏱ Focus"]
]

reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ZAHRA active.\nChoose a mode:",
        reply_markup=reply_markup
    )

# Handle messages
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🧠 Think":
        await update.message.reply_text(
            "State your situation.\nZAHRA will guide your thinking."
        )

    elif text == "🎯 Tasks":
        await update.message.reply_text(
            "Task system coming next.\nFor now, describe what you need to track."
        )

    elif text == "⏱ Focus":
        await update.message.reply_text(
            "Focus mode.\nRemove distractions. Start now."
        )

    else:
        await update.message.reply_text("ZAHRA is observing.")

# App setup
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

print("ZAHRA running...")
app.run_polling()
