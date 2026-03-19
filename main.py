import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("8651170265:AAHVtQxgNsNqGmFEMe6bXCdqRn2gPFN8RyQ")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Be aware of the monster around you")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

print("ZAHRA running...")
app.run_polling()
