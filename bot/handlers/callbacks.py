from telegram import Update
from telegram.ext import ContextTypes
from bot.game.engine import GameEngine
from bot.utils.helpers import get_display_name
from bot.utils.messages import scoreboard_msg
from bot.utils.keyboards import vote_keyboard, scoreboard_keyboard


def _gid(game) -> str:
    return str(game["_id"])


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    db = context.bot_data["db"]
    user = query.from_user
    chat = query.message.chat

    # ── Join Game ─────────────────────────────────────────────
    if data.startswith("join_"):
        game_id = data[len("join_"):]  # MongoDB ObjectId string
        user_data = await db.get_user(user.id)
        if not user_data or not user_data.get("chat_id"):
            await query.answer(
                "⚠️ Start me in DM first! Send /start to me privately.",
                show_alert=True
            )
            return

        game = await db.get_game_by_id(game_id)
        if not game or game["status"] != "waiting":
            await query.answer("❌ Game already started or doesn't exist!", show_alert=True)
            return

        existing = await db.get_player(game_id, user.id)
        if existing:
            await query.answer("✅ You're already in the game!", show_alert=True)
            return

        await db.add_player(game_id, user.id)
        players = await db.get_players(game_id)
        count = len(players)

        await query.answer(f"✅ Joined! Total players: {count}", show_alert=False)
        await query.message.reply_text(
            f"✅ **{get_display_name(user)}** joined the game! ({count} players)",
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
        task_id = data[len("task_done_"):]  # MongoDB ObjectId string
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
            f"✅ **Task Complete!**\n\n"
            f"🏆 **{name}** finished the task first!\n"
            f"💎 +{points} points awarded!{'  ⭐ Premium bonus!' if bonus else ''}",
            parse_mode="Markdown"
        )

    # ── Vote Button ───────────────────────────────────────────
    elif data.startswith("vote_"):
        # Format: vote_{game_id}_{target_id}_{phase}
        # game_id is a 24-char hex ObjectId, so split from the right
        parts = data.split("_")
        # parts[0]="vote", parts[-1]=phase, parts[-2]=target_id, parts[1:-2]=game_id parts
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

        target_name = "SKIP" if target_id == 0 else f"User {target_id}"
        if target_id != 0:
            target_user = await db.get_user(target_id)
            if target_user:
                target_name = f"@{target_user['username']}" if target_user.get("username") \
                    else target_user.get("first_name", "Player")

        await query.answer(f"🗳️ Voted for {target_name}!", show_alert=False)
        name = get_display_name(user)
        await query.message.reply_text(
            f"🗳️ **{name}** voted for **{target_name}**!",
            parse_mode="Markdown"
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
            "🎮 **Game Commands:**\n\n"
            "/startgame — Start a new game (admin)\n"
            "/joingame — Join the current game\n"
            "/leavegame — Leave the lobby\n"
            "/status — See game status\n"
            "/mytasks — View your pending tasks\n"
            "/endgame — End game (admin)",
            parse_mode="Markdown"
        )

    elif data == "help_abilities":
        await query.message.reply_text(
            "⚡ **Ability Commands:**\n\n"
            "🔴 **Impostor:**\n"
            "/kill @player, /vent, /sabotage\n"
            "/anon [msg], /faketask\n\n"
            "🟢 **Crewmate:**\n"
            "/scan @player, /shield\n"
            "/report, /watch @player\n\n"
            "🗳️ **Both:**\n"
            "/vote @player, /meeting",
            parse_mode="Markdown"
        )

    elif data == "help_stats":
        await query.message.reply_text(
            "📊 **Stats Commands:**\n\n"
            "/mystats — Your personal stats\n\n"
            "📊 Scoreboard auto-posts every 6 hours and is pinned!",
            parse_mode="Markdown"
        )

    elif data == "help_premium":
        await query.message.reply_text(
            "⭐ **Premium Info:**\n\n"
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
