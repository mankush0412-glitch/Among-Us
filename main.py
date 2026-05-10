import os
import asyncio
import logging
import datetime
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import JSONResponse

from telegram import Update, BotCommand, BotCommandScopeAllGroupChats, BotCommandScopeAllPrivateChats
from telegram.ext import Application

from bot.config import Config
from bot.handlers import register_handlers
from bot.game.scheduler import setup_scheduler
from bot.database import Database

logging.basicConfig(
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    level=getattr(logging, Config.LOG_LEVEL, logging.INFO)
)
logger = logging.getLogger(__name__)

telegram_app: Application = None

PRIVATE_COMMANDS = [
    BotCommand("start",    "🚀 Start the bot & register"),
    BotCommand("register", "📝 Register your account"),
    BotCommand("help",     "❓ Show all commands"),
    BotCommand("mystats",  "📊 Your personal stats"),
    BotCommand("premium",  "⭐ Premium info & perks"),
]

GROUP_COMMANDS = [
    BotCommand("startgame",  "🎮 Start a new Among Us game"),
    BotCommand("joingame",   "🙋 Join the current game"),
    BotCommand("leavegame",  "🚪 Leave the game lobby"),
    BotCommand("status",     "📋 Current game status"),
    BotCommand("mytasks",    "📌 See your pending tasks"),
    BotCommand("settings",   "⚙️ [Admin] Configure game settings"),
    BotCommand("kill",       "🔪 [Impostor] Kill a crewmate"),
    BotCommand("vent",       "🌀 [Impostor] Use a vent"),
    BotCommand("sabotage",   "💥 [Impostor] Trigger sabotage"),
    BotCommand("faketask",   "🎭 [Impostor] Fake a task"),
    BotCommand("scan",       "🔍 [Crewmate] Scan a player"),
    BotCommand("shield",     "🛡 [Crewmate] Activate shield"),
    BotCommand("report",     "🚨 Report a dead body"),
    BotCommand("watch",      "👁 Watch a player secretly"),
    BotCommand("anon",       "📨 Send anonymous message"),
    BotCommand("meeting",    "🔔 Call emergency meeting"),
    BotCommand("vote",       "🗳 Vote to eject a player"),
    BotCommand("addtask",    "➕ [Admin] Add custom task"),
    BotCommand("listtasks",  "📋 [Admin] List custom tasks"),
    BotCommand("deltask",    "🗑 [Admin] Delete custom task"),
    BotCommand("kickplayer", "👢 [Admin] Kick a player"),
    BotCommand("pingall",    "📣 [Admin] Ping all players"),
    BotCommand("endgame",    "🛑 [Admin] End the game"),
]


async def keep_alive():
    await asyncio.sleep(60)
    while True:
        try:
            await telegram_app.bot.get_me()
            logger.info("✅ Keep-alive ping sent to Telegram API")
        except Exception as e:
            logger.warning(f"⚠️ Keep-alive ping failed: {e}")
        await asyncio.sleep(270)


@asynccontextmanager
async def lifespan(app_instance: FastAPI):
    global telegram_app

    required = {"BOT_TOKEN": Config.BOT_TOKEN, "MONGODB_URI": Config.MONGODB_URI}
    for k, v in required.items():
        if not v:
            logger.critical(f"❌ Missing required env var: {k}")
            raise RuntimeError(f"Missing required environment variable: {k}")

    db = Database()
    await db.initialize()

    telegram_app = Application.builder().token(Config.BOT_TOKEN).build()
    telegram_app.bot_data["db"] = db

    register_handlers(telegram_app)
    await setup_scheduler(telegram_app)
    await telegram_app.initialize()
    await telegram_app.start()

    try:
        await telegram_app.bot.set_my_commands(PRIVATE_COMMANDS, scope=BotCommandScopeAllPrivateChats())
        await telegram_app.bot.set_my_commands(GROUP_COMMANDS, scope=BotCommandScopeAllGroupChats())
        logger.info("✅ Bot command menus set")
    except Exception as e:
        logger.warning(f"Could not set commands: {e}")

    render_url = os.environ.get("RENDER_EXTERNAL_URL", Config.WEBHOOK_URL).rstrip("/")
    if render_url:
        webhook_url = f"{render_url}/webhook/{Config.BOT_TOKEN}"
        try:
            await telegram_app.bot.set_webhook(
                url=webhook_url,
                allowed_updates=Update.ALL_TYPES,
                drop_pending_updates=True,
                secret_token=Config.SECRET_TOKEN or None
            )
            logger.info(f"✅ Webhook set: {webhook_url}")
        except Exception as e:
            logger.error(f"❌ Webhook error: {e}")
    else:
        logger.warning("⚠️ No RENDER_EXTERNAL_URL or WEBHOOK_URL set!")

    try:
        bot_info = await telegram_app.bot.get_me()
        logger.info(f"✅ Bot running: @{bot_info.username}")
    except Exception as e:
        logger.error(f"❌ get_me failed: {e}")

    ping_task = asyncio.create_task(keep_alive())
    logger.info("✅ Keep-alive task started")

    yield

    ping_task.cancel()
    logger.info("🛑 Shutting down bot...")
    try:
        await telegram_app.stop()
        await telegram_app.shutdown()
        await db.close()
    except Exception as e:
        logger.error(f"Shutdown error: {e}")
    logger.info("✅ Bot stopped cleanly")


app = FastAPI(lifespan=lifespan)


@app.post("/webhook/{token}")
async def telegram_webhook(request: Request, token: str):
    if token != Config.BOT_TOKEN:
        raise HTTPException(status_code=403, detail="Unauthorized")

    if Config.SECRET_TOKEN:
        header_token = request.headers.get("X-Telegram-Bot-Api-Secret-Token", "")
        if header_token != Config.SECRET_TOKEN:
            raise HTTPException(status_code=403, detail="Forbidden")

    update_data = await request.json()
    update = Update.de_json(update_data, telegram_app.bot)
    await telegram_app.process_update(update)
    return Response(status_code=200)


@app.get("/health")
async def health():
    return JSONResponse({
        "status": "ok",
        "bot": "Among Us Telegram Bot",
        "version": "2.0.0",
        "db": "MongoDB",
        "time": datetime.datetime.now().isoformat()
    })


@app.get("/ping")
@app.head("/ping")
async def ping():
    return JSONResponse({"status": "alive", "bot": "Among Us Bot"})


@app.get("/")
async def root():
    return JSONResponse({
        "name": "Among Us Telegram Bot 🎮",
        "status": "🟢 running",
        "uptime": "24/7 (Render free + UptimeRobot + Telegram ping)",
        "endpoints": ["/health", "/ping", "/webhook/<token>"],
        "time": datetime.datetime.now().isoformat()
    })


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, log_level="info")
