from telegram import Update
from telegram.ext import ContextTypes
from bot.game.engine import GameEngine
from bot.utils.helpers import (
    get_display_name, send_dm, get_random_room, get_random_sabotage,
    resolve_target, get_mention, get_mention_from_player
)
from bot.utils.messages import sabotage_msg
from bot.config import Config
from datetime import datetime
import random
import logging

logger = logging.getLogger(__name__)


def _gid(game) -> str:
    return str(game["_id"])


def _fmt_minutes(minutes: int) -> str:
    if minutes < 60:
        return f"{minutes} min"
    hours, mins = divmod(int(minutes), 60)
    return f"{hours}h {mins}m" if mins else f"{hours}h"


async def _get_game_and_player(db, user_id: int, chat_type: str, chat_id: int):
    """
    Resolve the active game and player for either a group or DM context.
    - Group chat: look up active game in this group.
    - Private chat: find any active game the user is in.
    Returns (game, game_id, group_id, player) or (None, None, None, None).
    """
    if chat_type == "private":
        game, group_id = await db.get_active_game_for_user(user_id)
    else:
        game = await db.get_active_game(chat_id)
        group_id = chat_id if game else None

    if not game:
        return None, None, None, None

    game_id = _gid(game)
    group_id = group_id or game.get("group_id")
    player = await db.get_player(game_id, user_id)
    return game, game_id, group_id, player


# ─────────────────────────────────────────────────────────────────────────────
# KILL
# ─────────────────────────────────────────────────────────────────────────────
async def kill_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = context.bot_data["db"]
    user = update.effective_user
    chat = update.effective_chat

    game, game_id, group_id, player = await _get_game_and_player(
        db, user.id, chat.type, chat.id
    )

    if not game:
        if chat.type == "private":
            await update.message.reply_text(
                "❌ You're not in any active game!\n"
                "Join a game in your group first."
            )
        else:
            await update.message.reply_text("❌ No active game running!")
        return

    if not player or player["role"] != "imposter":
        await update.message.reply_text("🔴 Only the Impostor can kill!")
        return

    if not player["is_alive"]:
        await update.message.reply_text("👻 Ghosts can't kill!")
        return

    target_user, error = await resolve_target(update, context, db, context.args)
    if error:
        await update.message.reply_text(error, parse_mode="Markdown")
        return
    if not target_user:
        await update.message.reply_text(
            "❌ Usage:\n"
            "• `/kill @username`\n"
            "• `/kill 123456789` _(user ID)_\n"
            "• Reply to their message and send `/kill`\n\n"
            "💡 _DM me this command to use it secretly!_",
            parse_mode="Markdown"
        )
        return

    engine = GameEngine(db)
    result = await engine.process_kill(
        context.bot, game_id, group_id, user.id, target_user["user_id"]
    )

    if not result["success"]:
        if result.get("shielded"):
            target_mention = get_mention(
                target_user["user_id"],
                target_user.get("first_name") or target_user.get("username") or "Player"
            )
            await update.message.reply_text(
                f"🛡️ *Kill blocked!* {target_mention}'s shield absorbed the attack!\n"
                "Their shield has been consumed.",
                parse_mode="Markdown"
            )
        else:
            await update.message.reply_text(f"❌ {result['reason']}")
        return

    # Delete command in group; in DM just confirm quietly
    if chat.type != "private":
        try:
            await update.message.delete()
        except Exception:
            pass
    else:
        await update.message.reply_text(
            "✅ *Kill executed!* Announcement sent to the group.",
            parse_mode="Markdown"
        )

    # Announce anonymously in the group
    await context.bot.send_message(
        chat_id=group_id,
        text=result["announcement"],
        parse_mode="MarkdownV2"
    )


# ─────────────────────────────────────────────────────────────────────────────
# VENT
# ─────────────────────────────────────────────────────────────────────────────
async def vent_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = context.bot_data["db"]
    user = update.effective_user
    chat = update.effective_chat

    game, game_id, group_id, player = await _get_game_and_player(
        db, user.id, chat.type, chat.id
    )

    if not game:
        if chat.type == "private":
            await update.message.reply_text("❌ You're not in any active game!")
        else:
            await update.message.reply_text("❌ No active game running!")
        return

    if not player or player["role"] != "imposter":
        await update.message.reply_text("❌ Only Impostors can use vents!")
        return

    if not player["is_alive"]:
        await update.message.reply_text("👻 Ghosts don't need vents!")
        return

    from_room = get_random_room()
    to_room = get_random_room()
    while to_room == from_room:
        to_room = get_random_room()

    if chat.type != "private":
        try:
            await update.message.delete()
        except Exception:
            pass
    else:
        await update.message.reply_text(
            "🌀 *Vent used!* Announcement sent to the group.",
            parse_mode="Markdown"
        )

    await context.bot.send_message(
        chat_id=group_id,
        text=(
            f"🌀 *Vent Detected!*\n\n"
            f"Someone used the vent system!\n"
            f"📍 {from_room} → {to_room}\n\n"
            f"_Who could it be?_ 👀"
        ),
        parse_mode="Markdown"
    )

    user_data = await db.get_user(user.id)
    if user_data and user_data.get("chat_id"):
        await send_dm(
            context.bot, user_data["chat_id"],
            f"🌀 You vented from *{from_room}* to *{to_room}*.\nYou have an alibi — stay calm!"
        )


