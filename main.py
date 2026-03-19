import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

TOKEN = os.getenv("TOKEN")

# Responses
insights = [
    "Most people don’t see reality directly.\nThey see their interpretation of it.",
    "Perception shapes behavior more than truth.",
    "What you ignore often controls you."
]

mindsets = [
    "Control your reaction.\nThat’s where real power begins.",
    "Discipline beats motivation over time.",
    "Consistency builds what intensity cannot sustain."
]

# /start with buttons
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🧠 Insight", callback_data="insight")],
        [InlineKeyboardButton("🎯 Mindset", callback_data="mindset")],
        [InlineKeyboardButton("⚡ Focus", callback_data="focus")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "ZAHRA is active.\nChoose an option:",
        reply_markup=reply_markup
    )

# Button click handler
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "insight":
        text = random.choice(insights)

    elif data == "mindset":
        text = random.choice(mindsets)

    elif data == "focus":
        text = "Focus is built by removing distractions."

    else:
        text = "ZAHRA is observing."

    await query.edit_message_text(text)

# App setup
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

print("ZAHRA running...")
app.run_polling()
