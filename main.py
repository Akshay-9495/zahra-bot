import os
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

TOKEN = os.getenv("TOKEN")

# Response pools
insights = [
    "Most people don’t see reality directly.\nThey see their interpretation of it.",
    "Perception often matters more than truth.",
    "What you focus on shapes what you experience."
]

mindsets = [
    "Control your reactions.\nThat’s where real influence begins.",
    "Discipline is choosing long-term over short-term.",
    "Consistency builds results that motivation cannot."
]

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ZAHRA is active.\nBe aware of patterns, not just people."
    )

# /insight (random)
async def insight(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(insights))

# /mindset (random)
async def mindset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(mindsets))

# Auto replies (keyword-based)
async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if "insight" in text:
        await update.message.reply_text(random.choice(insights))

    elif "mindset" in text:
        await update.message.reply_text(random.choice(mindsets))

    elif "focus" in text:
        await update.message.reply_text(
            "Focus is built by removing distractions."
        )

    else:
        await update.message.reply_text("ZAHRA is observing.")

# App setup
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("insight", insight))
app.add_handler(CommandHandler("mindset", mindset))

# Auto message handler
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))

print("ZAHRA running...")
app.run_polling()