# ─────────────────────────────────────────────────────────────────────────────
# SABOTAGE
# ─────────────────────────────────────────────────────────────────────────────
async def sabotage_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = context.bot_data["db"]
    user = update.effective_user
    chat = update.effective_chat

    game, game_id, group_id, player = await _get_game_and_player(
        db, user.id, chat.type, chat.id
    )

    if not game:
        if chat.type == "private":
            await update.message.reply_text("❌ You're not in any active game!")
        else:
            await update.message.reply_text("❌ No active game running!")
        return

    if not player or player["role"] != "imposter":
        await update.message.reply_text("❌ Only Impostors can sabotage!")
        return

    cfg = await db.get_group_cfg(group_id)
    # sabotage_cooldown is now in MINUTES
    sab_cd_minutes = cfg["sabotage_cooldown"]

    if player.get("last_sabotage"):
        try:
            last = datetime.fromisoformat(str(player["last_sabotage"]))
            diff_minutes = (datetime.now() - last).total_seconds() / 60
            if diff_minutes < sab_cd_minutes:
                remaining = int(sab_cd_minutes - diff_minutes)
                await update.message.reply_text(
                    f"⏰ Sabotage on cooldown! Wait *{_fmt_minutes(remaining)}* more.",
                    parse_mode="Markdown"
                )
                return
        except Exception:
            pass

    sab_type = get_random_sabotage()
    await db.update_player_field(game_id, user.id, "last_sabotage", datetime.now().isoformat())

    if chat.type != "private":
        try:
            await update.message.delete()
        except Exception:
            pass
    else:
        await update.message.reply_text(
            "💥 *Sabotage triggered!* Announcement sent to the group.",
            parse_mode="Markdown"
        )

    from bot.game.events import get_sabotage_challenge
    challenge = get_sabotage_challenge(sab_type)

    await context.bot.send_message(
        chat_id=group_id,
        text=sabotage_msg(sab_type, challenge["time"]),
        parse_mode="Markdown"
    )
    await context.bot.send_message(
        chat_id=group_id,
        text=f"⚡ *Challenge:*\n{challenge['question']}\n\n⏰ You have {challenge['time']} seconds!",
        parse_mode="Markdown"
    )


# ─────────────────────────────────────────────────────────────────────────────
# ANON MESSAGE
# ─────────────────────────────────────────────────────────────────────────────
async def anon_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = context.bot_data["db"]
    user = update.effective_user
    chat = update.effective_chat

    game, game_id, group_id, player = await _get_game_and_player(
        db, user.id, chat.type, chat.id
    )

    if not game:
        if chat.type == "private":
            await update.message.reply_text("❌ You're not in any active game!")
        else:
            await update.message.reply_text("❌ No active game running!")
        return

    if not player or player["role"] != "imposter" or not player["is_alive"]:
        await update.message.reply_text("❌ Only alive Impostors can send anonymous messages!")
        return

    anon_uses = player.get("anon_uses", 0)
    if anon_uses <= 0:
        await update.message.reply_text("❌ No anonymous message uses left!")
        return

    if not context.args:
        await update.message.reply_text(
            "❌ Usage: `/anon your message here`",
            parse_mode="Markdown"
        )
        return

    msg_text = " ".join(context.args)
    await db.update_player_field(game_id, user.id, "anon_uses", anon_uses - 1)

    if chat.type != "private":
        try:
            await update.message.delete()
        except Exception:
            pass
    else:
        await update.message.reply_text(
            f"📨 *Anonymous message sent!* ({anon_uses - 1} uses left)",
            parse_mode="Markdown"
        )

    await context.bot.send_message(
        chat_id=group_id,
        text=f"📨 *Anonymous Message:*\n\n_{msg_text}_",
        parse_mode="Markdown"
    )


