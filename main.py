import os
from copy import deepcopy
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("TOKEN")

# Menu
keyboard = [
    ["Think"],
    ["Decide"],
    ["Focus"],
    ["Undo"],
    ["Cancel"]
]

reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# State + history
user_state = {}
user_history = {}
user_data_store = {}


# ---------------- UTIL ----------------
def push_state(user_id, state, data):
    if user_id not in user_history:
        user_history[user_id] = []

    user_history[user_id].append({
        "state": state,
        "data": deepcopy(data)
    })


def pop_state(user_id):
    if user_id not in user_history or len(user_history[user_id]) == 0:
        return None

    return user_history[user_id].pop()


# ---------------- START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    user_state[user_id] = None
    user_history[user_id] = []
    context.user_data.clear()

    await update.message.reply_text(
        "ZAHRA Core System active.\nSelect a mode:",
        reply_markup=reply_markup
    )


# ---------------- CANCEL ----------------
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    user_state[user_id] = None
    user_history[user_id] = []
    context.user_data.clear()

    await update.message.reply_text("Cancelled. Reset complete.", reply_markup=reply_markup)


# ---------------- UNDO ----------------
async def undo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    previous = pop_state(user_id)

    if not previous:
        await update.message.reply_text("Nothing to undo.")
        return

    # Restore previous state
    user_state[user_id] = previous["state"]
    context.user_data.clear()
    context.user_data.update(previous["data"])

    await update.message.reply_text(f"Reverted to previous step: {previous['state']}")


# ---------------- HANDLER ----------------
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    state = user_state.get(user_id)

    if user_id not in user_history:
        user_history[user_id] = []

    # ---------------- CANCEL ----------------
    if text == "Cancel":
        return await cancel(update, context)

    # ---------------- UNDO ----------------
    if text == "Undo":
        return await undo(update, context)

    # ---------------- THINK ----------------
    if text == "Think":
        push_state(user_id, state, dict(context.user_data))
        user_state[user_id] = "think_situation"
        await update.message.reply_text("State your situation.")
        return

    if state == "think_situation":
        push_state(user_id, state, dict(context.user_data))
        context.user_data["situation"] = text
        user_state[user_id] = "think_goal"
        await update.message.reply_text("State your goal.")
        return

    if state == "think_goal":
        push_state(user_id, state, dict(context.user_data))
        context.user_data["goal"] = text
        user_state[user_id] = "think_block"
        await update.message.reply_text("What is blocking you?")
        return

    if state == "think_block":
        situation = context.user_data.get("situation")
        goal = context.user_data.get("goal")
        block = text

        user_state[user_id] = None
        user_history[user_id] = []

        await update.message.reply_text(
            "Analysis:\n\n"
            f"Situation: {situation}\n"
            f"Goal: {goal}\n"
            f"Block: {block}\n\n"
            "Direction:\n"
            "- Focus on controllable factors\n"
            "- Remove distractions\n"
            "- Execute first step"
        )
        return

    # ---------------- DECIDE ----------------
    if text == "Decide":
        push_state(user_id, state, dict(context.user_data))
        user_state[user_id] = "decide_option1"
        await update.message.reply_text("Enter Option 1:")
        return

    if state == "decide_option1":
        push_state(user_id, state, dict(context.user_data))
        context.user_data["option1"] = text
        user_state[user_id] = "decide_option2"
        await update.message.reply_text("Enter Option 2:")
        return

    if state == "decide_option2":
        option1 = context.user_data.get("option1")
        option2 = text

        user_state[user_id] = None
        user_history[user_id] = []

        await update.message.reply_text(
            "Decision Analysis:\n\n"
            f"Option 1: {option1}\n"
            f"Option 2: {option2}\n\n"
            "Compare long-term impact, risk, and alignment."
        )
        return

    # ---------------- FOCUS ----------------
    if text == "Focus":
        await update.message.reply_text(
            "Focus Mode:\n"
            "- Choose one task\n"
            "- Eliminate distractions\n"
            "- Work without switching"
        )
        return

    await update.message.reply_text("ZAHRA is ready.")


# ---------------- APP ----------------
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("cancel", cancel))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

print("ZAHRA Advanced running...")
app.run_polling()
