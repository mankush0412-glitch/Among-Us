from telegram import Update
from telegram.ext import ContextTypes
from bot.game.engine import GameEngine
from bot.utils.helpers import get_display_name
from bot.utils.keyboards import vote_keyboard
from bot.utils.messages import voting_msg


def _gid(game) -> str:
    return str(game["_id"])


async def vote_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = context.bot_data["db"]
    user = update.effective_user
    chat = update.effective_chat

    if chat.type == "private":
        await update.message.reply_text("❌ Use this in a group!")
        return

    game = await db.get_active_game(chat.id)
    if not game or game["status"] not in ("active", "voting"):
        await update.message.reply_text("❌ No active voting right now! Wait for voting phase.")
        return

    game_id = _gid(game)
    player = await db.get_player(game_id, user.id)
    if not player:
        await update.message.reply_text("❌ You're not in this game!")
        return

    if not player["is_alive"]:
        await update.message.reply_text("👻 Ghosts cannot vote!")
        return

    if not context.args:
        await update.message.reply_text("❌ Usage: /vote @username  or  /vote skip")
        return

    target_username = context.args[0].lstrip("@")
    if target_username.lower() == "skip":
        target_id = 0
        target_name = "SKIP"
    else:
        target_user = await db.get_user_by_username(target_username)
        if not target_user:
            await update.message.reply_text(f"❌ @{target_username} not found!")
            return

        target_player = await db.get_player(game_id, target_user["user_id"])
        if not target_player or not target_player["is_alive"]:
            await update.message.reply_text(f"❌ @{target_username} is not alive in this game!")
            return

        target_id = target_user["user_id"]
        target_name = f"@{target_username}"

    current_phase = await db.get_current_phase(game_id)

    engine = GameEngine(db)
    result = await engine.process_vote(game_id, user.id, target_id, current_phase)

    if not result["success"]:
        await update.message.reply_text(f"❌ {result['reason']}")
        return

    await update.message.reply_text(
        f"🗳️ **{get_display_name(user)}** voted for **{target_name}**!",
        parse_mode="Markdown"
    )


async def meeting_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = context.bot_data["db"]
    user = update.effective_user
    chat = update.effective_chat

    if chat.type == "private":
        await update.message.reply_text("❌ Use this in a group!")
        return

    game = await db.get_active_game(chat.id)
    if not game or game["status"] != "active":
        await update.message.reply_text("❌ No active game!")
        return

    game_id = _gid(game)
    player = await db.get_player(game_id, user.id)
    if not player or not player["is_alive"]:
        await update.message.reply_text("❌ Only alive players can call meetings!")
        return

    emergency_used = player.get("emergency_used") or 0
    if emergency_used >= 2:
        await update.message.reply_text(
            "❌ You've used all your Emergency Meetings! Use /vote to still vote."
        )
        return

    await db.update_player_field(game_id, user.id, "emergency_used", emergency_used + 1)

    alive = await db.get_alive_players(game_id)
    next_phase = await db.get_next_phase(game_id)

    kb = vote_keyboard(alive, game_id, next_phase)
    name = get_display_name(user)

    await chat.send_message(
        f"🚨━━━━━━━━━━━━━━━━━━━━━━━━━━🚨\n"
        f"   🆘 EMERGENCY MEETING! 🆘\n"
        f"🚨━━━━━━━━━━━━━━━━━━━━━━━━━━🚨\n\n"
        f"📢 **{name}** called an Emergency Meeting!\n\n"
        f"👥 **{len(alive)}** alive players\n"
        f"🗳️ Discuss & vote now!\n\n"
        f"⏰ Meeting ends in 5 minutes!",
        parse_mode="Markdown",
        reply_markup=kb
    )