# ─────────────────────────────────────────────────────────────────────────────
# FAKE TASK
# ─────────────────────────────────────────────────────────────────────────────
async def faketask_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = context.bot_data["db"]
    user = update.effective_user
    chat = update.effective_chat

    game, game_id, group_id, player = await _get_game_and_player(
        db, user.id, chat.type, chat.id
    )

    if not game:
        if chat.type == "private":
            await update.message.reply_text("❌ You're not in any active game!")
        else:
            await update.message.reply_text("❌ No active game running!")
        return

    if not player or player["role"] != "imposter" or not player["is_alive"]:
        await update.message.reply_text("❌ Only alive Impostors can fake tasks!")
        return

    fake_tasks = [
        "Fix wiring", "Empty garbage", "Swipe card",
        "Submit scan", "Fuel engines", "Clean O2 filter",
        "Upload data", "Inspect sample", "Start reactor", "Chart course"
    ]
    fake_task = random.choice(fake_tasks)
    impostor_name = get_display_name(user)

    if chat.type != "private":
        try:
            await update.message.delete()
        except Exception:
            pass
    else:
        await update.message.reply_text(
            "🎭 *Fake task announced!* Other players can see it.",
            parse_mode="Markdown"
        )

    await context.bot.send_message(
        chat_id=group_id,
        text=(
            f"📋 *Task Complete!*\n\n"
            f"*{impostor_name}* just finished: _{fake_task}_\n"
            f"💎 +10 pts"
        ),
        parse_mode="Markdown"
    )


# ─────────────────────────────────────────────────────────────────────────────
# SCAN (Crewmate only — group only)
# ─────────────────────────────────────────────────────────────────────────────
async def scan_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = context.bot_data["db"]
    user = update.effective_user
    chat = update.effective_chat

    if chat.type == "private":
        await update.message.reply_text("❌ Use /scan in the group chat!")
        return

    game = await db.get_active_game(chat.id)
    if not game or game["status"] != "active":
        await update.message.reply_text("❌ No active game running!")
        return

    game_id = _gid(game)
    player = await db.get_player(game_id, user.id)
    if not player or player["role"] != "crewmate":
        await update.message.reply_text("❌ Only Crewmates can scan!")
        return

    if not player["is_alive"]:
        await update.message.reply_text("👻 Ghosts can't scan!")
        return

    scan_uses = player.get("scan_uses", 0)
    if scan_uses <= 0:
        await update.message.reply_text("❌ You have no scan uses left!")
        return

    target_user, error = await resolve_target(update, context, db, context.args)
    if error:
        await update.message.reply_text(error, parse_mode="Markdown")
        return
    if not target_user:
        await update.message.reply_text(
            "❌ Usage:\n"
            "• `/scan @username`\n"
            "• `/scan 123456789` _(user ID)_\n"
            "• Reply to their message and send `/scan`",
            parse_mode="Markdown"
        )
        return

    target_player = await db.get_player(game_id, target_user["user_id"])
    if not target_player:
        target_mention = get_mention(
            target_user["user_id"],
            target_user.get("first_name") or target_user.get("username") or "Player"
        )
        await update.message.reply_text(
            f"❌ {target_mention} is not in this game!", parse_mode="Markdown"
        )
        return

    target_mention = get_mention(
        target_user["user_id"],
        target_user.get("first_name") or target_user.get("username") or "Player"
    )
    await db.update_player_field(game_id, user.id, "scan_uses", scan_uses - 1)

    hints_sus = [
        f"🔴 {target_mention} was spotted near the vents...",
        f"🔴 {target_mention} completed a task 3x faster than possible.",
        f"🔴 {target_mention}'s biometrics show elevated stress levels.",
        f"🔴 {target_mention} was in a room with no assigned task.",
    ]
    hints_clear = [
        f"🟢 {target_mention} appears to be working diligently on tasks.",
        f"🟢 {target_mention}'s activity log is consistent with a crewmate.",
        f"🟢 {target_mention} was spotted completing the MedBay scan.",
        f"🟢 {target_mention} shows no signs of deception.",
    ]

    is_imposter = target_player["role"] == "imposter"
    if is_imposter:
        hint = random.choice(hints_sus) if random.random() < 0.7 else random.choice(hints_clear)
    else:
        hint = random.choice(hints_clear) if random.random() < 0.7 else random.choice(hints_sus)

    await update.message.reply_text(
        f"🔍 *Scan Result* · {scan_uses - 1} uses left\n\n"
        f"{hint}\n\n"
        f"_Note: Scans are not 100% accurate._",
        parse_mode="Markdown"
    )


