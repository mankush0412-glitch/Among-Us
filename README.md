# 🚀 Among Us Telegram Bot

A feature-rich Among Us-style game bot for Telegram groups, with daily tasks, secret roles, abilities, scoring, premium system, and much more.

---

## ⚡ Quick Setup

### Step 1 — Get Bot Token
1. Open Telegram → search **@BotFather**
2. Send `/newbot`
3. Follow prompts, copy the **token**

### Step 2 — Get Your Telegram User ID
1. Open Telegram → search **@userinfobot**
2. Send `/start` → copy your **User ID**

### Step 3 — Install & Configure
```bash
# Clone / extract this project
pip install -r requirements.txt

# Copy env file and fill it
cp .env.example .env
```

Edit `.env`:
```
BOT_TOKEN=your_bot_token_here
OWNER_ID=your_telegram_user_id
WEBHOOK_URL=https://your-app.onrender.com
DATABASE_PATH=/data/bot_data.db
```

### Step 4 — Run Locally (Testing)
```bash
python main.py
```

---

## 🌐 Deploy on Render (Free)

1. Push this project to a **GitHub repo**
2. Go to [render.com](https://render.com) → **New Web Service**
3. Connect your GitHub repo
4. Render auto-detects `render.yaml`
5. Add these **Environment Variables** in Render dashboard:
   - `BOT_TOKEN` → your bot token
   - `OWNER_ID` → your Telegram user ID
   - `WEBHOOK_URL` → `https://your-app-name.onrender.com`
6. Click **Deploy**

> ✅ Render free tier gives you a persistent disk (1GB) for the database.

---

## 📋 All Commands

### 👤 User Commands
| Command | Description |
|---------|-------------|
| `/start` | Register with bot (use in DM first!) |
| `/help` | Full help menu |
| `/register` | Register in the group |
| `/mystats` | View your personal stats |
| `/premium` | Check premium status |
| `/status` | Current game status |
| `/mytasks` | View pending tasks |

### 🎮 Game Commands
| Command | Description |
|---------|-------------|
| `/startgame` | Start a new game (admin) |
| `/joingame` | Join the current lobby |
| `/leavegame` | Leave the game lobby |

### 🔴 Impostor Abilities
| Command | Description |
|---------|-------------|
| `/kill @player` | Eliminate a crewmate |
| `/vent` | Teleport between rooms |
| `/sabotage` | Trigger group emergency |
| `/anon [msg]` | Send anonymous message |
| `/faketask` | Fake a task completion |

### 🟢 Crewmate Abilities
| Command | Description |
|---------|-------------|
| `/scan @player` | Get a sus hint |
| `/shield` | Protect from next kill |
| `/report` | Call emergency meeting |
| `/watch @player` | Spy on their activity |
| `/vote @player` | Vote to eject |
| `/meeting` | Emergency meeting (limited) |

### 👑 Admin Commands (Group Admins)
| Command | Description |
|---------|-------------|
| `/endgame` | End current game |
| `/addtask [text]` | Add custom task |
| `/settime` | View time settings |
| `/kickplayer @player` | Remove player from game |
| `/pingall [msg]` | Ping all alive players |

### 🔑 Owner Commands (You Only)
| Command | Description |
|---------|-------------|
| `/broadcast [msg]` | Send to ALL groups |
| `/addpremium @user [days]` | Grant premium |
| `/removepremium @user` | Remove premium |
| `/ownerstats` | Global bot statistics |
| `/ban @user` | Ban a user |
| `/unban @user` | Unban a user |
| `/allgroups` | List all active groups |
| `/forceend [group_id]` | Force end any game |

---

## 🎮 How Game Works

### Daily Schedule (Auto)
- **9:00 AM** — Game starts, roles assigned via DM
- **Every 2h** — New task posted in group
- **Every 3h** — Ambient atmosphere message
- **Every 5h** — Random event (bonus points, mystery rewards, etc.)
- **Every 6h** — Scoreboard posted + pinned by bot
- **7:00 PM** — Voting phase begins
- **9:00 PM** — Eject result revealed

### Roles
- **Impostor 🔴** — Blend in, sabotage, eliminate crewmates
- **Crewmate 🟢** — Complete tasks, find the impostor
- **Ghost 👻** — Eliminated, can still watch

### Points System
| Action | Points |
|--------|--------|
| Task completed (first) | +10 |
| Task completed (premium) | +15 |
| Correct vote | +15 |
| Wrong vote | -5 |
| Crewmate wins | +20 |
| Impostor wins | +30 |
| Successful kill | +5 |

---

## ⭐ Premium System

Premium users get:
- ⭐ Badge on leaderboard
- +5 bonus points per task
- 5 scan uses (vs 3 free)
- 8 anonymous messages (vs 5 free)
- 2 shields per game (vs 1 free)

**Grant premium:**
```
/addpremium @username 30
```
(30 = days, default)

---

## 📊 Data

- **Tasks:** 350+ across 10+ categories (GK, Science, Math, Riddles, Sports, Movies, Music, Tech, Geography, History, Word Games, Among Us themed)
- **Imposter Activities:** 200+ unique activity descriptions
- **Crewmate Activities:** 200+ unique activity descriptions
- **Random Events:** 8 dynamic game events
- **Sabotage Types:** 5 different sabotage challenges

---

## 🔧 Bot DM System — How It Works

> **Q: How does the bot DM players?**

For the bot to DM a user:
1. **User must first send `/start` to the bot in private.**
2. This registers their `chat_id` in the database.
3. When the game starts, the bot uses this stored `chat_id` to DM them their secret role.

⚠️ If a user never sent `/start` to the bot privately, they **cannot** receive their secret role.
The bot will warn them when they try to join without registering in DM.

---

## 🗂️ Project Structure

```
telegram-among-us-bot/
├── main.py                    # Flask app + webhook handler
├── requirements.txt
├── render.yaml                # Render deployment config
├── .env.example
├── bot/
│   ├── config.py              # All configuration
│   ├── database.py            # SQLite database operations
│   ├── handlers/
│   │   ├── start.py           # /start, /help, /register, /mystats
│   │   ├── game.py            # /startgame, /joingame, /status
│   │   ├── abilities.py       # /kill, /vent, /sabotage, /scan...
│   │   ├── voting.py          # /vote, /meeting
│   │   ├── admin.py           # Admin-only commands
│   │   ├── owner.py           # Owner-only commands
│   │   ├── premium.py         # /premium
│   │   └── callbacks.py       # All inline button handlers
│   ├── game/
│   │   ├── engine.py          # Core game logic
│   │   ├── roles.py           # Role definitions
│   │   ├── events.py          # Random events & sabotages
│   │   └── scheduler.py       # APScheduler jobs
│   └── utils/
│       ├── messages.py        # All message templates
│       ├── keyboards.py       # Inline keyboard layouts
│       └── helpers.py         # Utility functions
└── data/
    ├── tasks_data.py          # 350+ tasks across all categories
    └── activities_data.py     # 400+ imposter & crewmate activities
```

---

## 🛠️ Troubleshooting

**Bot not responding?**
- Check `BOT_TOKEN` is correct
- Make sure webhook URL is set properly on Render

**Users not getting DMs?**
- They must send `/start` to the bot privately first

**Database errors?**
- Render free disk may reset on restarts — upgrade to paid or use PostgreSQL

**Scheduler not running?**
- APScheduler needs the Flask process to stay alive — Render free tier keeps it up with health pings at `/health`

---

## 📞 Support

Contact the bot owner in Telegram for premium access or support.
