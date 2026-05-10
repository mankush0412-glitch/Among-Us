import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # ─── Core Bot Settings ─────────────────────────────────────
    BOT_TOKEN: str = os.environ.get("BOT_TOKEN", "")
    OWNER_ID: int = int(os.environ.get("OWNER_ID", "0"))
    OWNER_USERNAME: str = os.environ.get("OWNER_USERNAME", "")  # without @, used for premium contact button
    WEBHOOK_URL: str = os.environ.get("WEBHOOK_URL", "")
    SECRET_TOKEN: str = os.environ.get("SECRET_TOKEN", "")

    # ─── MongoDB ───────────────────────────────────────────────
    MONGODB_URI: str = os.environ.get("MONGODB_URI", "mongodb://localhost:27017")
    DB_NAME: str = os.environ.get("DB_NAME", "among_us_bot")

    # ─── Logging ───────────────────────────────────────────────
    LOG_LEVEL: str = os.environ.get("LOG_LEVEL", "INFO")

    # ─── Game Schedule (IST) ───────────────────────────────────
    GAME_START_HOUR: int = int(os.environ.get("GAME_START_HOUR", "9"))
    SCORE_INTERVAL_HOURS: int = int(os.environ.get("SCORE_INTERVAL_HOURS", "6"))
    VOTING_START_HOUR: int = int(os.environ.get("VOTING_START_HOUR", "19"))
    REVEAL_HOUR: int = int(os.environ.get("REVEAL_HOUR", "21"))
    TASK_INTERVAL_HOURS: int = int(os.environ.get("TASK_INTERVAL_HOURS", "2"))

    # ─── Game Rules ────────────────────────────────────────────
    MAX_IMPOSTERS: int = 2
    MAX_EMERGENCY_MEETINGS: int = 2
    SCAN_USES: int = 3
    SHIELD_USES: int = 1
    ANON_MESSAGES_PER_GAME: int = 5
    KILL_COOLDOWN_HOURS: int = 4
    SABOTAGE_COOLDOWN_HOURS: int = 3

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
    PING_URL: str = os.environ.get("PING_URL", "")  # set to your render URL for self-ping
