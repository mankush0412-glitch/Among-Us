from telegram import Update
from telegram.ext import ContextTypes
from bot.game.engine import GameEngine
from bot.utils.helpers import get_display_name, send_dm, get_random_room, get_random_sabotage
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
        await update.message.reply_text("❌ Use in a group!")
        return

    if not context.args:
        await update.message.reply_text("❌ Usage: /kill @username")
        return

    game = await db.get_active_game(chat.id)
    if not game or game["status"] != "active":
        await update.message.reply_text("❌ No active game!")
        return

    game_id = _gid(game)
    player = await db.get_player(game_id, user.id)
    if not player or player["role"] != "imposter":
        await update.message.reply_text("🔴 Only the Impostor can use /kill!")
        return

    target_username = context.args[0].lstrip("@")
    target_user = await db.get_user_by_username(target_username)

    if not target_user:
        await update.message.reply_text(f"❌ Player @{target_username} not found!")
        return

    engine = GameEngine(db)
    result = await engine.process_kill(
        context.bot, game_id, chat.id, user.id, target_user["user_id"]
    )

    if not result["success"]:
        if result.get("shielded"):
            await update.message.reply_text(
                f"🛡️ **BLOCKED!** Your kill on @{target_username} was deflected by a shield!\n"
                "Their shield has been consumed.",
                parse_mode="Markdown"
            )
        else:
            await update.message.reply_text(f"❌ {result['reason']}")
        return

    await update.message.delete()
    await chat.send_message(result["announcement"], parse_mode="Markdown")


async def vent_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = context.bot_data["db"]
    user = update.effective_user
    chat = update.effective_chat

    if chat.type == "private":
        await update.message.reply_text("❌ Use in a group!")
        return

    game = await db.get_active_game(chat.id)
    if not game or game["status"] != "active":
        await update.message.reply_text("❌ No active game!")
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
        f"🌀 **VENT DETECTED!**\n\n"
        f"Someone used the vent system!\n"
        f"📍 From: {from_room}\n"
        f"📍 To: {to_room}\n\n"
        f"_Who could it be?_ 👀",
        parse_mode="Markdown"
    )

    user_data = await db.get_user(user.id)
    if user_data and user_data.get("chat_id"):
        await send_dm(
            context.bot, user_data["chat_id"],
            f"🌀 You vented from {from_room} to {to_room}. You have an alibi! Stay calm."
        )


async def sabotage_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = context.bot_data["db"]
    user = update.effective_user
    chat = update.effective_chat

    if chat.type == "private":
        await update.message.reply_text("❌ Use in a group!")
        return

    game = await db.get_active_game(chat.id)
    if not game or game["status"] != "active":
        await update.message.reply_text("❌ No active game!")
        return

    game_id = _gid(game)
    player = await db.get_player(game_id, user.id)
    if not player or player["role"] != "imposter":
        await update.message.reply_text("❌ Only Impostors can sabotage!")
        return

    if player.get("last_sabotage"):
        last = datetime.fromisoformat(player["last_sabotage"])
        diff = (datetime.now() - last).total_seconds() / 3600
        if diff < Config.SABOTAGE_COOLDOWN_HOURS:
            remaining = round(Config.SABOTAGE_COOLDOWN_HOURS - diff, 1)
            await update.message.reply_text(f"⏰ Sabotage on cooldown! Wait {remaining}h more.")
            return

    sab_type = get_random_sabotage()
    await db.update_player_field(game_id, user.id, "last_sabotage", datetime.now().isoformat())

    await update.message.delete()
    from bot.game.events import get_sabotage_challenge
    challenge = get_sabotage_challenge(sab_type)

    await chat.send_message(sabotage_msg(sab_type, challenge["time"]), parse_mode="Markdown")
    await chat.send_message(
        f"⚡ **CHALLENGE:**\n{challenge['question']}\n\n⏰ You have {challenge['time']} seconds!",
        parse_mode="Markdown"
    )


