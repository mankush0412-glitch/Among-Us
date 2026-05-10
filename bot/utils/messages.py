from bot.config import Config


GAME_BANNER = """
╔══════════════════════════════╗
║   🚀 AMONG US - TELEGRAM 🚀  ║
║      Impostor Hunt Game      ║
╚══════════════════════════════╝
"""

IMPOSTER_DM_MSG = """
🔴━━━━━━━━━━━━━━━━━━━━━━━━━━🔴
       ⚠️ SECRET MISSION ⚠️
🔴━━━━━━━━━━━━━━━━━━━━━━━━━━🔴

🎭 You are the **IMPOSTOR!**

Your mission:
• Blend in with crewmates
• Sabotage tasks secretly
• Eliminate crewmates before voting
• Don't get voted out!

🛠️ Your Abilities:
• /kill @player — Eliminate a crewmate
• /vent — Teleport to another room
• /sabotage — Trigger a group emergency
• /anon [msg] — Send anonymous message
• /faketask — Fake a task completion

⚠️ Keep this message SECRET!
🔴━━━━━━━━━━━━━━━━━━━━━━━━━━🔴
"""

CREWMATE_DM_MSG = """
🟢━━━━━━━━━━━━━━━━━━━━━━━━━━🟢
       🛸 MISSION BRIEFING 🛸
🟢━━━━━━━━━━━━━━━━━━━━━━━━━━🟢

👷 You are a **CREWMATE!**

Your mission:
• Complete all tasks
• Find and vote out the Impostor
• Don't trust anyone blindly!

🛠️ Your Abilities:
• /scan @player — Get a sus hint
• /shield — Protect yourself once
• /report — Call emergency meeting
• /watch @player — Track their moves
• /vote @player — Vote in meetings

🔍 Stay sharp, stay alive!
🟢━━━━━━━━━━━━━━━━━━━━━━━━━━🟢
"""

def game_start_msg(player_count: int, imposter_count: int):
    return f"""
🚀━━━━━━━━━━━━━━━━━━━━━━━━━━🚀
      🎮 GAME STARTED! 🎮
🚀━━━━━━━━━━━━━━━━━━━━━━━━━━🚀

👥 Players: **{player_count}**
🔴 Impostors: **{imposter_count}**
🟢 Crewmates: **{player_count - imposter_count}**

📩 Check your DM for your secret role!
⚡ First task incoming in 30 seconds...

🏆 May the best detective win!
🚀━━━━━━━━━━━━━━━━━━━━━━━━━━🚀
"""

def task_msg(task_text: str, category: str, task_num: int):
    category_icons = {
        "quiz": "🧠", "riddle": "🧩", "trivia": "📚",
        "math": "🔢", "dare": "🎯", "word": "📝",
        "general": "⭐", "science": "🔬", "history": "📜",
        "sports": "⚽", "movies": "🎬", "music": "🎵"
    }
    icon = category_icons.get(category, "⭐")
    return f"""
{icon}━━━━━━━━━━━━━━━━━━━━━━━━━━{icon}
      📋 TASK #{task_num} - {category.upper()}
{icon}━━━━━━━━━━━━━━━━━━━━━━━━━━{icon}

{task_text}

⚡ First correct answer wins +{Config.POINTS_TASK_COMPLETE} points!
⏰ You have 5 minutes!
"""

def scoreboard_msg(scores: list, group_title: str):
    if not scores:
        return "📊 No scores yet! Play some games first."

    medals = ["🥇", "🥈", "🥉"]
    board = f"""
🏆━━━━━━━━━━━━━━━━━━━━━━━━━━🏆
   📊 LEADERBOARD - {group_title[:20]}
🏆━━━━━━━━━━━━━━━━━━━━━━━━━━🏆

"""
    for i, s in enumerate(scores[:10]):
        medal = medals[i] if i < 3 else f"#{i+1}"
        name = s["first_name"] or s["username"] or "Player"
        premium = Config.PREMIUM_BADGE if s["is_premium"] else ""
        board += f"{medal} {premium}{name}\n"
        board += f"   💎 {s['total_points']} pts | 🎮 {s['games_played']} games | 🏅 {s['games_won']} wins\n\n"

    board += "🏆━━━━━━━━━━━━━━━━━━━━━━━━━━🏆"
    return board


def voting_msg(phase: int):
    return f"""
🗳️━━━━━━━━━━━━━━━━━━━━━━━━━━🗳️
      ⚠️ VOTING PHASE #{phase} ⚠️
🗳️━━━━━━━━━━━━━━━━━━━━━━━━━━🗳️

🔍 Discuss and find the Impostor!

Use /vote @player to cast your vote
Or use the buttons below.

⏰ Voting closes in 5 minutes!
"""

def eject_msg(player_name: str, was_imposter: bool, role: str):
    if was_imposter:
        return f"""
🚀━━━━━━━━━━━━━━━━━━━━━━━━━━🚀
     ✅ CORRECT EJECTION! ✅
🚀━━━━━━━━━━━━━━━━━━━━━━━━━━🚀

**{player_name}** was ejected...
🔴 **{player_name} WAS THE IMPOSTOR!**

🎉 Crewmates win! Great detective work!
🟢 +{Config.POINTS_CREW_WIN} points for all crewmates!
"""
    else:
        return f"""
🚀━━━━━━━━━━━━━━━━━━━━━━━━━━🚀
     ❌ WRONG EJECTION! ❌
🚀━━━━━━━━━━━━━━━━━━━━━━━━━━🚀

**{player_name}** was ejected...
🟢 **{player_name} was NOT the Impostor!**

😈 The Impostor is still among you...
🔴 Impostor gains +5 bonus points!
"""

