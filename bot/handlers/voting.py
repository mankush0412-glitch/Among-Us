from telegram import Update
from telegram.ext import ContextTypes
from bot.game.engine import GameEngine
from bot.utils.helpers import get_display_name, get_mention, resolve_target
from bot.utils.keyboards import vote_keyboard
from bot.utils.messages import voting_msg
from bot.config import Config


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
        await update.message.reply_text("❌ No voting is happening right now!")
        return

    game_id = _gid(game)
    player = await db.get_player(game_id, user.id)
    if not player:
        await update.message.reply_text("❌ You're not in this game!")
        return

    if not player["is_alive"]:
        await update.message.reply_text("👻 Ghosts cannot vote!")
        return

    # ── If no argument and no reply → show inline keyboard (like /meeting) ──
    has_reply = bool(getattr(update.message, "reply_to_message", None))
    has_args  = bool(context.args)

    if not has_args and not has_reply:
        alive = await db.get_alive_players(game_id)
        current_phase = await db.get_current_phase(game_id)
        kb = vote_keyboard(alive, game_id, current_phase)
        voter_mention = get_mention(user.id, get_display_name(user))
        await update.message.reply_text(
            f"🗳️ *Who do you want to vote out?*\n\n"
            f"{voter_mention}, tap a name below to cast your vote.\n"
            f"Or use `/vote @username` to vote directly.",
            parse_mode="Markdown",
            reply_markup=kb
        )
        return

    # Handle "skip" shortcut first
    if context.args and context.args[0].lower() == "skip":
        target_id = 0
        target_name = "SKIP"
    else:
        target_user, error = await resolve_target(update, context, db, context.args)
        if error:
            await update.message.reply_text(error)
            return
        if not target_user:
            await update.message.reply_text(
                "❌ Usage:\n"
                "• `/vote @username`\n"
                "• `/vote 123456789` _(user ID)_\n"
                "• `/vote skip`\n"
                "• Reply to their message and send `/vote`\n"
                "• Or just `/vote` to see the keyboard",
                parse_mode="Markdown"
            )
            return

        target_player = await db.get_player(game_id, target_user["user_id"])
        if not target_player or not target_player["is_alive"]:
            target_mention = get_mention(
                target_user["user_id"],
                target_user.get("first_name") or target_user.get("username") or "Player"
            )
            await update.message.reply_text(
                f"❌ {target_mention} is not alive in this game!",
                parse_mode="Markdown"
            )
            return

        target_id = target_user["user_id"]
        target_name = get_mention(
            target_id,
            target_user.get("first_name") or target_user.get("username") or "Player"
        )

    current_phase = await db.get_current_phase(game_id)
    engine = GameEngine(db)
    result = await engine.process_vote(game_id, user.id, target_id, current_phase)

    if not result["success"]:
        await update.message.reply_text(f"❌ {result['reason']}")
        return

    voter_mention = get_mention(user.id, get_display_name(user))
    await update.message.reply_text(
        f"🗳️ {voter_mention} voted for *{target_name}*!",
        parse_mode="Markdown"
    )

    # ── Check if all alive players have voted → auto-reveal result ──
    alive = await db.get_alive_players(game_id)
    vote_count = await db.get_vote_count(game_id, current_phase)
    if vote_count >= len(alive):
        await _auto_eject(context.bot, db, engine, game_id, chat.id, current_phase)


async def _auto_eject(bot, db, engine, game_id: str, group_id: int, phase: int):
    """Called when all alive players have voted — immediately reveals result."""
    try:
        result = await engine.process_eject(bot, game_id, group_id, phase)

        # Announce eject result
        await bot.send_message(
            chat_id=group_id,
            text=result["message"],
            parse_mode="MarkdownV2"
        )

        # If game not over, transition back to active so scheduler doesn't double-eject
        if not result.get("game_over"):
            await db.update_game_status(game_id, "active")
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"Auto-eject error: {e}")


async def meeting_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = context.bot_data["db"]
    user = update.effective_user
    chat = update.effective_chat

    if chat.type == "private":
        await update.message.reply_text("❌ Use this in a group!")
        return

    game = await db.get_active_game(chat.id)
    if not game or game["status"] != "active":
        await update.message.reply_text("❌ No active game running!")
        return

    game_id = _gid(game)
    player = await db.get_player(game_id, user.id)
    if not player or not player["is_alive"]:
        await update.message.reply_text("❌ Only alive players can call meetings!")
        return

    emergency_used = player.get("emergency_used") or 0
    if emergency_used >= Config.MAX_EMERGENCY_MEETINGS:
        await update.message.reply_text(
            f"❌ You've used all your emergency meetings!\n"
            f"Use /vote @player to still cast your vote."
        )
        return

    await db.update_player_field(game_id, user.id, "emergency_used", emergency_used + 1)

    alive = await db.get_alive_players(game_id)
    next_phase = await db.get_next_phase(game_id)
    kb = vote_keyboard(alive, game_id, next_phase)
    caller_mention = get_mention(user.id, get_display_name(user))

    await chat.send_message(
        f"🚨 *Emergency Meeting!*\n\n"
        f"📢 {caller_mention} called the meeting!\n"
        f"👥 *{len(alive)}* players alive\n\n"
        f"Discuss and find the Impostor!\n"
        f"Tap a button below or use /vote @player _(or reply + /vote)_\n"
        f"⏰ Meeting ends when everyone votes or after 5 minutes!",
        parse_mode="Markdown",
        reply_markup=kb
    )