async def scan_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = context.bot_data["db"]
    user = update.effective_user
    chat = update.effective_chat

    if chat.type == "private":
        await update.message.reply_text("❌ Use in a group!")
        return

    game = await db.get_active_game(chat.id)
    if not game or game["status"] != "active":
        await update.message.reply_text("❌ No active game!")
        return

    game_id = _gid(game)
    player = await db.get_player(game_id, user.id)
    if not player or player["role"] != "crewmate":
        await update.message.reply_text("❌ Only Crewmates can scan!")
        return

    if not player["is_alive"]:
        await update.message.reply_text("👻 Ghosts can't scan!")
        return

    scan_uses = player.get("scan_uses", Config.SCAN_USES)
    if scan_uses <= 0:
        await update.message.reply_text("❌ No scan uses left!")
        return

    if not context.args:
        await update.message.reply_text("❌ Usage: /scan @username")
        return

    target_username = context.args[0].lstrip("@")
    target_user = await db.get_user_by_username(target_username)
    if not target_user:
        await update.message.reply_text(f"❌ Player @{target_username} not found!")
        return

    target_player = await db.get_player(game_id, target_user["user_id"])
    if not target_player:
        await update.message.reply_text(f"❌ @{target_username} is not in this game!")
        return

    await db.update_player_field(game_id, user.id, "scan_uses", scan_uses - 1)

    hints_sus = [
        f"🔴 **Scan Result:** @{target_username} was spotted near the vents...",
        f"🔴 **Scan Result:** @{target_username} completed a task 3x faster than possible.",
        f"🔴 **Scan Result:** @{target_username}'s biometrics show elevated stress levels.",
        f"🔴 **Scan Result:** @{target_username} was in a room with no task assigned to them.",
    ]
    hints_clear = [
        f"🟢 **Scan Result:** @{target_username} appears to be working diligently on tasks.",
        f"🟢 **Scan Result:** @{target_username}'s activity log is consistent with a crewmate.",
        f"🟢 **Scan Result:** @{target_username} was spotted completing the MedBay scan.",
        f"🟢 **Scan Result:** @{target_username} shows no signs of deception.",
    ]

    is_imposter = target_player["role"] == "imposter"
    if is_imposter:
        hint = random.choice(hints_sus) if random.random() < 0.7 else random.choice(hints_clear)
    else:
        hint = random.choice(hints_clear) if random.random() < 0.7 else random.choice(hints_sus)

    await update.message.reply_text(
        f"🔍 **SCAN RESULT** (uses left: {scan_uses - 1})\n\n{hint}\n\n_Note: Scans are not 100% accurate._",
        parse_mode="Markdown"
    )


async def shield_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = context.bot_data["db"]
    user = update.effective_user
    chat = update.effective_chat

    game = await db.get_active_game(chat.id)
    if not game or game["status"] != "active":
        await update.message.reply_text("❌ No active game!")
        return

    game_id = _gid(game)
    player = await db.get_player(game_id, user.id)
    if not player or player["role"] != "crewmate":
        await update.message.reply_text("❌ Only Crewmates can shield!")
        return

    if player.get("shield_active"):
        await update.message.reply_text("🛡️ Shield is already active!")
        return

    shields_used = player.get("shields_used") or 0
    if shields_used >= Config.SHIELD_USES:
        await update.message.reply_text("❌ You've used all your shields!")
        return

    await db.update_player_field(game_id, user.id, "shield_active", True)
    await db.update_player_field(game_id, user.id, "shields_used", shields_used + 1)

    await update.message.reply_text(
        "🛡️ **Shield Activated!**\n\nYou're protected from the next kill attempt.\n"
        "_Your shield will be consumed when hit._",
        parse_mode="Markdown"
    )


