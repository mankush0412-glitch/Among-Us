from telegram import Update
from telegram.ext import ContextTypes
from bot.game.engine import GameEngine
from bot.utils.helpers import get_display_name, get_mention
from bot.config import Config


def _gid(game) -> str:
    return str(game["_id"])


async def startgame_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = context.bot_data["db"]
    user = update.effective_user
    chat = update.effective_chat

    if chat.type == "private":
        await update.message.reply_text("❌ Use this command in a group!")
        return

    member = await context.bot.get_chat_member(chat.id, user.id)
    if member.status not in ("administrator", "creator"):
        await update.message.reply_text("❌ Only admins can start the game!")
        return

    user_data = await db.get_user(user.id)
    if not user_data or not user_data.get("chat_id"):
        await update.message.reply_text(
            "⚠️ Start the bot in DM first!\nSend /start to me in private."
        )
        return

    await db.register_group(chat.id, chat.title or "Group")

    engine = GameEngine(db)
    game_id = await engine.create_game(chat.id, user.id)

    if game_id is None:
        await update.message.reply_text(
            "❌ A game is already active! Use /status to see it or /endgame to stop it."
        )
        return

    await db.add_player(game_id, user.id)

    from bot.utils.keyboards import join_game_keyboard
    text = (
        f"🎮━━━━━━━━━━━━━━━━━━━━━━━━━━🎮\n"
        f"      🚀 GAME LOBBY OPEN! 🚀\n"
        f"🎮━━━━━━━━━━━━━━━━━━━━━━━━━━🎮\n\n"
        f"👑 Started by: **{get_display_name(user)}**\n"
        f"👥 Players needed: minimum 3\n\n"
        f"📩 **IMPORTANT:** Everyone must first\n"
        f"send /start to me in DM to receive role!\n\n"
        f"Press **Join Game** button to play!\n"
        f"Game auto-starts when enough players join.\n\n"
        f"🎮━━━━━━━━━━━━━━━━━━━━━━━━━━🎮"
    )
    await update.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=join_game_keyboard(game_id)
    )


async def joingame_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = context.bot_data["db"]
    user = update.effective_user
    chat = update.effective_chat

    if chat.type == "private":
        await update.message.reply_text("❌ Use this command in a group!")
        return

    user_data = await db.get_user(user.id)
    if not user_data or not user_data.get("chat_id"):
        await update.message.reply_text(
            "⚠️ You must start me in DM first to receive your secret role!\n"
            "Send /start to me in private, then come back and /joingame"
        )
        return

    game = await db.get_active_game(chat.id)
    if not game:
        await update.message.reply_text("❌ No active game! Ask an admin to /startgame")
        return

    if game["status"] != "waiting":
        await update.message.reply_text("❌ Game already started! Wait for next round.")
        return

    game_id = _gid(game)
    existing = await db.get_player(game_id, user.id)
    if existing:
        await update.message.reply_text("✅ You're already in the game!")
        return

    await db.add_player(game_id, user.id)
    players = await db.get_players(game_id)
    count = len(players)

    await update.message.reply_text(
        f"✅ **{get_display_name(user)}** joined the game!\n"
        f"👥 Players: **{count}** (min 3 to start)\n\n"
        f"{'🚀 Use /startgame to begin!' if count >= 3 else f'⏳ Waiting for {3 - count} more player(s)...'}",
        parse_mode="Markdown"
    )


async def leavegame_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = context.bot_data["db"]
    user = update.effective_user
    chat = update.effective_chat

    game = await db.get_active_game(chat.id)
    if not game or game["status"] != "waiting":
        await update.message.reply_text("❌ No joinable game to leave.")
        return

    game_id = _gid(game)
    player = await db.get_player(game_id, user.id)
    if not player:
        await update.message.reply_text("❌ You're not in this game!")
        return

    await db.remove_player(game_id, user.id)
    await update.message.reply_text(
        f"👋 **{get_display_name(user)}** left the game lobby.",
        parse_mode="Markdown"
    )


async def gamestatus_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = context.bot_data["db"]
    chat = update.effective_chat

    if chat.type == "private":
        await update.message.reply_text("Use this in a group!")
        return

    game = await db.get_active_game(chat.id)
    if not game:
        await update.message.reply_text("❌ No active game in this group.")
        return

    game_id = _gid(game)
    engine = GameEngine(db)
    status = await engine.get_game_status(game_id)
    players = status["players"]

    player_list = ""
    for p in players:
        name = p.get("first_name") or p.get("username") or "Player"
        alive_icon = "💚" if p["is_alive"] else "💀"
        prem_icon = "⭐" if p.get("is_premium") else ""
        player_list += f"{alive_icon} {prem_icon}{name} — {p.get('points', 0)} pts\n"

    status_labels = {
        "waiting": "⏳ Waiting for players",
        "active": "🎮 Game in progress",
        "voting": "🗳️ Voting phase",
        "ended": "🏁 Game ended"
    }

    text = (
        f"📊━━━━━━━━━━━━━━━━━━━━━━━━━━📊\n"
        f"        GAME STATUS\n"
        f"📊━━━━━━━━━━━━━━━━━━━━━━━━━━📊\n\n"
        f"🎯 Status: **{status_labels.get(game['status'], game['status'])}**\n"
        f"👥 Total Players: **{status['total_players']}**\n"
        f"💚 Alive: **{status['alive_players']}**\n\n"
        f"**Players:**\n{player_list}\n"
        f"📊━━━━━━━━━━━━━━━━━━━━━━━━━━📊"
    )
    await update.message.reply_text(text, parse_mode="Markdown")


async def mytasks_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = context.bot_data["db"]
    user = update.effective_user
    chat = update.effective_chat

    game = await db.get_active_game(chat.id)
    if not game:
        await update.message.reply_text("❌ No active game!")
        return

    game_id = _gid(game)
    player = await db.get_player(game_id, user.id)
    if not player:
        await update.message.reply_text("❌ You're not in this game!")
        return

    tasks = await db.get_recent_tasks(game_id, limit=5)

    if not tasks:
        await update.message.reply_text("📋 No pending tasks right now! Check back soon.")
        return

    text = "📋 **Pending Tasks:**\n\n"
    for i, t in enumerate(tasks, 1):
        cat = t.get("task_category", "general").upper()
        task_text = t.get("task_text", "")[:80]
        text += f"{i}. [{cat}] {task_text}...\n\n"

    await update.message.reply_text(text, parse_mode="Markdown")
