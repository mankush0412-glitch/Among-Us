from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def join_game_keyboard(game_id: int):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 Join Game", callback_data=f"join_{game_id}")],
        [InlineKeyboardButton("👥 View Players", callback_data=f"players_{game_id}")]
    ])


def task_keyboard(task_id: int):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Task Complete!", callback_data=f"task_done_{task_id}")]
    ])


def vote_keyboard(players: list, game_id: int, phase: int):
    buttons = []
    for p in players:
        name = p["first_name"] or p["username"] or "Player"
        buttons.append([
            InlineKeyboardButton(
                f"🔴 Vote {name}",
                callback_data=f"vote_{game_id}_{p['user_id']}_{phase}"
            )
        ])
    buttons.append([InlineKeyboardButton("⏭ Skip Vote", callback_data=f"vote_{game_id}_0_{phase}")])
    return InlineKeyboardMarkup(buttons)


def confirm_keyboard(action: str, target_id: int):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Yes", callback_data=f"confirm_{action}_{target_id}"),
            InlineKeyboardButton("❌ No", callback_data=f"cancel_{action}")
        ]
    ])


def ability_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔪 Kill", callback_data="ability_kill"),
            InlineKeyboardButton("🌀 Vent", callback_data="ability_vent")
        ],
        [
            InlineKeyboardButton("💣 Sabotage", callback_data="ability_sabotage"),
            InlineKeyboardButton("📨 Anon Msg", callback_data="ability_anon")
        ],
        [InlineKeyboardButton("📋 Fake Task", callback_data="ability_faketask")]
    ])


def crew_ability_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔍 Scan", callback_data="ability_scan"),
            InlineKeyboardButton("🛡 Shield", callback_data="ability_shield")
        ],
        [
            InlineKeyboardButton("📢 Report", callback_data="ability_report"),
            InlineKeyboardButton("👁 Watch", callback_data="ability_watch")
        ]
    ])


def scoreboard_keyboard(group_id: int):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 Refresh", callback_data=f"score_refresh_{group_id}")]
    ])


def premium_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📩 Contact Owner for Premium", url="https://t.me/")]
    ])


def help_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🎮 Game Commands", callback_data="help_game"),
            InlineKeyboardButton("⚡ Abilities", callback_data="help_abilities")
        ],
        [
            InlineKeyboardButton("📊 Stats", callback_data="help_stats"),
            InlineKeyboardButton("👑 Premium", callback_data="help_premium")
        ]
    ])
