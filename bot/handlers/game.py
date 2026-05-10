from telegram import Update
from telegram.ext import ContextTypes
from bot.game.engine import GameEngine
from bot.utils.helpers import get_display_name, get_mention
from bot.utils.messages import game_start_msg
from bot.game.roles import role_dm_header, get_role_abilities_text
from bot.utils.helpers import send_dm
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
        await update.message.reply_text("❌ Only group admins can start a game!")
        return

    await db.register_group(chat.id, chat.title or "Group")

    game = await db.get_active_game(chat.id)

    # ── Case 1: Game already running ────────────────────────────
    if game and game["status"] in ("active", "voting"):
        await update.message.reply_text(
            "⚠️ A game is already running in this group!\n\n"
            "Use /status to see it, or /endgame to end it."
        )
        return

    # ── Case 2: Lobby exists → start it ─────────────────────────
    if game and game["status"] == "waiting":
        game_id = _gid(game)
        players = await db.get_players(game_id)
        count = len(players)

        if count < 3:
            await update.message.reply_text(
                f"⏳ *Not enough players!*\n\n"
                f"👥 {count}/3 players joined.\n"
                f"Ask others to tap *Join Game* or use /joingame.",
                parse_mode="Markdown"
            )
            return

        engine = GameEngine(db)
        result = await engine.start_game(context.bot, game_id, chat.id)

        if not result["success"]:
            await update.message.reply_text(f"❌ {result['reason']}")
            return

        await update.message.reply_text(
            game_start_msg(result["player_count"], result["imposter_count"]),
            parse_mode="Markdown"
        )
        return

    # ── Case 3: No game → create new lobby ──────────────────────
    user_data = await db.get_user(user.id)
    if not user_data or not user_data.get("chat_id"):
        await update.message.reply_text(
            "⚠️ *Please start me in DM first!*\n\n"
            "Search this bot on Telegram → open private chat → send /start\n"
            "Then come back and try /startgame again.",
            parse_mode="Markdown"
        )
        return

    engine = GameEngine(db)
    game_id = await engine.create_game(chat.id, user.id)

    if game_id is None:
        await update.message.reply_text(
            "⚠️ A game already exists! Use /status to check or /endgame to end it."
        )
        return

    await db.add_player(game_id, user.id)

    from bot.utils.keyboards import join_game_keyboard
    host_mention = get_mention(user.id, get_display_name(user))
    await update.message.reply_text(
        f"🎮 *Game Lobby is Open!*\n\n"
        f"👑 Host: {host_mention}\n"
        f"👥 Minimum players needed: *3*\n\n"
        f"📱 *Important:* Everyone must DM me /start first so I can send secret roles!\n\n"
        f"Tap *Join Game* below, then admin uses /startgame again to begin!",
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
            "⚠️ *You need to start me in DM first!*\n\n"
            "Open a private chat with me → send /start\n"
            "Then come back and use /joingame.",
            parse_mode="Markdown"
        )
        return

    game = await db.get_active_game(chat.id)
    if not game:
        await update.message.reply_text("❌ No active game right now. Ask an admin to /startgame!")
        return

    game_id = _gid(game)
    existing = await db.get_player(game_id, user.id)
    if existing:
        await update.message.reply_text("✅ You're already in the game!")
        return

    # ── Mid-game joining (active game) ───────────────────────────
    if game["status"] == "active":
        await db.add_player(game_id, user.id)
        await db.update_player_field(game_id, user.id, "role", "crewmate")
        players = await db.get_players(game_id)

        # Send role DM to late joiner
        chat_id = user_data.get("chat_id")
        if chat_id:
            header = role_dm_header("crewmate")
            abilities = get_role_abilities_text("crewmate")
            await send_dm(
                context.bot, chat_id,
                f"{header}\n"
                f"⚠️ *You joined mid-game as a Crewmate!*\n"
                f"Complete tasks and find the Impostor.\n\n"
                f"🛠️ *Your Abilities:*\n{abilities}"
            )

        player_mention = get_mention(user.id, get_display_name(user))
        await update.message.reply_text(
            f"✅ {player_mention} joined the ongoing game!\n\n"
            f"👥 Total players: *{len(players)}*\n"
            f"📩 Check your DM for your role!",
            parse_mode="Markdown"
        )
        return

    # ── Normal lobby joining ─────────────────────────────────────
    if game["status"] == "voting":
        await update.message.reply_text(
            "🗳️ Voting is in progress! You can join the next game."
        )
        return

    await db.add_player(game_id, user.id)
    players = await db.get_players(game_id)
    count = len(players)

    if count >= 3:
        suffix = "✅ Enough players! Admin can use /startgame to begin."
    else:
        suffix = f"⏳ Need {3 - count} more player(s)..."

    player_mention = get_mention(user.id, get_display_name(user))
    await update.message.reply_text(
        f"✅ {player_mention} joined the lobby!\n"
        f"👥 Players: *{count}* · {suffix}",
        parse_mode="Markdown"
    )


async def leavegame_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = context.bot_data["db"]
    user = update.effective_user
    chat = update.effective_chat

    game = await db.get_active_game(chat.id)
    if not game or game["status"] != "waiting":
        await update.message.reply_text("❌ You can only leave during the lobby phase.")
        return

    game_id = _gid(game)
    player = await db.get_player(game_id, user.id)
    if not player:
        await update.message.reply_text("❌ You're not in the current lobby!")
        return

    await db.remove_player(game_id, user.id)
    player_mention = get_mention(user.id, get_display_name(user))
    await update.message.reply_text(
        f"👋 {player_mention} left the lobby.",
        parse_mode="Markdown"
    )


async def gamestatus_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = context.bot_data["db"]
    chat = update.effective_chat

    if chat.type == "private":
        await update.message.reply_text("❌ Use this in a group!")
        return

    game = await db.get_active_game(chat.id)
    if not game:
        await update.message.reply_text("❌ No active game in this group. Use /startgame!")
        return

    game_id = _gid(game)
    engine = GameEngine(db)
    status = await engine.get_game_status(game_id)
    players = status["players"]

    player_lines = ""
    for p in players:
        name = p.get("first_name") or p.get("username") or "Player"
        uid = p["user_id"]
        mention = f"[{name}](tg://user?id={uid})"
        alive_icon = "💚" if p["is_alive"] else "💀"
        prem_icon = "⭐" if p.get("is_premium") else ""
        pts = p.get("points", 0)
        player_lines += f"{alive_icon} {prem_icon}{mention} — {pts} pts\n"

    status_labels = {
        "waiting": "⏳ Waiting for players",
        "active": "🎮 Game in progress",
        "voting": "🗳️ Voting phase",
        "ended": "🏁 Ended"
    }

    await update.message.reply_text(
        f"📊 *Game Status*\n\n"
        f"🎯 {status_labels.get(game['status'], game['status'])}\n"
        f"👥 Players: *{status['total_players']}* · 💚 Alive: *{status['alive_players']}*\n\n"
        f"{player_lines.strip()}",
        parse_mode="Markdown"
    )


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
        await update.message.reply_text("📋 No pending tasks right now. Check back soon!")
        return

    text = "📋 *Pending Tasks*\n\n"
    for i, t in enumerate(tasks, 1):
        cat = t.get("task_category", "general").capitalize()
        task_text = t.get("task_text", "")[:80]
        text += f"*{i}.* `[{cat}]` {task_text}\n\n"

    await update.message.reply_text(text, parse_mode="Markdown")