def kill_announcement(killer_name: str, victim_name: str):
    return f"""
💀━━━━━━━━━━━━━━━━━━━━━━━━━━💀
        ⚠️ BODY FOUND ⚠️
💀━━━━━━━━━━━━━━━━━━━━━━━━━━💀

🔪 **{victim_name}** has been eliminated!
👻 {victim_name} is now a Ghost.

Use /report to call Emergency Meeting!
"""

def sabotage_msg(sabotage_type: str, time_limit: int):
    sabotages = {
        "power": f"⚡ POWER OUTAGE! Type 'RESTORE' in {time_limit} seconds or lose 5 points each!",
        "oxygen": f"😮‍💨 OXYGEN DEPLETED! Solve this to restore: What gas makes up 21% of air? Answer in {time_limit} seconds!",
        "reactor": f"☢️ REACTOR MELTDOWN! All crewmates send '🔧 FIXING' in {time_limit} seconds!",
        "comms": f"📡 COMMUNICATIONS DOWN! No abilities for next {time_limit} seconds!",
        "lights": f"🌑 LIGHTS OUT! First person to send '💡 FIXED' gets +15 points!"
    }
    return f"""
💣━━━━━━━━━━━━━━━━━━━━━━━━━━💣
      ⚠️ SABOTAGE! ⚠️
💣━━━━━━━━━━━━━━━━━━━━━━━━━━💣

{sabotages.get(sabotage_type, "⚠️ Unknown sabotage!")}
"""

def game_over_imposter_wins(imposter_name: str):
    return f"""
🔴━━━━━━━━━━━━━━━━━━━━━━━━━━🔴
    😈 IMPOSTOR WINS! 😈
🔴━━━━━━━━━━━━━━━━━━━━━━━━━━🔴

🎭 **{imposter_name}** was the Impostor!
They outsmarted everyone!

🔴 Impostor: +{Config.POINTS_IMPOSTER_WIN} points!
💀 Better luck next time, Crewmates!
"""

def game_over_crew_wins(imposter_name: str):
    return f"""
🟢━━━━━━━━━━━━━━━━━━━━━━━━━━🟢
   🎉 CREWMATES WIN! 🎉
🟢━━━━━━━━━━━━━━━━━━━━━━━━━━🟢

😈 **{imposter_name}** was the Impostor!
Crewmates are victorious!

🟢 All Crewmates: +{Config.POINTS_CREW_WIN} points!
🏆 Amazing teamwork!
"""

def help_msg():
    return """
🎮━━━━━━━━━━━━━━━━━━━━━━━━━━🎮
    AMONG US BOT - HELP MENU
🎮━━━━━━━━━━━━━━━━━━━━━━━━━━🎮

🚀 GETTING STARTED:
• /start — Register with bot (in DM first!)
• /register — Register in group
• /joingame — Join active game
• /status — Current game status

🎮 GAME COMMANDS:
• /startgame — Start a new game (admin)
• /endgame — End current game (admin)
• /mytasks — See your pending tasks

🔴 IMPOSTOR ABILITIES:
• /kill @player — Eliminate a crewmate
• /vent — Use vents to teleport
• /sabotage — Trigger emergency event
• /anon [msg] — Send anonymous message
• /faketask — Fake a task completion

🟢 CREWMATE ABILITIES:
• /scan @player — Check for sus activity
• /shield — Protect yourself from kill
• /report — Call emergency meeting
• /watch @player — Spy on someone

🗳️ VOTING:
• /vote @player — Vote to eject
• /meeting — Emergency meeting (limited)

📊 STATS:
• /mystats — Your personal stats
• /score — Group leaderboard

🎮━━━━━━━━━━━━━━━━━━━━━━━━━━🎮
"""

def welcome_msg(name: str):
    return f"""
🚀━━━━━━━━━━━━━━━━━━━━━━━━━━🚀
   Welcome to AMONG US BOT! 🎮
🚀━━━━━━━━━━━━━━━━━━━━━━━━━━🚀

Hey **{name}**! 👋

You're now registered and ready to play!

✅ Next Steps:
1. Add this bot to your Telegram group
2. Use /startgame to begin
3. Members join with /joingame
4. Game auto-starts when enough players join!

💡 Tip: Always start the bot in DM first
so it can send you secret role messages!

🎮 Good luck, and trust no one! 👀
🚀━━━━━━━━━━━━━━━━━━━━━━━━━━🚀
"""

def stats_msg(user_data: dict, score_data: dict):
    name = user_data["first_name"] or user_data["username"] or "Player"
    premium_text = f"⭐ PREMIUM MEMBER" if user_data["is_premium"] else "Free Player"

    if not score_data:
        return f"📊 **{name}** — No games played yet! Join a game first."

    win_rate = 0
    if score_data["games_played"] > 0:
        win_rate = round((score_data["games_won"] / score_data["games_played"]) * 100, 1)

    return f"""
📊━━━━━━━━━━━━━━━━━━━━━━━━━━📊
      PLAYER STATS - {name}
📊━━━━━━━━━━━━━━━━━━━━━━━━━━📊

🎖 Status: {premium_text}
💎 Total Points: {score_data['total_points']}
🎮 Games Played: {score_data['games_played']}
🏆 Games Won: {score_data['games_won']} ({win_rate}%)

🔴 Impostor Wins: {score_data['imposter_wins']}
🟢 Crewmate Wins: {score_data['crew_wins']}
📋 Tasks Completed: {score_data['tasks_completed']}
🔪 Kills Made: {score_data['kills_made']}
🎯 Correct Votes: {score_data['correct_votes']}

📊━━━━━━━━━━━━━━━━━━━━━━━━━━📊
"""
