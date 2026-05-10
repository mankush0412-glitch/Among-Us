from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.keyboards import premium_keyboard
from bot.config import Config


async def premium_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = context.bot_data["db"]
    user = update.effective_user

    user_data = await db.get_user(user.id)
    is_prem = user_data["is_premium"] if user_data else False
    expires = user_data["premium_expires"] if user_data else None

    if is_prem:
        expires_str = expires.strftime("%d %b %Y") if hasattr(expires, "strftime") else str(expires)[:10]
        await update.message.reply_text(
            f"⭐ *Your Premium Status*\n"
            f"{'─' * 28}\n\n"
            f"✅ Status: *Active Premium*\n"
            f"📅 Expires: *{expires_str}*\n\n"
            f"*Your perks:*\n"
            f"• ⭐ Premium badge in leaderboard\n"
            f"• 🎯 +5 bonus points per task\n"
            f"• 🔍 Extra scan uses (5 instead of 3)\n"
            f"• 📨 Extra anon messages (8 instead of 5)\n"
            f"• 🛡️ 2 shields per game instead of 1\n"
            f"• 🏆 Priority in score display\n"
            f"• 🎮 Access to exclusive game modes",
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(
            f"⭐ *Get Premium Access*\n"
            f"{'─' * 28}\n\n"
            f"Current status: *Free Player*\n\n"
            f"*Premium perks:*\n"
            f"• ⭐ Premium badge in leaderboard\n"
            f"• 🎯 +5 bonus points per task\n"
            f"• 🔍 Extra scan uses (5 instead of 3)\n"
            f"• 📨 Extra anon messages (8 instead of 5)\n"
            f"• 🛡️ 2 shields per game instead of 1\n"
            f"• 🏆 Priority in score display\n"
            f"• 🎮 Exclusive game modes\n\n"
            f"📩 Contact the bot owner to get Premium!",
            parse_mode="Markdown",
            reply_markup=premium_keyboard()
        )
