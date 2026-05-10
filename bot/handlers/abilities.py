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


def _gid(game) -> str:
    return str(game["_id"])


async def kill_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    if not player or player["role"] != "imposter":
        await update.message.reply_text("🔴 Only the Impostor can kill!")
        return

    target_user, error = await resolve_target(update, context, db, context.args)
    if error:
        await update.message.reply_text(error)
        return
    if not target_user:
        await update.message.reply_text(
            "❌ Usage:\n"
            "• `/kill @username`\n"
            "• `/kill 123456789` _(user ID)_\n"
            "• Reply to their message and send `/kill`",
            parse_mode="Markdown"
        )
        return

    engine = GameEngine(db)
    result = await engine.process_kill(context.bot, game_id, chat.id, user.id, target_user["user_id"])

    if not result["success"]:
        if result.get("shielded"):
            target_mention = get_mention(target_user["user_id"],
                                         target_user.get("first_name") or target_user.get("username") or "Player")
            await update.message.reply_text(
                f"🛡️ *Kill blocked!* {target_mention}'s shield absorbed the attack!\n"
                "Their shield has been consumed.",
                parse_mode="Markdown"
            )
        else:
            await update.message.reply_text(f"❌ {result['reason']}")
        return

    await update.message.delete()
    await chat.send_message(result["announcement"], parse_mode="MarkdownV2")


async def vent_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

    await update.message.delete()
    await chat.send_message(
        f"🌀 *Vent Detected!*\n\n"
        f"Someone used the vent system!\n"
        f"📍 {from_room} → {to_room}\n\n"
        f"_Who could it be?_ 👀",
        parse_mode="Markdown"
    )

    user_data = await db.get_user(user.id)
    if user_data and user_data.get("chat_id"):
        await send_dm(
            context.bot, user_data["chat_id"],
            f"🌀 You vented from *{from_room}* to *{to_room}*.\nYou have an alibi — stay calm!"
        )


async def sabotage_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    if not player or player["role"] != "imposter":
        await update.message.reply_text("❌ Only Impostors can sabotage!")
        return

    cfg = await db.get_group_cfg(chat.id)
    sab_cd = cfg["sabotage_cooldown"]

    if player.get("last_sabotage"):
        try:
            last = datetime.fromisoformat(str(player["last_sabotage"]))
            diff = (datetime.now() - last).total_seconds() / 3600
            if diff < sab_cd:
                remaining = round(sab_cd - diff, 1)
                await update.message.reply_text(
                    f"⏰ Sabotage on cooldown! Wait *{remaining}h* more.", parse_mode="Markdown"
                )
                return
        except Exception:
            pass

    sab_type = get_random_sabotage()
    await db.update_player_field(game_id, user.id, "last_sabotage", datetime.now().isoformat())

    await update.message.delete()
    from bot.game.events import get_sabotage_challenge
    challenge = get_sabotage_challenge(sab_type)

    await chat.send_message(sabotage_msg(sab_type, challenge["time"]), parse_mode="Markdown")
    await chat.send_message(
        f"⚡ *Challenge:*\n{challenge['question']}\n\n⏰ You have {challenge['time']} seconds!",
        parse_mode="Markdown"
    )


async def scan_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
        await update.message.reply_text(error)
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
        target_mention = get_mention(target_user["user_id"],
                                     target_user.get("first_name") or target_user.get("username") or "Player")
        await update.message.reply_text(f"❌ {target_mention} is not in this game!", parse_mode="Markdown")
        return

    target_mention = get_mention(target_user["user_id"],
                                  target_user.get("first_name") or target_user.get("username") or "Player")

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


async def shield_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = context.bot_data["db"]
    user = update.effective_user
    chat = update.effective_chat

    game = await db.get_active_game(chat.id)
    if not game or game["status"] != "active":
        await update.message.reply_text("❌ No active game running!")
        return

    game_id = _gid(game)
    player = await db.get_player(game_id, user.id)
    if not player or player["role"] != "crewmate":
        await update.message.reply_text("❌ Only Crewmates can use shields!")
        return

    if player.get("shield_active"):
        await update.message.reply_text("🛡️ Your shield is already active!")
        return

    shields_used = player.get("shields_used") or 0
    max_shields = player.get("max_shields") or Config.SHIELD_USES
    if player.get("is_premium"):
        max_shields += 1

    if shields_used >= max_shields:
        await update.message.reply_text("❌ You've used all your shields for this game!")
        return

    await db.update_player_field(game_id, user.id, "shield_active", True)
    await db.update_player_field(game_id, user.id, "shields_used", shields_used + 1)

    await update.message.reply_text(
        f"🛡️ *Shield Activated!*\n\n"
        f"You're protected from the next kill attempt.\n"
        f"_{max_shields - shields_used - 1} shield(s) remaining._",
        parse_mode="Markdown"
    )


