import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("TOKEN")

keyboard = [
    ["🧠 Think"],
    ["🎯 Tasks"],
    ["⏱ Focus"]
]

reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Store user states
user_state = {}

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_state[update.effective_user.id] = None

    await update.message.reply_text(
        "ZAHRA active.\nChoose a mode:",
        reply_markup=reply_markup
    )

# Handle messages
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    state = user_state.get(user_id)

    # Start Thinking Flow
    if text == "🧠 Think":
        user_state[user_id] = "situation"
        await update.message.reply_text("Describe your situation.")
        return

    # Thinking flow steps
    if state == "situation":
        user_state[user_id] = "goal"
        context.user_data["situation"] = text
        await update.message.reply_text("What is your goal?")
        return

    elif state == "goal":
        user_state[user_id] = "block"
        context.user_data["goal"] = text
        await update.message.reply_text("What is blocking you?")
        return

    elif state == "block":
        situation = context.user_data.get("situation", "")
        goal = context.user_data.get("goal", "")
        block = text

        user_state[user_id] = None

        await update.message.reply_text(
            "Analysis:\n"
            f"Situation: {situation}\n"
            f"Goal: {goal}\n"
            f"Block: {block}\n\n"
            "Focus on what you can control. Remove distractions. Take the first step."
        )
        return

    # Other menu options
    if text == "🎯 Tasks":
        await update.message.reply_text("Task system will be added next.")

    elif text == "⏱ Focus":
        await update.message.reply_text("Focus mode: eliminate distractions and start now.")

    else:
        await update.message.reply_text("ZAHRA is observing.")

# App setup
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

print("ZAHRA running...")
app.run_polling()