# ─────────────────────────────────────────────────────────────────────────────
# SHIELD (group only)
# ─────────────────────────────────────────────────────────────────────────────
async def shield_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = context.bot_data["db"]
    user = update.effective_user
    chat = update.effective_chat

    if chat.type == "private":
        await update.message.reply_text("❌ Use /shield in the group chat!")
        return

    game = await db.get_active_game(chat.id)
    if not game or game["status"] != "active":
        await update.message.reply_text("❌ No active game running!")
        return

    game_id = _gid(game)
    player = await db.get_player(game_id, user.id)
    if not player or player["role"] != "crewmate":
        await update.message.reply_text("❌ Only Crewmates can use shields!")
        return

    if not player["is_alive"]:
        await update.message.reply_text("👻 Ghosts can't use shields!")
        return

    if player.get("shield_active"):
        await update.message.reply_text("🛡 Your shield is already active!")
        return

    shields_used = player.get("shields_used", 0)
    max_shields = player.get("max_shields", Config.SHIELD_USES)

    if shields_used >= max_shields:
        await update.message.reply_text(
            f"❌ You've used all your shields! ({max_shields}/{max_shields})"
        )
        return

    await db.update_player_field(game_id, user.id, "shield_active", True)
    await db.update_player_field(game_id, user.id, "shields_used", shields_used + 1)

    remaining = max_shields - shields_used - 1
    user_mention = get_mention(user.id, get_display_name(user))
    await update.message.reply_text(
        f"🛡 *Shield Activated!*\n\n"
        f"{user_mention} is now protected from the next kill!\n"
        f"Shields remaining: {remaining}/{max_shields}",
        parse_mode="Markdown"
    )


# ─────────────────────────────────────────────────────────────────────────────
# REPORT (group only)
# ─────────────────────────────────────────────────────────────────────────────
async def report_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = context.bot_data["db"]
    user = update.effective_user
    chat = update.effective_chat

    if chat.type == "private":
        await update.message.reply_text("❌ Use /report in the group chat!")
        return

    game = await db.get_active_game(chat.id)
    if not game or game["status"] != "active":
        await update.message.reply_text("❌ No active game running!")
        return

    game_id = _gid(game)
    player = await db.get_player(game_id, user.id)
    if not player or not player["is_alive"]:
        await update.message.reply_text("❌ Only alive players can report bodies!")
        return

    from bot.utils.keyboards import vote_keyboard
    alive = await db.get_alive_players(game_id)
    next_phase = await db.get_next_phase(game_id)
    kb = vote_keyboard(alive, game_id, next_phase)
    caller_mention = get_mention(user.id, get_display_name(user))

    await db.update_game_status(game_id, "voting")
    await chat.send_message(
        f"🚨 *Body Reported!*\n\n"
        f"📢 {caller_mention} found a body!\n"
        f"👥 *{len(alive)}* players still alive\n\n"
        f"Tap a button to vote or use /vote @player",
        parse_mode="Markdown",
        reply_markup=kb
    )


# ─────────────────────────────────────────────────────────────────────────────
# WATCH (group only)
# ─────────────────────────────────────────────────────────────────────────────
async def watch_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = context.bot_data["db"]
    user = update.effective_user
    chat = update.effective_chat

    if chat.type == "private":
        await update.message.reply_text("❌ Use /watch in the group chat!")
        return

    game = await db.get_active_game(chat.id)
    if not game or game["status"] != "active":
        await update.message.reply_text("❌ No active game running!")
        return

    game_id = _gid(game)
    player = await db.get_player(game_id, user.id)
    if not player or player["role"] != "crewmate" or not player["is_alive"]:
        await update.message.reply_text("❌ Only alive Crewmates can watch!")
        return

    target_user, error = await resolve_target(update, context, db, context.args)
    if error:
        await update.message.reply_text(error, parse_mode="Markdown")
        return
    if not target_user:
        await update.message.reply_text(
            "❌ Usage: `/watch @username` or reply to their message",
            parse_mode="Markdown"
        )
        return

    target_player = await db.get_player(game_id, target_user["user_id"])
    if not target_player or not target_player["is_alive"]:
        await update.message.reply_text("❌ That player is not alive in this game!")
        return

    await db.update_player_field(game_id, user.id, "watching_user", target_user["user_id"])

    activities = [
        "heading towards the Reactor",
        "fixing wiring in Electrical",
        "uploading data in Admin",
        "checking O2 filters",
        "seen near a vent in Storage",
        "scanning in MedBay",
        "fueling engines",
        "charting a course in Navigation"
    ]
    activity = random.choice(activities)
    target_mention = get_mention(
        target_user["user_id"],
        target_user.get("first_name") or target_user.get("username") or "Player"
    )

    await update.message.reply_text(
        f"👁 *Watch Report*\n\n"
        f"{target_mention} was last seen *{activity}*.\n\n"
        f"_This is a snapshot — keep watching for more clues._",
        parse_mode="Markdown"
    )
