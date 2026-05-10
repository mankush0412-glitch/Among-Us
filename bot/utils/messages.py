from bot.config import Config


IMPOSTER_DM_MSG = """
🔴 *You are the IMPOSTOR!*

Your mission is to blend in, eliminate crewmates, and avoid being voted out.

*Your abilities:*
• /kill @player — Eliminate a crewmate
• /vent — Use vents to move secretly
• /sabotage — Trigger a group emergency
• /anon [msg] — Send an anonymous message
• /faketask — Fake completing a task

💡 Tip: You can also reply to someone's message and use /kill (no @username needed)!

⚠️ Keep this message secret. Trust no one.
"""

CREWMATE_DM_MSG = """
🟢 *You are a CREWMATE!*

Complete tasks, stay alert, and vote out the Impostor before it's too late.

*Your abilities:*
• /scan @player — Get a sus hint about someone
• /shield — Protect yourself from one kill
• /report — Call an emergency meeting
• /watch @player — Spy on someone's activity
• /vote @player — Vote during meetings

💡 Tip: Reply to someone's message and use /vote or /scan directly!

🔍 Stay sharp. Anyone could be the Impostor.
"""


def game_start_msg(player_count: int, imposter_count: int):
    return (
        f"🚀 *Game Started!*\n"
        f"{'─' * 28}\n"
        f"👥 Players: *{player_count}*\n"
        f"🔴 Impostors: *{imposter_count}*\n"
        f"🟢 Crewmates: *{player_count - imposter_count}*\n\n"
        f"📩 Check your DM for your secret role!\n"
        f"⚡ First task will appear shortly.\n\n"
        f"_May the best detective win!_"
    )


def task_msg(task_text: str, category: str, task_num: int, points: int = None):
    if points is None:
        points = Config.POINTS_TASK_COMPLETE
    category_icons = {
        "quiz": "🧠", "riddle": "🧩", "trivia": "📚",
        "math": "🔢", "dare": "🎯", "word": "📝",
        "general": "⭐", "science": "🔬", "history": "📜",
        "sports": "⚽", "movies": "🎬", "music": "🎵", "custom": "✏️"
    }
    icon = category_icons.get(category, "⭐")
    return (
        f"{icon} *Task #{task_num}* — {category.capitalize()}\n"
        f"{'─' * 28}\n\n"
        f"{task_text}\n\n"
        f"⚡ First correct answer wins +{points} pts!\n"
        f"⏰ You have 5 minutes."
    )


def scoreboard_msg(scores: list, group_title: str):
    if not scores:
        return "📊 No scores yet! Play some games first."

    medals = ["🥇", "🥈", "🥉"]
    lines = [f"🏆 *Leaderboard — {group_title[:20]}*\n{'─' * 28}\n"]

    for i, s in enumerate(scores[:10]):
        medal = medals[i] if i < 3 else f"`#{i+1}`"
        name = s.get("first_name") or s.get("username") or "Player"
        uid = s.get("user_id")
        premium = "⭐ " if s.get("is_premium") else ""
        display = f"[{name}](tg://user?id={uid})" if uid else f"*{name}*"
        lines.append(
            f"{medal} {premium}{display}\n"
            f"    💎 {s['total_points']} pts  🎮 {s['games_played']} games  🏅 {s['games_won']} wins\n"
        )

    return "\n".join(lines)


def voting_msg(phase: int):
    return (
        f"🗳️ *Voting Phase #{phase}*\n"
        f"{'─' * 28}\n\n"
        f"Discuss and find the Impostor!\n\n"
        f"Use /vote @player or reply to someone's message with /vote\n"
        f"⏰ Voting closes in 5 minutes."
    )


def eject_msg(player_mention: str, was_imposter: bool, role: str):
    if was_imposter:
        return (
            f"🚀 {player_mention} was ejected\\.\\.\\.\n\n"
            f"🔴 *They WERE the Impostor\\!*\n\n"
            f"🎉 Crewmates win\\! Great detective work\\.\n"
            f"🟢 \\+{Config.POINTS_CREW_WIN} pts for all crewmates\\!"
        )
    else:
        return (
            f"🚀 {player_mention} was ejected\\.\\.\\.\n\n"
            f"🟢 *They were NOT the Impostor\\.*\n\n"
            f"😈 The Impostor is still among you\\.\\.\\.\n"
            f"🔴 Impostor gains \\+5 bonus points\\."
        )


def kill_announcement(victim_mention: str):
    return (
        f"💀 *Body Found\\!*\n\n"
        f"{victim_mention} has been eliminated\\.\n"
        f"👻 They are now a ghost\\.\n\n"
        f"Use /report to call an Emergency Meeting\\!"
    )


