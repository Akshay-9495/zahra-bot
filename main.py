import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("TOKEN")

# Menu buttons
keyboard = [
    ["🧠 Think"],
    ["🎯 Tasks"],
    ["⏱ Focus"]
]

reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# State storage
user_state = {}

# Task storage (per user)
user_tasks = {}


# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_state[user_id] = None

    await update.message.reply_text(
        "ZAHRA active.\nChoose a mode:",
        reply_markup=reply_markup
    )


# Main handler
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    state = user_state.get(user_id)

    # ---------------- THINK MODE ----------------
    if text == "🧠 Think":
        user_state[user_id] = "situation"
        await update.message.reply_text("Describe your situation.")
        return

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

    # ---------------- TASK MODE ----------------
    if text == "🎯 Tasks":
        tasks = user_tasks.get(user_id, [])

        if not tasks:
            await update.message.reply_text("No tasks found.\nSend a task to add one.")
        else:
            message = "Your tasks:\n\n"
            for i, t in enumerate(tasks, 1):
                message += f"{i}. {t}\n"
            message += "\nSend a new task to add more."
            await update.message.reply_text(message)

        user_state[user_id] = "add_task"
        return

    if state == "add_task":
        task = text

        if user_id not in user_tasks:
            user_tasks[user_id] = []

        user_tasks[user_id].append(task)
        user_state[user_id] = None

        await update.message.reply_text(f"Task added:\n{task}")
        return

    # ---------------- FOCUS MODE ----------------
    if text == "⏱ Focus":
        await update.message.reply_text(
            "Focus mode started.\n\n"
            "Choose one task.\n"
            "Remove distractions.\n"
            "Work without switching tasks."
        )
        return

    # Default response
    await update.message.reply_text("ZAHRA is observing.")


# App setup
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

print("ZAHRA running...")
app.run_polling()
