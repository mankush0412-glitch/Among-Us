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