def sabotage_msg(sabotage_type: str, time_limit: int):
    sabotages = {
        "power": f"⚡ *Power Outage!* Type `RESTORE` in {time_limit} seconds or lose 5 pts each!",
        "oxygen": f"😮‍💨 *Oxygen Depleted!* What gas makes up 21% of air? Answer in {time_limit} seconds!",
        "reactor": f"☢️ *Reactor Meltdown!* All crewmates send `🔧 FIXING` in {time_limit} seconds!",
        "comms": f"📡 *Communications Down!* No abilities for the next {time_limit} seconds!",
        "lights": f"🌑 *Lights Out!* First to send `💡 FIXED` gets +15 pts!"
    }
    return (
        f"💥 *Sabotage!*\n"
        f"{'─' * 28}\n\n"
        f"{sabotages.get(sabotage_type, '⚠️ Unknown sabotage!')}"
    )


def game_over_imposter_wins(imposter_mention: str):
    return (
        f"😈 *Impostor Wins\\!*\n"
        f"{'─' * 28}\n\n"
        f"🎭 {imposter_mention} was the Impostor — and outsmarted everyone\\!\n\n"
        f"🔴 Impostor: \\+{Config.POINTS_IMPOSTER_WIN} pts\n"
        f"💀 Better luck next time, Crewmates\\!"
    )


def game_over_crew_wins(imposter_mention: str):
    return (
        f"🎉 *Crewmates Win\\!*\n"
        f"{'─' * 28}\n\n"
        f"😈 {imposter_mention} was the Impostor — but couldn't fool the crew\\!\n\n"
        f"🟢 All Crewmates: \\+{Config.POINTS_CREW_WIN} pts\n"
        f"🏆 Amazing teamwork\\!"
    )


def help_msg():
    return (
        f"🎮 *Among Us Bot — Commands*\n"
        f"{'─' * 28}\n\n"
        f"*Getting Started*\n"
        f"• /start — Register with the bot _(DM first!)_\n"
        f"• /register — Register in the group\n"
        f"• /joingame — Join the active game\n"
        f"• /status — See current game status\n\n"
        f"*Game (Admin only)*\n"
        f"• /startgame — Open lobby / start the game\n"
        f"• /endgame — End the current game\n"
        f"• /settings — ⚙️ Configure points, rules & schedule\n"
        f"• /kickplayer @user — Remove a player\n"
        f"• /pingall — Ping all alive players\n\n"
        f"*Impostor Abilities*\n"
        f"• /kill @player or user\\_id — Eliminate a crewmate\n"
        f"• /kill _(reply to message)_ — Kill the person you replied to\n"
        f"• /vent — Use a vent to move secretly\n"
        f"• /sabotage — Trigger an emergency event\n"
        f"• /anon [msg] — Send an anonymous message\n"
        f"• /faketask — Fake a task completion\n\n"
        f"*Crewmate Abilities*\n"
        f"• /scan @player or user\\_id — Get a sus hint\n"
        f"• /scan _(reply to message)_ — Scan the replied player\n"
        f"• /shield — Protect yourself from one kill\n"
        f"• /report — Call an emergency meeting\n"
        f"• /watch @player or user\\_id — Spy on someone\n\n"
        f"*Voting*\n"
        f"• /vote @player or user\\_id — Vote to eject\n"
        f"• /vote _(reply to message)_ — Vote for the replied player\n"
        f"• /meeting — Call emergency meeting\n\n"
        f"*Stats*\n"
        f"• /mystats — Your personal stats\n"
        f"• /score — Group leaderboard"
    )


def welcome_msg(name: str):
    return (
        f"👋 Welcome, *{name}!*\n\n"
        f"You're registered and ready to play Among Us on Telegram.\n\n"
        f"*How to get started:*\n"
        f"1. Add me to your Telegram group\n"
        f"2. Admin uses /startgame to open the lobby\n"
        f"3. Everyone joins with /joingame\n"
        f"4. Admin uses /startgame again to begin!\n\n"
        f"💡 Always start me in DM first so I can send you your secret role.\n\n"
        f"_Good luck. Trust no one._ 👀"
    )


def stats_msg(user_data: dict, score_data: dict):
    name = user_data.get("first_name") or user_data.get("username") or "Player"
    premium_text = "⭐ Premium" if user_data.get("is_premium") else "Free"

    if not score_data:
        return f"📊 *{name}* — No games played yet. Join a game first!"

    games_played = score_data.get("games_played", 0)
    games_won = score_data.get("games_won", 0)
    win_rate = round((games_won / games_played) * 100, 1) if games_played > 0 else 0

    return (
        f"📊 *{name}* — {premium_text}\n"
        f"{'─' * 28}\n"
        f"💎 Points: *{score_data.get('total_points', 0)}*\n"
        f"🎮 Games: *{games_played}*  |  🏆 Wins: *{games_won}* ({win_rate}%)\n\n"
        f"🔴 Impostor wins: {score_data.get('imposter_wins', 0)}\n"
        f"🟢 Crewmate wins: {score_data.get('crew_wins', 0)}\n"
        f"📋 Tasks done: {score_data.get('tasks_completed', 0)}\n"
        f"🔪 Kills made: {score_data.get('kills_made', 0)}\n"
        f"🎯 Correct votes: {score_data.get('correct_votes', 0)}"
    )