async def report_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = context.bot_data["db"]
    user = update.effective_user
    chat = update.effective_chat

    game = await db.get_active_game(chat.id)
    if not game or game["status"] != "active":
        await update.message.reply_text("❌ No active game running!")
        return

    game_id = _gid(game)
    player = await db.get_player(game_id, user.id)
    if not player or not player["is_alive"]:
        await update.message.reply_text("❌ Only alive players can report!")
        return

    cfg = await db.get_group_cfg(chat.id)
    max_mtg = cfg["max_meetings"]
    emergency_used = player.get("emergency_used") or 0

    if emergency_used >= max_mtg:
        await update.message.reply_text(
            f"❌ You've used all {max_mtg} emergency meetings!"
        )
        return

    await db.update_player_field(game_id, user.id, "emergency_used", emergency_used + 1)

    alive = await db.get_alive_players(game_id)
    next_phase = await db.get_next_phase(game_id)

    from bot.utils.keyboards import vote_keyboard
    kb = vote_keyboard(alive, game_id, next_phase)
    caller_mention = get_mention(user.id, get_display_name(user))

    await chat.send_message(
        f"🚨 *Emergency Meeting!*\n\n"
        f"📢 Called by {caller_mention}\n"
        f"👥 *{len(alive)}* players alive\n\n"
        f"Discuss who the Impostor is!\n"
        f"Use /vote @player, reply + /vote, or tap a button below.\n"
        f"⏰ Voting closes in 5 minutes!",
        parse_mode="Markdown",
        reply_markup=kb
    )


async def watch_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = context.bot_data["db"]
    user = update.effective_user
    chat = update.effective_chat

    game = await db.get_active_game(chat.id)
    if not game or game["status"] != "active":
        await update.message.reply_text("❌ No active game running!")
        return

    game_id = _gid(game)
    player = await db.get_player(game_id, user.id)
    if not player or player["role"] != "crewmate" or not player["is_alive"]:
        await update.message.reply_text("❌ Only alive crewmates can watch!")
        return

    target_user, error = await resolve_target(update, context, db, context.args)
    if error:
        await update.message.reply_text(error)
        return
    if not target_user:
        await update.message.reply_text(
            "❌ Usage:\n"
            "• `/watch @username`\n"
            "• `/watch 123456789` _(user ID)_\n"
            "• Reply to their message and send `/watch`",
            parse_mode="Markdown"
        )
        return

    await db.update_player_field(game_id, user.id, "watching_user", target_user["user_id"])

    target_mention = get_mention(target_user["user_id"],
                                  target_user.get("first_name") or target_user.get("username") or "Player")

    user_data = await db.get_user(user.id)
    if user_data and user_data.get("chat_id"):
        activities = [
            f"{target_mention} was seen near the Electrical room.",
            f"{target_mention} completed a task very quickly.",
            f"{target_mention} stood still for an unusual amount of time.",
            f"{target_mention} was spotted talking to another player privately.",
            f"{target_mention} moved away from a task suddenly.",
        ]
        await send_dm(
            context.bot, user_data["chat_id"],
            f"👁️ *Watch Report — {target_mention}*\n\n"
            f"{random.choice(activities)}\n\n"
            f"_You'll receive another update in 1 hour._"
        )

    await update.message.reply_text(
        f"👁️ You are now watching {target_mention}.\n"
        f"Check your DM for activity reports!",
        parse_mode="Markdown"
    )


async def anon_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = context.bot_data["db"]
    user = update.effective_user
    chat = update.effective_chat

    game = await db.get_active_game(chat.id)
    if not game or game["status"] != "active":
        await update.message.reply_text("❌ No active game running!")
        return

    game_id = _gid(game)
    player = await db.get_player(game_id, user.id)
    if not player or player["role"] != "imposter":
        await update.message.reply_text("❌ Only Impostors can send anonymous messages!")
        return

    if not player["is_alive"]:
        await update.message.reply_text("👻 Ghosts can't send anon messages!")
        return

    anon_uses = player.get("anon_uses", 0)
    if anon_uses <= 0:
        await update.message.reply_text("❌ No anonymous message uses left!")
        return

    if not context.args:
        await update.message.reply_text("❌ Usage: `/anon [your message]`", parse_mode="Markdown")
        return

    msg_text = " ".join(context.args)
    await db.update_player_field(game_id, user.id, "anon_uses", anon_uses - 1)

    await update.message.delete()
    await chat.send_message(
        f"📩 *Anonymous Message*\n\n"
        f"_{msg_text}_\n\n"
        f"_— Unknown_",
        parse_mode="Markdown"
    )


async def faketask_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = context.bot_data["db"]
    user = update.effective_user
    chat = update.effective_chat

    game = await db.get_active_game(chat.id)
    if not game or game["status"] != "active":
        await update.message.reply_text("❌ No active game running!")
        return

    game_id = _gid(game)
    player = await db.get_player(game_id, user.id)
    if not player or player["role"] != "imposter":
        await update.message.reply_text("❌ Only Impostors can fake tasks!")
        return

    if not player["is_alive"]:
        await update.message.reply_text("👻 Ghosts can't fake tasks!")
        return

    fake_tasks = [
        "fixed the wiring in Electrical",
        "uploaded data in Admin",
        "fueled the engines in Lower Engine",
        "calibrated the scanner in MedBay",
        "cleared the trash chute in Storage",
        "aligned the telescope in Navigation",
        "submitted scan in Security",
        "started the reactor in Reactor",
        "cleaned the O2 filter",
        "wiped down the cafeteria tables"
    ]

    fake_task = random.choice(fake_tasks)
    name = get_display_name(user)

    await update.message.delete()
    await chat.send_message(
        f"✅ *Task Complete!*\n\n"
        f"👷 *{name}* has {fake_task}!\n"
        f"_Task progress updated._",
        parse_mode="Markdown"
    )
