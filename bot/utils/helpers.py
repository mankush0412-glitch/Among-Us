import random
from datetime import datetime
from bot.config import Config


def is_owner(user_id: int) -> bool:
    return user_id == Config.OWNER_ID


def get_display_name(user) -> str:
    if hasattr(user, 'first_name'):
        return user.first_name or user.username or "Player"
    if isinstance(user, dict):
        return user.get("first_name") or user.get("username") or "Player"
    return "Player"


def get_mention(user_id: int, name: str) -> str:
    return f"[{name}](tg://user?id={user_id})"


def get_mention_from_player(player: dict) -> str:
    name = player.get("first_name") or player.get("username") or "Player"
    return get_mention(player["user_id"], name)


def calculate_imposters(player_count: int) -> int:
    if player_count <= 6:
        return 1
    elif player_count <= 12:
        return 2
    else:
        return min(3, player_count // 5)


def pick_imposters(players: list, count: int) -> list:
    return random.sample([p["user_id"] for p in players], min(count, len(players)))


def format_time(dt_str: str) -> str:
    try:
        dt = datetime.fromisoformat(dt_str)
        return dt.strftime("%d %b %Y, %I:%M %p")
    except Exception:
        return dt_str or "Unknown"


def get_random_room() -> str:
    rooms = [
        "🔧 Cafeteria", "⚡ Electrical", "🛠 MedBay", "🌿 O2 Room",
        "☢️ Reactor", "🔬 Laboratory", "📡 Communications",
        "🚀 Engine Room", "🛸 Navigation", "🔫 Weapons Bay",
        "💾 Admin Room", "🌊 Lower Engine", "🔐 Security",
        "🌌 Storage", "📦 Cargo Bay"
    ]
    return random.choice(rooms)


def get_random_sabotage() -> str:
    return random.choice(["power", "oxygen", "reactor", "comms", "lights"])


def truncate(text: str, length: int = 50) -> str:
    return text[:length] + "..." if len(text) > length else text


def safe_username(username: str) -> str:
    if username:
        return f"@{username}"
    return "Unknown"


def get_badge(user_id: int, is_premium: bool) -> str:
    if user_id == Config.OWNER_ID:
        return Config.OWNER_BADGE
    if is_premium:
        return Config.PREMIUM_BADGE
    return ""


async def send_dm(bot, chat_id: int, text: str, parse_mode: str = "Markdown"):
    try:
        await bot.send_message(chat_id=chat_id, text=text, parse_mode=parse_mode)
        return True
    except Exception:
        return False


def chunk_list(lst: list, size: int) -> list:
    return [lst[i:i+size] for i in range(0, len(lst), size)]


def time_until(hour: int) -> str:
    now = datetime.now()
    target = now.replace(hour=hour, minute=0, second=0, microsecond=0)
    if target < now:
        from datetime import timedelta
        target += timedelta(days=1)
    diff = target - now
    hours = int(diff.total_seconds() // 3600)
    minutes = int((diff.total_seconds() % 3600) // 60)
    return f"{hours}h {minutes}m"


async def resolve_target(update, context, db, args):
    """
    Resolve a target player from four sources (in priority order):
      1. A Telegram inline mention (text_mention entity) in the command message
      2. A reply to someone's message — works with no args
      3. A numeric user ID argument    — e.g. /kill 123456789
      4. A @username argument          — e.g. /kill @john or /kill john

    Returns (user_data_dict, error_message_str).
    Exactly one of the two will be None.
    When both are None the caller should show a usage hint.
    """
    # ── Priority 1: text_mention entity (Telegram inline mention) ──
    # When someone uses Telegram's native mention (e.g. tapping a name in
    # the member list), it creates a text_mention entity with the user object.
    if update.message and update.message.entities and not args:
        for entity in update.message.entities:
            # Skip the command entity itself (type="bot_command")
            if hasattr(entity, "type") and entity.type == "text_mention":
                if entity.user:
                    user_data = await db.get_user(entity.user.id)
                    if not user_data:
                        # Auto-register from entity info so the mention still works
                        return None, (
                            f"❌ [{entity.user.first_name}](tg://user?id={entity.user.id}) "
                            f"hasn't registered with the bot yet!"
                        )
                    return user_data, None

    # ── Priority 2: replied-to message (only when no explicit arg given) ──
    reply = getattr(update.message, "reply_to_message", None)
    if reply and not args:
        replied_user = reply.from_user
        if not replied_user:
            return None, "❌ Could not get user info from that message!"
        user_data = await db.get_user(replied_user.id)
        if not user_data:
            return None, "❌ That user hasn't registered with the bot yet!"
        return user_data, None

    # ── Priority 3: explicit argument ────────────────────────────────────
    if args:
        arg = args[0].lstrip("@")

        if arg.isdigit():
            user_data = await db.get_user_by_id(int(arg))
            if not user_data:
                return None, f"❌ No registered player found with ID `{arg}`!"
            return user_data, None

        user_data = await db.get_user_by_username(arg)
        if not user_data:
            return None, f"❌ Player @{arg} not found!"
        return user_data, None

    # ── No target given ───────────────────────────────────────────────────
    return None, None
