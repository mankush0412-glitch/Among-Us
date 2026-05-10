import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # ─── Core Bot Settings ─────────────────────────────────────
    BOT_TOKEN: str = os.environ.get("BOT_TOKEN", "")
    OWNER_ID: int = int(os.environ.get("OWNER_ID", "0"))
    OWNER_USERNAME: str = os.environ.get("OWNER_USERNAME", "")
    WEBHOOK_URL: str = os.environ.get("WEBHOOK_URL", "")
    SECRET_TOKEN: str = os.environ.get("SECRET_TOKEN", "")

    # ─── MongoDB ───────────────────────────────────────────────
    MONGODB_URI: str = os.environ.get("MONGODB_URI", "mongodb://localhost:27017")
    DB_NAME: str = os.environ.get("DB_NAME", "among_us_bot")

    # ─── Logging ───────────────────────────────────────────────
    LOG_LEVEL: str = os.environ.get("LOG_LEVEL", "INFO")

    # ─── Game Schedule (UTC hour of day) ───────────────────────
    GAME_START_HOUR: int = int(os.environ.get("GAME_START_HOUR", "9"))
    VOTING_START_HOUR: int = int(os.environ.get("VOTING_START_HOUR", "19"))
    REVEAL_HOUR: int = int(os.environ.get("REVEAL_HOUR", "21"))

    # ─── All interval timers are in MINUTES ────────────────────
    # Task interval: how often a task is posted (default 120 min = 2h)
    TASK_INTERVAL_MINUTES: int = int(os.environ.get("TASK_INTERVAL_MINUTES", "120"))

    # Kill cooldown between kills (default 240 min = 4h)
    KILL_COOLDOWN_MINUTES: int = int(os.environ.get("KILL_COOLDOWN_MINUTES", "240"))

    # Sabotage cooldown (default 180 min = 3h)
    SABOTAGE_COOLDOWN_MINUTES: int = int(os.environ.get("SABOTAGE_COOLDOWN_MINUTES", "180"))

    # Scoreboard post interval (default 360 min = 6h)
    SCORE_INTERVAL_MINUTES: int = int(os.environ.get("SCORE_INTERVAL_MINUTES", "360"))

    # ─── Game Rules ────────────────────────────────────────────
    MAX_IMPOSTERS: int = 2
    MAX_EMERGENCY_MEETINGS: int = 2
    SCAN_USES: int = 3
    SHIELD_USES: int = 1
    ANON_MESSAGES_PER_GAME: int = 5

    # ─── Points ────────────────────────────────────────────────
    POINTS_TASK_COMPLETE: int = 10
    POINTS_IMPOSTER_WIN: int = 30
    POINTS_CREW_WIN: int = 20
    POINTS_CORRECT_VOTE: int = 15
    POINTS_WRONG_VOTE: int = -5
    POINTS_FIRST_TASK: int = 5

    # ─── Badges ────────────────────────────────────────────────
    PREMIUM_BADGE: str = "⭐"
    OWNER_BADGE: str = "👑"
    IMPOSTER_BADGE: str = "🔴"
    CREWMATE_BADGE: str = "🟢"
    GHOST_BADGE: str = "👻"

    # ─── UptimeRobot keep-alive ────────────────────────────────
    PING_URL: str = os.environ.get("PING_URL", "")
