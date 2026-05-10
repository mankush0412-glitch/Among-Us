from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.messages import welcome_msg, help_msg, stats_msg, scoreboard_msg
from bot.utils.keyboards import help_keyboard, premium_keyboard
from bot.utils.helpers import is_owner, get_display_name, get_badge
from bot.config import Config


async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = context.bot_data["db"]
    user = update.effective_user
    chat = update.effective_chat

    if user.is_bot:
        return

    # Register user — chat_id is only passed from DM so it never overwrites a valid value
    await db.register_user(
        user.id,
        user.username,
        user.first_name,
        chat.id if chat.type == "private" else None
    )

    if chat.type != "private":
        await db.register_group(chat.id, chat.title or "Group")
        await update.message.reply_text(
            "👋 Hi! I'm the Among Us Bot.\n\n"
            "📩 *First, send /start to me in DM* so I can send you your secret role.\n"
            "Then use /joingame in the group to join!",
            parse_mode="Markdown"
        )
        return

    user_data = await db.get_user(user.id)
    is_prem = user_data.get("is_premium", False) if user_data else False
    badge = get_badge(user.id, is_prem)

    text = welcome_msg(f"{badge}{user.first_name}")
    await update.message.reply_text(text, parse_mode="Markdown", reply_markup=help_keyboard())


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        help_msg(),
        parse_mode="Markdown",
        reply_markup=help_keyboard()
    )


async def register_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = context.bot_data["db"]
    user = update.effective_user
    chat = update.effective_chat

    if user.is_bot:
        return

    user_data = await db.get_user(user.id)

    if not user_data or not user_data.get("chat_id"):
        await update.message.reply_text(
            "⚠️ You haven't started the bot in DM yet!\n\n"
            "📩 Send /start to me in private chat first, then come back.",
            parse_mode="Markdown"
        )
        return

    if chat.type != "private":
        await db.register_group(chat.id, chat.title or "Group")

    prem_text = "\n⭐ Status: *Premium Member*" if user_data.get("is_premium") else ""
    await update.message.reply_text(
        f"✅ *{user.first_name}* is registered and ready to play!{prem_text}\n\n"
        "Use /joingame when a game starts!",
        parse_mode="Markdown"
    )


async def mystats_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = context.bot_data["db"]
    user = update.effective_user
    chat = update.effective_chat

    user_data = await db.get_user(user.id)
    if not user_data:
        await update.message.reply_text(
            "❌ You're not registered! Use /start in my DM first."
        )
        return

    if chat.type == "private":
        all_scores = await db.fetchall("scores", {"user_id": user.id})
        score_data = {}
        if all_scores:
            score_data = {
                "total_points": sum(s.get("total_points", 0) for s in all_scores),
                "games_played": sum(s.get("games_played", 0) for s in all_scores),
                "games_won": sum(s.get("games_won", 0) for s in all_scores),
                "imposter_wins": sum(s.get("imposter_wins", 0) for s in all_scores),
                "crew_wins": sum(s.get("crew_wins", 0) for s in all_scores),
                "tasks_completed": sum(s.get("tasks_completed", 0) for s in all_scores),
                "kills_made": sum(s.get("kills_made", 0) for s in all_scores),
                "correct_votes": sum(s.get("correct_votes", 0) for s in all_scores),
            }
    else:
        score_data = await db.fetchone("scores", {"user_id": user.id, "group_id": chat.id})
        score_data = dict(score_data) if score_data else {}

    text = stats_msg(dict(user_data), score_data)
    await update.message.reply_text(text, parse_mode="Markdown")


async def score_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = context.bot_data["db"]
    chat = update.effective_chat

    if chat.type == "private":
        await update.message.reply_text(
            "📊 Use /score in a group to see that group's leaderboard!"
        )
        return

    scores = await db.get_scores(chat.id, limit=10)
    if not scores:
        await update.message.reply_text(
            "📊 No scores yet in this group! Play some games first."
        )
        return

    from bot.utils.keyboards import scoreboard_keyboard
    text = scoreboard_msg(scores, chat.title or "Group")
    await update.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=scoreboard_keyboard(chat.id)
    )


async def dm_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle non-command messages in DM — guide the user."""
    user = update.effective_user
    chat = update.effective_chat

    if chat.type != "private":
        return

    db = context.bot_data["db"]
    user_data = await db.get_user(user.id)

    if not user_data:
        await update.message.reply_text(
            "👋 Send /start to register and get started!"
        )
        return

    await update.message.reply_text(
        "Use /help to see all available commands.",
    )