async def report_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = context.bot_data["db"]
    user = update.effective_user
    chat = update.effective_chat

    game = await db.get_active_game(chat.id)
    if not game or game["status"] != "active":
        await update.message.reply_text("❌ No active game!")
        return

    game_id = _gid(game)
    player = await db.get_player(game_id, user.id)
    if not player or not player["is_alive"]:
        await update.message.reply_text("❌ Only alive players can report!")
        return

    emergency_used = player.get("emergency_used") or 0
    if emergency_used >= Config.MAX_EMERGENCY_MEETINGS:
        await update.message.reply_text(
            f"❌ You've used all {Config.MAX_EMERGENCY_MEETINGS} emergency meetings!"
        )
        return

    await db.update_player_field(game_id, user.id, "emergency_used", emergency_used + 1)

    alive = await db.get_alive_players(game_id)
    next_phase = await db.get_next_phase(game_id)

    from bot.utils.keyboards import vote_keyboard
    kb = vote_keyboard(alive, game_id, next_phase)
    name = get_display_name(user)
    await chat.send_message(
        f"🚨━━━━━━━━━━━━━━━━━━━━━━━━━━🚨\n"
        f"   ⚠️ EMERGENCY MEETING ⚠️\n"
        f"🚨━━━━━━━━━━━━━━━━━━━━━━━━━━🚨\n\n"
        f"📢 Called by: **{name}**\n\n"
        f"🔍 Discuss who the Impostor is!\n"
        f"Use /vote @player or buttons below!\n\n"
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
        await update.message.reply_text("❌ No active game!")
        return

    game_id = _gid(game)
    player = await db.get_player(game_id, user.id)
    if not player or player["role"] != "crewmate" or not player["is_alive"]:
        await update.message.reply_text("❌ Only alive crewmates can watch!")
        return

    if not context.args:
        await update.message.reply_text("❌ Usage: /watch @username")
        return

    target_username = context.args[0].lstrip("@")
    target_user = await db.get_user_by_username(target_username)
    if not target_user:
        await update.message.reply_text(f"❌ @{target_username} not found!")
        return

    await db.update_player_field(game_id, user.id, "watching_user", target_user["user_id"])

    user_data = await db.get_user(user.id)
    if user_data and user_data.get("chat_id"):
        target_player = await db.get_player(game_id, target_user["user_id"])
        if target_player:
            activities = [
                f"@{target_username} was seen near the Electrical room.",
                f"@{target_username} completed a task very quickly.",
                f"@{target_username} stood still for an unusual amount of time.",
                f"@{target_username} was spotted talking to another player privately.",
                f"@{target_username} moved away from a task suddenly.",
            ]
            await send_dm(
                context.bot, user_data["chat_id"],
                f"👁️ **WATCH REPORT on @{target_username}:**\n\n"
                f"{random.choice(activities)}\n\n"
                f"_You'll receive another update in 1 hour._"
            )

    await update.message.reply_text(
        f"👁️ You are now watching **@{target_username}**.\n"
        f"Check your DM for activity reports!",
        parse_mode="Markdown"
    )


async def anon_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = context.bot_data["db"]
    user = update.effective_user
    chat = update.effective_chat

    game = await db.get_active_game(chat.id)
    if not game or game["status"] != "active":
        await update.message.reply_text("❌ No active game!")
        return

    game_id = _gid(game)
    player = await db.get_player(game_id, user.id)
    if not player or player["role"] != "imposter":
        await update.message.reply_text("❌ Only Impostors can send anonymous messages!")
        return

    if not player["is_alive"]:
        await update.message.reply_text("👻 Ghosts can't send anon messages!")
        return

    anon_uses = player.get("anon_uses", Config.ANON_MESSAGES_PER_GAME)
    if anon_uses <= 0:
        await update.message.reply_text("❌ No anonymous message uses left!")
        return

    if not context.args:
        await update.message.reply_text("❌ Usage: /anon [your message]")
        return

    msg_text = " ".join(context.args)
    await db.update_player_field(game_id, user.id, "anon_uses", anon_uses - 1)

    await update.message.delete()
    await chat.send_message(
        f"👤━━━━━━━━━━━━━━━━━━━━━━━━━━👤\n"
        f"      📩 ANONYMOUS MESSAGE\n"
        f"👤━━━━━━━━━━━━━━━━━━━━━━━━━━👤\n\n"
        f"_{msg_text}_\n\n"
        f"👤━━━━━━━━━━━━━━━━━━━━━━━━━━👤",
        parse_mode="Markdown"
    )


async def faketask_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = context.bot_data["db"]
    user = update.effective_user
    chat = update.effective_chat

    game = await db.get_active_game(chat.id)
    if not game or game["status"] != "active":
        await update.message.reply_text("❌ No active game!")
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
        f"✅ **Task Complete!**\n\n"
        f"👷 **{name}** has {fake_task}!\n"
        f"_Task progress updated._",
        parse_mode="Markdown"
    )
