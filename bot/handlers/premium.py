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
        expire_text = f"📅 Expires: **{expires[:10]}**" if expires else "📅 Expires: **Never**"
        await update.message.reply_text(
            f"⭐━━━━━━━━━━━━━━━━━━━━━━━━━━⭐\n"
            f"      YOUR PREMIUM STATUS\n"
            f"⭐━━━━━━━━━━━━━━━━━━━━━━━━━━⭐\n\n"
            f"✅ Status: **ACTIVE PREMIUM**\n"
            f"{expire_text}\n\n"
            f"🎯 Your Premium Perks:\n"
            f"• ⭐ Premium badge in leaderboard\n"
            f"• 🎯 +5 bonus points per task\n"
            f"• 🔍 Extra scan uses (5 instead of 3)\n"
            f"• 📨 Extra anonymous messages (8 instead of 5)\n"
            f"• 🛡️ 2 shields per game instead of 1\n"
            f"• 🏆 Priority in score display\n"
            f"• 🎮 Access to exclusive game modes\n\n"
            f"⭐━━━━━━━━━━━━━━━━━━━━━━━━━━⭐",
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(
            f"⭐━━━━━━━━━━━━━━━━━━━━━━━━━━⭐\n"
            f"        GET PREMIUM ACCESS\n"
            f"⭐━━━━━━━━━━━━━━━━━━━━━━━━━━⭐\n\n"
            f"🆓 Current: **Free Player**\n\n"
            f"✨ Premium Perks:\n"
            f"• ⭐ Premium badge in leaderboard\n"
            f"• 🎯 +5 bonus points per task\n"
            f"• 🔍 Extra scan uses (5 instead of 3)\n"
            f"• 📨 Extra anonymous messages (8 instead of 5)\n"
            f"• 🛡️ 2 shields per game instead of 1\n"
            f"• 🏆 Priority in score display\n"
            f"• 🎮 Exclusive game modes coming soon!\n\n"
            f"📩 Contact the bot owner to get Premium!\n\n"
            f"⭐━━━━━━━━━━━━━━━━━━━━━━━━━━⭐",
            parse_mode="Markdown",
            reply_markup=premium_keyboard()
        )
