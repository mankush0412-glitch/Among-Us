from telegram import Update
from telegram.ext import ContextTypes
from bot.game.engine import GameEngine
from bot.utils.helpers import get_display_name, send_dm, get_mention
from bot.utils.messages import scoreboard_msg
from bot.utils.keyboards import vote_keyboard, scoreboard_keyboard
from bot.game.roles import role_dm_header, get_role_abilities_text
from bot.config import Config
import logging

logger = logging.getLogger(__name__)


def _gid(game) -> str:
    return str(game["_id"])


async def _auto_eject_if_all_voted(bot, db, engine, game_id: str, group_id: int, phase: int):
    """
    After every vote, check if all alive players have voted.
    If yes → immediately reveal the eject result (no need to wait for scheduler).
    """
    try:
        alive = await db.get_alive_players(game_id)
        vote_count = await db.get_vote_count(game_id, phase)

        if vote_count < len(alive):
            return  # Not everyone voted yet

        result = await engine.process_eject(bot, game_id, group_id, phase)

        await bot.send_message(
            chat_id=group_id,
            text=result["message"],
            parse_mode="MarkdownV2"
        )

        # Transition back to active so the hourly scheduler doesn't double-eject
        if not result.get("game_over"):
            await db.update_game_status(game_id, "active")

    except Exception as e:
        logger.error(f"Auto-eject check error: {e}")


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    db = context.bot_data["db"]
    user = query.from_user
    chat = query.message.chat

    # ── Join Game ─────────────────────────────────────────────
    if data.startswith("join_"):
        game_id = data[len("join_"):]

        user_data = await db.get_user(user.id)
        if not user_data or not user_data.get("chat_id"):
            await query.answer(
                "⚠️ Open a private chat with me and send /start first!\n"
                "Then tap Join again.",
                show_alert=True
            )
            return

        game = await db.get_game_by_id(game_id)
        if not game:
            await query.answer("❌ Game not found!", show_alert=True)
            return

        if game["status"] in ("ended", "cancelled"):
            await query.answer("❌ This game has already ended!", show_alert=True)
            return

        existing = await db.get_player(game_id, user.id)
        if existing:
            await query.answer("✅ You're already in the game!", show_alert=False)
            return

        # ── Mid-game join (active game) ──────────────────────
        if game["status"] == "active":
            await db.add_player(game_id, user.id)
            await db.update_player_field(game_id, user.id, "role", "crewmate")
            players = await db.get_players(game_id)

            chat_id = user_data.get("chat_id")
            if chat_id:
                header = role_dm_header("crewmate")
                abilities = get_role_abilities_text("crewmate")
                await send_dm(
                    context.bot, chat_id,
                    f"{header}\n"
                    f"⚠️ *You joined mid-game as a Crewmate!*\n"
                    f"Complete tasks and find the Impostor.\n\n"
                    f"🛠️ *Your Abilities:*\n{abilities}"
                )

            await query.answer("✅ Joined as late Crewmate!", show_alert=True)
            await query.message.reply_text(
                f"✅ *{get_display_name(user)}* joined the ongoing game!\n"
                f"👥 Total players: *{len(players)}* · 📩 Check DM for role!",
                parse_mode="Markdown"
            )
            return

        if game["status"] == "voting":
            await query.answer("🗳️ Voting in progress! Join next game.", show_alert=True)
            return

        # ── Lobby join ────────────────────────────────────────
        await db.add_player(game_id, user.id)
        players = await db.get_players(game_id)
        count = len(players)

        if count >= 3:
            hint = "Admin can now use /startgame to begin! ✅"
        else:
            hint = f"Need {3 - count} more player(s)..."

        await query.answer(f"✅ Joined! Players: {count}", show_alert=False)
        await query.message.reply_text(
            f"✅ *{get_display_name(user)}* joined!\n"
            f"👥 Players: *{count}* · {hint}",
            parse_mode="Markdown"
        )

    # ── Show Players List ─────────────────────────────────────
    elif data.startswith("players_"):
        game_id = data[len("players_"):]
        players = await db.get_players(game_id)
        if not players:
            await query.answer("No players yet!", show_alert=True)
            return

        names = "\n".join([
            f"• {p.get('first_name') or p.get('username') or 'Player'}"
            for p in players
        ])
        await query.answer(f"Players ({len(players)}):\n{names}", show_alert=True)

    # ── Task Done ──────────────────────────────────────────────
    elif data.startswith("task_done_"):
        task_id = data[len("task_done_"):]
        game = await db.get_active_game(chat.id)
        if not game:
            await query.answer("No active game!", show_alert=True)
            return

        game_id = _gid(game)
        task = await db.get_task_by_id(task_id)
        if not task:
            await query.answer("Task not found!", show_alert=True)
            return

        if task.get("is_completed"):
            await query.answer("❌ Task already completed by someone!", show_alert=True)
            return

        player = await db.get_player(game_id, user.id)
        if not player:
            await query.answer("You're not in this game!", show_alert=True)
            return

        if not player["is_alive"]:
            await query.answer("👻 Ghosts can't complete tasks!", show_alert=True)
            return

        await db.complete_task(task_id, user.id)
        bonus = 5 if player.get("is_premium") else 0
        points = 10 + bonus
        await db.add_points(game_id, user.id, points)
        await db.increment_tasks(game_id, user.id)

        name = get_display_name(user)
        await query.edit_message_reply_markup(reply_markup=None)
        await query.message.reply_text(
            f"✅ *Task Complete!*\n\n"
            f"*{name}* finished first!\n"
            f"💎 +{points} pts{' ⭐ Premium bonus!' if bonus else ''}",
            parse_mode="Markdown"
        )

    # ── Vote Button ───────────────────────────────────────────
    elif data.startswith("vote_"):
        parts = data.split("_")
        phase = int(parts[-1])
        target_id = int(parts[-2])
        game_id = "_".join(parts[1:-2])

        player = await db.get_player(game_id, user.id)
        if not player:
            await query.answer("You're not in this game!", show_alert=True)
            return
        if not player["is_alive"]:
            await query.answer("👻 Ghosts can't vote!", show_alert=True)
            return

        engine = GameEngine(db)
        result = await engine.process_vote(game_id, user.id, target_id, phase)

        if not result["success"]:
            await query.answer(f"❌ {result['reason']}", show_alert=True)
            return

        target_name = "SKIP"
        if target_id != 0:
            target_user = await db.get_user(target_id)
            if target_user:
                target_name = target_user.get("first_name") or f"@{target_user.get('username', 'Player')}"

        await query.answer(f"🗳️ Voted for {target_name}!", show_alert=False)
        voter_mention = get_mention(user.id, get_display_name(user))
        await query.message.reply_text(
            f"🗳️ {voter_mention} voted for *{target_name}*!",
            parse_mode="Markdown"
        )

        # ── Auto-reveal when all alive players have voted ──────
        game = await db.get_game_by_id(game_id)
        if game:
            group_id = game["group_id"]
            await _auto_eject_if_all_voted(
                context.bot, db, engine, game_id, group_id, phase
            )

    # ── Score Refresh ─────────────────────────────────────────
    elif data.startswith("score_refresh_"):
        group_id = int(data.split("_")[2])
        scores = await db.get_scores(group_id, limit=10)
        group = await db.fetchone("groups", {"group_id": group_id})
        title = group.get("title") if group else "Group"
        text = scoreboard_msg(list(scores), title)
        kb = scoreboard_keyboard(group_id)
        await query.edit_message_text(text=text, parse_mode="Markdown", reply_markup=kb)

    # ── Help Sections ─────────────────────────────────────────
    elif data == "help_game":
        await query.message.reply_text(
            "🎮 *Game Commands*\n\n"
            "/startgame — Open lobby / start game _(admin)_\n"
            "/joingame — Join current game\n"
            "/leavegame — Leave the lobby\n"
            "/status — See game status & players\n"
            "/mytasks — View pending tasks\n"
            "/score — Group leaderboard\n"
            "/endgame — End game _(admin)_",
            parse_mode="Markdown"
        )

    elif data == "help_abilities":
        await query.message.reply_text(
            "⚡ *Ability Commands*\n\n"
            "🔴 *Impostor* _(use in group OR DM the bot)_:\n"
            "/kill @player · /vent · /sabotage\n"
            "/anon [msg] · /faketask\n\n"
            "🟢 *Crewmate:*\n"
            "/scan @player · /shield\n"
            "/report · /watch @player\n\n"
            "🗳️ *Both:*\n"
            "/vote @player · /meeting\n\n"
            "💡 _Impostors can DM the bot to use abilities secretly!_",
            parse_mode="Markdown"
        )

    elif data == "help_stats":
        await query.message.reply_text(
            "📊 *Stats Commands*\n\n"
            "/mystats — Your personal stats\n"
            "/score — Group leaderboard\n\n"
            "_Scoreboard auto-posts every 6 hours!_",
            parse_mode="Markdown"
        )

    elif data == "help_premium":
        await query.message.reply_text(
            "⭐ *Premium Info*\n\n"
            "/premium — Check your premium status\n\n"
            "Contact the bot owner for premium access!",
            parse_mode="Markdown"
        )

    elif data.startswith("ability_"):
        ability = data.split("_")[1]
        await query.answer(
            f"Use /{ability} command with proper arguments!",
            show_alert=True
        )
