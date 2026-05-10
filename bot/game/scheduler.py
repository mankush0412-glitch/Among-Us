import logging
import random
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from bot.config import Config
from bot.utils.messages import scoreboard_msg, task_msg
from bot.utils.keyboards import scoreboard_keyboard, task_keyboard
from bot.game.events import get_ambient_message, get_random_event

logger = logging.getLogger(__name__)
scheduler = AsyncIOScheduler()


async def setup_scheduler(application):
    bot = application.bot
    db = application.bot_data["db"]

    scheduler.add_job(
        post_scoreboard,
        IntervalTrigger(hours=Config.SCORE_INTERVAL_HOURS),
        args=[bot, db],
        id="scoreboard",
        replace_existing=True
    )

    scheduler.add_job(
        post_daily_task,
        IntervalTrigger(hours=Config.TASK_INTERVAL_HOURS),
        args=[bot, db],
        id="daily_task",
        replace_existing=True
    )

    scheduler.add_job(
        start_voting_phase,
        CronTrigger(hour=Config.VOTING_START_HOUR, minute=0),
        args=[bot, db],
        id="voting",
        replace_existing=True
    )

    scheduler.add_job(
        reveal_phase,
        CronTrigger(hour=Config.REVEAL_HOUR, minute=0),
        args=[bot, db],
        id="reveal",
        replace_existing=True
    )

    scheduler.add_job(
        post_ambient_message,
        IntervalTrigger(hours=3),
        args=[bot, db],
        id="ambient",
        replace_existing=True
    )

    scheduler.add_job(
        random_event_trigger,
        IntervalTrigger(hours=5),
        args=[bot, db],
        id="random_event",
        replace_existing=True
    )

    scheduler.start()
    logger.info("✅ Scheduler started with all jobs")


def _gid(game) -> str:
    """Get game_id string from a MongoDB game document."""
    return str(game["_id"])


async def post_scoreboard(bot, db):
    groups = await db.get_all_groups()
    for group in groups:
        try:
            scores = await db.get_scores(group["group_id"], limit=10)
            if not scores:
                continue
            text = scoreboard_msg(list(scores), group.get("title") or "Group")
            kb = scoreboard_keyboard(group["group_id"])
            msg = await bot.send_message(
                chat_id=group["group_id"],
                text=text,
                parse_mode="Markdown",
                reply_markup=kb
            )
            try:
                await bot.pin_chat_message(
                    chat_id=group["group_id"],
                    message_id=msg.message_id,
                    disable_notification=True
                )
            except Exception:
                pass
        except Exception as e:
            logger.error(f"Scoreboard error for group {group['group_id']}: {e}")


async def post_daily_task(bot, db):
    from data.tasks_data import get_random_task
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup

    groups = await db.get_all_groups()
    for group in groups:
        try:
            game = await db.get_active_game(group["group_id"])
            if not game or game["status"] != "active":
                continue

            game_id = _gid(game)

            # Mix in custom tasks occasionally
            custom_tasks = await db.get_custom_tasks(group["group_id"])
            if custom_tasks and random.random() < 0.3:
                chosen = random.choice(custom_tasks)
                task_text = chosen["task_text"]
                category = "custom"
            else:
                task_data = get_random_task()
                task_text = task_data["text"]
                category = task_data["category"]

            num = (await db.get_task_count(game_id)) + 1
            text = task_msg(task_text, category, num)

            msg = await bot.send_message(
                chat_id=group["group_id"],
                text=text,
                parse_mode="Markdown"
            )

            task_id = await db.post_task(game_id, group["group_id"], task_text, category, msg.message_id)

            kb2 = InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ I Did This Task!", callback_data=f"task_done_{task_id}")]
            ])
            await msg.edit_reply_markup(reply_markup=kb2)

        except Exception as e:
            logger.error(f"Task post error for group {group['group_id']}: {e}")


async def start_voting_phase(bot, db):
    from bot.utils.messages import voting_msg
    from bot.utils.keyboards import vote_keyboard

    groups = await db.get_all_groups()
    for group in groups:
        try:
            game = await db.get_active_game(group["group_id"])
            if not game or game["status"] != "active":
                continue

            game_id = _gid(game)
            await db.update_game_status(game_id, "voting")
            alive = await db.get_alive_players(game_id)
            next_phase = await db.get_next_phase(game_id)

            text = voting_msg(next_phase)
            kb = vote_keyboard(alive, game_id, next_phase)

            await bot.send_message(
                chat_id=group["group_id"],
                text=text,
                parse_mode="Markdown",
                reply_markup=kb
            )
        except Exception as e:
            logger.error(f"Voting phase error for group {group['group_id']}: {e}")


async def reveal_phase(bot, db):
    from bot.game.engine import GameEngine

    engine = GameEngine(db)
    groups = await db.get_all_groups()

    for group in groups:
        try:
            game = await db.get_active_game(group["group_id"])
            if not game or game["status"] != "voting":
                continue

            game_id = _gid(game)
            current_phase = await db.get_current_phase(game_id)
            result = await engine.process_eject(bot, game_id, group["group_id"], current_phase)
            await bot.send_message(
                chat_id=group["group_id"],
                text=result["message"],
                parse_mode="Markdown"
            )
        except Exception as e:
            logger.error(f"Reveal error for group {group['group_id']}: {e}")


async def post_ambient_message(bot, db):
    groups = await db.get_all_groups()
    for group in groups:
        try:
            game = await db.get_active_game(group["group_id"])
            if not game or game["status"] != "active":
                continue
            msg = get_ambient_message()
            await bot.send_message(chat_id=group["group_id"], text=f"_{msg}_", parse_mode="Markdown")
        except Exception as e:
            logger.error(f"Ambient msg error for group {group['group_id']}: {e}")


async def random_event_trigger(bot, db):
    from bot.game.events import get_random_event, get_impostor_hint

    groups = await db.get_all_groups()
    for group in groups:
        try:
            game = await db.get_active_game(group["group_id"])
            if not game or game["status"] != "active":
                continue

            if random.random() < 0.4:
                event = get_random_event()
                await bot.send_message(
                    chat_id=group["group_id"],
                    text=f"🎲 **RANDOM EVENT!**\n\n{event['message']}",
                    parse_mode="Markdown"
                )
            elif random.random() < 0.3:
                hint = get_impostor_hint()
                await bot.send_message(
                    chat_id=group["group_id"],
                    text=f"🕵️ **SYSTEM ALERT:**\n\n{hint}",
                    parse_mode="Markdown"
                )
        except Exception as e:
            logger.error(f"Random event error for group {group['group_id']}: {e}")
