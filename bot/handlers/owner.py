from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.helpers import is_owner, get_display_name
from bot.config import Config
from datetime import datetime, timedelta


async def broadcast_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = context.bot_data["db"]
    user = update.effective_user

    if not is_owner(user.id):
        await update.message.reply_text("❌ Owner only command!")
        return

    if not context.args:
        await update.message.reply_text("❌ Usage: /broadcast [message]")
        return

    msg_text = " ".join(context.args)
    groups = await db.get_all_groups()

    broadcast_text = (
        f"📢━━━━━━━━━━━━━━━━━━━━━━━━━━📢\n"
        f"         BOT ANNOUNCEMENT\n"
        f"📢━━━━━━━━━━━━━━━━━━━━━━━━━━📢\n\n"
        f"{msg_text}\n\n"
        f"📢━━━━━━━━━━━━━━━━━━━━━━━━━━📢"
    )

    success = 0
    failed = 0
    for group in groups:
        try:
            await context.bot.send_message(
                chat_id=group["group_id"],
                text=broadcast_text,
                parse_mode="Markdown"
            )
            success += 1
        except Exception:
            failed += 1

    await db.save_broadcast(msg_text, user.id, success)

    await update.message.reply_text(
        f"✅ **Broadcast sent!**\n\n"
        f"📤 Reached: **{success}** groups\n"
        f"❌ Failed: **{failed}** groups",
        parse_mode="Markdown"
    )


async def addpremium_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = context.bot_data["db"]
    user = update.effective_user

    if not is_owner(user.id):
        await update.message.reply_text("❌ Owner only command!")
        return

    if len(context.args) < 1:
        await update.message.reply_text("❌ Usage: /addpremium @username [days=30]")
        return

    target_username = context.args[0].lstrip("@")
    days = int(context.args[1]) if len(context.args) > 1 else 30

    target_user = await db.get_user_by_username(target_username)
    if not target_user:
        await update.message.reply_text(f"❌ @{target_username} not found in database!")
        return

    expires_at = await db.add_premium(target_user["user_id"], user.id, days)
    expires_str = expires_at.strftime("%Y-%m-%d")

    try:
        await context.bot.send_message(
            chat_id=target_user["chat_id"],
            text=(
                f"⭐━━━━━━━━━━━━━━━━━━━━━━━━━━⭐\n"
                f"    🎉 PREMIUM ACTIVATED! 🎉\n"
                f"⭐━━━━━━━━━━━━━━━━━━━━━━━━━━⭐\n\n"
                f"You've been granted **Premium** access!\n"
                f"📅 Valid for: **{days} days**\n"
                f"🏆 Expires: {expires_str}\n\n"
                f"✨ Premium Perks:\n"
                f"• ⭐ Premium badge\n"
                f"• 🎯 +5 bonus points per task\n"
                f"• 🔍 Extra scan uses (+2)\n"
                f"• 📨 Extra anon messages (+3)\n"
                f"• 🛡️ Extra shield use\n\n"
                f"Thanks for your support! 🙏"
            ),
            parse_mode="Markdown"
        )
    except Exception:
        pass

    await update.message.reply_text(
        f"✅ **Premium granted to @{target_username}**\n"
        f"📅 Duration: {days} days\n"
        f"🗓️ Expires: {expires_str}",
        parse_mode="Markdown"
    )


async def removepremium_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = context.bot_data["db"]
    user = update.effective_user

    if not is_owner(user.id):
        await update.message.reply_text("❌ Owner only command!")
        return

    if not context.args:
        await update.message.reply_text("❌ Usage: /removepremium @username")
        return

    target_username = context.args[0].lstrip("@")
    target_user = await db.get_user_by_username(target_username)
    if not target_user:
        await update.message.reply_text(f"❌ @{target_username} not found!")
        return

    await db.remove_premium(target_user["user_id"])
    await update.message.reply_text(
        f"✅ Premium removed from **@{target_username}**.",
        parse_mode="Markdown"
    )


async def ownerstats_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = context.bot_data["db"]
    user = update.effective_user

    if not is_owner(user.id):
        await update.message.reply_text("❌ Owner only command!")
        return

    stats = await db.get_global_stats()
    await update.message.reply_text(
        f"👑━━━━━━━━━━━━━━━━━━━━━━━━━━👑\n"
        f"       BOT GLOBAL STATS\n"
        f"👑━━━━━━━━━━━━━━━━━━━━━━━━━━👑\n\n"
        f"👤 Total Users: **{stats['users']}**\n"
        f"👥 Active Groups: **{stats['groups']}**\n"
        f"🎮 Games Completed: **{stats['games']}**\n"
        f"⭐ Premium Users: **{stats['premium']}**\n\n"
        f"👑━━━━━━━━━━━━━━━━━━━━━━━━━━👑",
        parse_mode="Markdown"
    )


async def banuser_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = context.bot_data["db"]
    user = update.effective_user

    if not is_owner(user.id):
        await update.message.reply_text("❌ Owner only command!")
        return

    if not context.args:
        await update.message.reply_text("❌ Usage: /ban @username")
        return

    target_username = context.args[0].lstrip("@")
    target_user = await db.get_user_by_username(target_username)
    if not target_user:
        await update.message.reply_text(f"❌ @{target_username} not found!")
        return

    await db.ban_user(target_user["user_id"])
    await update.message.reply_text(
        f"🚫 **@{target_username}** has been banned from using the bot.",
        parse_mode="Markdown"
    )


async def unbanuser_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = context.bot_data["db"]
    user = update.effective_user

    if not is_owner(user.id):
        await update.message.reply_text("❌ Owner only command!")
        return

    if not context.args:
        await update.message.reply_text("❌ Usage: /unban @username")
        return

    target_username = context.args[0].lstrip("@")
    target_user = await db.get_user_by_username(target_username)
    if not target_user:
        await update.message.reply_text(f"❌ @{target_username} not found!")
        return

    await db.unban_user(target_user["user_id"])
    await update.message.reply_text(
        f"✅ **@{target_username}** has been unbanned.",
        parse_mode="Markdown"
    )


async def allgroups_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = context.bot_data["db"]
    user = update.effective_user

    if not is_owner(user.id):
        await update.message.reply_text("❌ Owner only command!")
        return

    groups = await db.get_all_groups()
    if not groups:
        await update.message.reply_text("No active groups found.")
        return

    text = f"👥 **All Active Groups ({len(groups)}):**\n\n"
    for i, g in enumerate(groups, 1):
        text += f"{i}. **{g.get('title') or 'Unknown'}** (`{g['group_id']}`)\n"

    await update.message.reply_text(text, parse_mode="Markdown")


async def forceend_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = context.bot_data["db"]
    user = update.effective_user

    if not is_owner(user.id):
        await update.message.reply_text("❌ Owner only command!")
        return

    if not context.args:
        await update.message.reply_text("❌ Usage: /forceend [group_id]")
        return

    group_id = int(context.args[0])
    game = await db.get_active_game(group_id)
    if not game:
        await update.message.reply_text("❌ No active game in that group!")
        return

    await db.update_game_status(str(game["_id"]), "cancelled")
    try:
        await context.bot.send_message(
            chat_id=group_id,
            text="🛑 **Game has been force-ended by the bot owner.**",
            parse_mode="Markdown"
        )
    except Exception:
        pass
    await update.message.reply_text("✅ Game force-ended successfully.")
