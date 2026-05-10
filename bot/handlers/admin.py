from telegram import Update
from telegram.ext import ContextTypes
from bot.game.engine import GameEngine
from bot.utils.helpers import get_display_name, get_mention, resolve_target


async def _is_admin(update: Update, context) -> bool:
    chat = update.effective_chat
    user = update.effective_user
    if chat.type == "private":
        return False
    member = await context.bot.get_chat_member(chat.id, user.id)
    return member.status in ("administrator", "creator")


async def endgame_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = context.bot_data["db"]
    chat = update.effective_chat
    user = update.effective_user

    if not await _is_admin(update, context):
        await update.message.reply_text("❌ Only admins can end the game!")
        return

    game = await db.get_active_game(chat.id)
    if not game:
        await update.message.reply_text("❌ No active game to end!")
        return

    await db.update_game_status(str(game["_id"]), "cancelled")
    await update.message.reply_text(
        f"🛑 *Game ended* by *{get_display_name(user)}*.\n\n"
        "No winner declared. Use /startgame to start a new game.",
        parse_mode="Markdown"
    )


async def addtask_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = context.bot_data["db"]
    chat = update.effective_chat
    user = update.effective_user

    if not await _is_admin(update, context):
        await update.message.reply_text("❌ Only admins can add custom tasks!")
        return

    if not context.args:
        await update.message.reply_text(
            "❌ *Usage:* `/addtask [task description]`\n\n"
            "*Example:* `/addtask Who was the first person on the moon?`",
            parse_mode="Markdown"
        )
        return

    task_text = " ".join(context.args)

    if len(task_text) < 10:
        await update.message.reply_text("❌ Task too short! Write at least 10 characters.")
        return

    if len(task_text) > 500:
        await update.message.reply_text("❌ Task too long! Maximum 500 characters.")
        return

    await db.add_custom_task(chat.id, task_text, user.id)
    await update.message.reply_text(
        f"✅ *Custom task added!*\n\n"
        f"📋 {task_text}\n\n"
        f"Use /listtasks to see all custom tasks.",
        parse_mode="Markdown"
    )


async def listtasks_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = context.bot_data["db"]
    chat = update.effective_chat

    if not await _is_admin(update, context):
        await update.message.reply_text("❌ Admins only!")
        return

    tasks = await db.list_custom_tasks(chat.id)
    if not tasks:
        await update.message.reply_text(
            "📋 No custom tasks yet!\n\nUse /addtask to add your first task."
        )
        return

    text = f"📋 *Custom Tasks ({len(tasks)})*\n\n"
    for i, t in enumerate(tasks, 1):
        text += f"`{i}.` {t['task_text'][:100]}\n"
        if i >= 20:
            text += f"\n_...+{len(tasks)-20} more_"
            break

    await update.message.reply_text(text, parse_mode="Markdown")


async def deltask_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = context.bot_data["db"]
    chat = update.effective_chat

    if not await _is_admin(update, context):
        await update.message.reply_text("❌ Admins only!")
        return

    if not context.args:
        await update.message.reply_text(
            "❌ *Usage:* `/deltask [part of task text]`\n\nUse /listtasks to see all tasks.",
            parse_mode="Markdown"
        )
        return

    search = " ".join(context.args)
    deleted = await db.delete_custom_task(chat.id, search)

    if deleted:
        await update.message.reply_text(f"🗑️ Task matching `{search}` deleted!", parse_mode="Markdown")
    else:
        await update.message.reply_text(
            f"❌ No task found matching `{search}`.\n\nUse /listtasks to see all tasks.",
            parse_mode="Markdown"
        )


async def settime_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await _is_admin(update, context):
        await update.message.reply_text("❌ Admins only!")
        return

    await update.message.reply_text(
        "⚙️ *Game Schedule*\n\n"
        "🌅 Game starts: 9:00 AM\n"
        "📋 New task every: 2 hours\n"
        "🗳️ Voting starts: 7:00 PM\n"
        "🏆 Reveal: 9:00 PM\n"
        "📊 Scoreboard: Every 6 hours\n\n"
        "_To change timings, update env vars and restart._",
        parse_mode="Markdown"
    )


async def kickplayer_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = context.bot_data["db"]
    chat = update.effective_chat

    if not await _is_admin(update, context):
        await update.message.reply_text("❌ Admins only!")
        return

    target_user, error = await resolve_target(update, context, db, context.args)
    if error:
        await update.message.reply_text(error)
        return
    if not target_user:
        await update.message.reply_text(
            "❌ Usage:\n"
            "• `/kickplayer @username`\n"
            "• `/kickplayer 123456789` _(user ID)_\n"
            "• Reply to their message and send `/kickplayer`",
            parse_mode="Markdown"
        )
        return

    game = await db.get_active_game(chat.id)
    if not game:
        await update.message.reply_text("❌ No active game!")
        return

    target_mention = get_mention(
        target_user["user_id"],
        target_user.get("first_name") or target_user.get("username") or "Player"
    )
    await db.kill_player(str(game["_id"]), target_user["user_id"])
    await update.message.reply_text(
        f"👢 {target_mention} was removed from the game by an admin.",
        parse_mode="Markdown"
    )


async def pingall_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = context.bot_data["db"]
    chat = update.effective_chat

    if not await _is_admin(update, context):
        await update.message.reply_text("❌ Admins only!")
        return

    game = await db.get_active_game(chat.id)
    if not game:
        await update.message.reply_text("❌ No active game!")
        return

    alive = await db.get_alive_players(str(game["_id"]))
    if not alive:
        await update.message.reply_text("No alive players to ping!")
        return

    mentions = " ".join([
        f"[{p.get('first_name') or p.get('username') or 'Player'}](tg://user?id={p['user_id']})"
        for p in alive
    ])

    msg = " ".join(context.args) if context.args else "Don't forget to check the latest task!"
    await update.message.reply_text(
        f"📣 *Attention, all players!*\n\n{msg}\n\n{mentions}",
        parse_mode="Markdown"
    )
