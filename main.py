import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ZAHRA is active.\n\nBe aware of patterns, not just people."
    )

# /insight
async def insight(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Most people don’t see reality directly.\n"
        "They see their interpretation of it."
    )

# /mindset
async def mindset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Control your reactions.\n"
        "That’s where real influence begins."
    )

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("insight", insight))
app.add_handler(CommandHandler("mindset", mindset))

print("ZAHRA running...")
app.run_polling()
