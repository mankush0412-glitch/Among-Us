from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

# ─── Limits: (min, max, step) ── all interval timers are in MINUTES ─────────
LIMITS = {
    "pt":  (1,    50,    1),   # points_task
    "piw": (10,  200,    5),   # points_imposter_win
    "pcw": (10,  200,    5),   # points_crew_win
    "pcv": (5,    50,    5),   # points_correct_vote
    "pwv": (-30,   0,    5),   # points_wrong_vote (negative)
    "kc":  (15,  480,   15),   # kill_cooldown      → MINUTES
    "sc2": (15,  240,   15),   # sabotage_cooldown  → MINUTES
    "su":  (1,    10,    1),   # scan_uses
    "shu": (1,     5,    1),   # shield_uses
    "au":  (1,    15,    1),   # anon_uses
    "mm":  (1,     5,    1),   # max_meetings
    "ti":  (5,   480,    5),   # task_interval      → MINUTES
    "vh":  (0,    23,    1),   # voting_hour (0-23 UTC)
    "rh":  (0,    23,    1),   # reveal_hour (0-23 UTC)
    "si":  (60, 1440,   60),   # score_interval     → MINUTES (60=1h, 1440=24h)
}

KEY_FIELD = {
    "pt":  "points_task",
    "piw": "points_imposter_win",
    "pcw": "points_crew_win",
    "pcv": "points_correct_vote",
    "pwv": "points_wrong_vote",
    "kc":  "kill_cooldown",
    "sc2": "sabotage_cooldown",
    "su":  "scan_uses",
    "shu": "shield_uses",
    "au":  "anon_uses",
    "mm":  "max_meetings",
    "ti":  "task_interval",
    "vh":  "voting_hour",
    "rh":  "reveal_hour",
    "si":  "score_interval",
}

# Keys whose values are stored & displayed as minutes
MINUTE_KEYS = {"kc", "sc2", "ti", "si"}

# Keys whose values are hour-of-day (0–23)
HOUR_OF_DAY_KEYS = {"vh", "rh"}


def _fmt(key: str, val) -> str:
    """Human-readable display of a setting value."""
    if key in HOUR_OF_DAY_KEYS:
        return f"{int(val):02d}:00"
    if key in MINUTE_KEYS:
        val = int(val)
        if val < 60:
            return f"{val} min"
        hours, mins = divmod(val, 60)
        return f"{hours}h {mins}m" if mins else f"{hours}h"
    if key in ("pt", "piw", "pcw", "pcv", "pwv"):
        return f"{val} pts"
    return str(val)


async def _is_admin(bot, chat_id: int, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id, user_id)
        return member.status in ("administrator", "creator")
    except Exception:
        return False


# ─── Keyboard builders ───────────────────────────────────────────────────────

def _adj_row(label: str, short_key: str, val) -> list:
    step = LIMITS[short_key][2]
    return [
        InlineKeyboardButton("➖", callback_data=f"s_a_{short_key}_{-step}"),
        InlineKeyboardButton(f"{label}: {_fmt(short_key, val)}", callback_data="s_noop"),
        InlineKeyboardButton("➕", callback_data=f"s_a_{short_key}_{step}"),
    ]


def build_main_kb():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("💎 Points",     callback_data="s_pts"),
            InlineKeyboardButton("🎮 Game Rules",  callback_data="s_rules"),
        ],
        [
            InlineKeyboardButton("⏱ Timers",      callback_data="s_sched"),
            InlineKeyboardButton("❌ Close",        callback_data="s_close"),
        ],
    ])


def build_pts_kb(cfg: dict):
    return InlineKeyboardMarkup([
        _adj_row("Task pts",      "pt",  cfg["points_task"]),
        _adj_row("Impostor win",  "piw", cfg["points_imposter_win"]),
        _adj_row("Crewmate win",  "pcw", cfg["points_crew_win"]),
        _adj_row("Correct vote",  "pcv", cfg["points_correct_vote"]),
        _adj_row("Wrong vote",    "pwv", cfg["points_wrong_vote"]),
        [InlineKeyboardButton("◀️ Back", callback_data="s_main")],
    ])


def build_rules_kb(cfg: dict):
    return InlineKeyboardMarkup([
        _adj_row("Kill cooldown",  "kc",  cfg["kill_cooldown"]),
        _adj_row("Sabotage CD",    "sc2", cfg["sabotage_cooldown"]),
        _adj_row("Scan uses",      "su",  cfg["scan_uses"]),
        _adj_row("Shield uses",    "shu", cfg["shield_uses"]),
        _adj_row("Anon messages",  "au",  cfg["anon_uses"]),
        _adj_row("Max meetings",   "mm",  cfg["max_meetings"]),
        [InlineKeyboardButton("◀️ Back", callback_data="s_main")],
    ])


def build_sched_kb(cfg: dict):
    return InlineKeyboardMarkup([
        _adj_row("Task every",        "ti", cfg["task_interval"]),
        _adj_row("Scoreboard every",  "si", cfg["score_interval"]),
        _adj_row("Voting starts at",  "vh", cfg["voting_hour"]),
        _adj_row("Reveal at",         "rh", cfg["reveal_hour"]),
        [InlineKeyboardButton("◀️ Back", callback_data="s_main")],
    ])


# ─── Message text builders ───────────────────────────────────────────────────

def main_text(group_title: str) -> str:
    return (
        f"⚙️ *Game Settings — {group_title}*\n"
        f"{'─' * 28}\n\n"
        f"Choose a category to configure.\n"
        f"Changes take effect immediately.\n\n"
        f"💎 *Points* — task/win/vote rewards\n"
        f"🎮 *Game Rules* — cooldowns & ability uses\n"
        f"⏱ *Timers* — task interval, voting & reveal time\n\n"
        f"_All interval timers use minutes._"
    )


def pts_text(cfg: dict) -> str:
    return (
        f"💎 *Points Settings*\n"
        f"{'─' * 28}\n\n"
        f"Use ➖ / ➕ to adjust.\n\n"
        f"• Task complete: *{cfg['points_task']} pts*\n"
        f"• Impostor win:  *{cfg['points_imposter_win']} pts*\n"
        f"• Crewmate win:  *{cfg['points_crew_win']} pts*\n"
        f"• Correct vote:  *{cfg['points_correct_vote']} pts*\n"
        f"• Wrong vote:    *{cfg['points_wrong_vote']} pts*"
    )


def rules_text(cfg: dict) -> str:
    return (
        f"🎮 *Game Rules*\n"
        f"{'─' * 28}\n\n"
        f"Use ➖ / ➕ to adjust.\n\n"
        f"• Kill cooldown:   *{_fmt('kc',  cfg['kill_cooldown'])}*\n"
        f"• Sabotage CD:     *{_fmt('sc2', cfg['sabotage_cooldown'])}*\n"
        f"• Scan uses:       *{cfg['scan_uses']}x*\n"
        f"• Shield uses:     *{cfg['shield_uses']}x*\n"
        f"• Anon messages:   *{cfg['anon_uses']}x*\n"
        f"• Max meetings:    *{cfg['max_meetings']}x*"
    )


def sched_text(cfg: dict) -> str:
    return (
        f"⏱ *Timer Settings*\n"
        f"{'─' * 28}\n\n"
        f"Use ➖ / ➕ to adjust.\n"
        f"_Task & scoreboard intervals are in minutes._\n"
        f"_Voting & reveal are the UTC hour (0–23)._\n\n"
        f"• Task every:         *{_fmt('ti', cfg['task_interval'])}*\n"
        f"• Scoreboard every:   *{_fmt('si', cfg['score_interval'])}*\n"
        f"• Voting starts at:   *{_fmt('vh', cfg['voting_hour'])}* UTC\n"
        f"• Reveal at:          *{_fmt('rh', cfg['reveal_hour'])}* UTC"
    )


# ─── Command handler ─────────────────────────────────────────────────────────

async def settings_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = context.bot_data["db"]
    user = update.effective_user
    chat = update.effective_chat

    if chat.type == "private":
        await update.message.reply_text("❌ Use /settings in your group!")
        return

    if not await _is_admin(context.bot, chat.id, user.id):
        await update.message.reply_text("❌ Only group admins can open settings!")
        return

    await db.register_group(chat.id, chat.title or "Group")
    title = chat.title or "Group"

    await update.message.reply_text(
        main_text(title),
        parse_mode="Markdown",
        reply_markup=build_main_kb()
    )


# ─── Callback handler ────────────────────────────────────────────────────────

async def settings_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    db = context.bot_data["db"]
    user = query.from_user
    chat = query.message.chat

    if not await _is_admin(context.bot, chat.id, user.id):
        await query.answer("❌ Only admins can change settings!", show_alert=True)
        return

    cfg = await db.get_group_cfg(chat.id)
    title = chat.title or "Group"

    if data == "s_main":
        await query.edit_message_text(
            main_text(title), parse_mode="Markdown", reply_markup=build_main_kb()
        )

    elif data == "s_pts":
        await query.edit_message_text(
            pts_text(cfg), parse_mode="Markdown", reply_markup=build_pts_kb(cfg)
        )

    elif data == "s_rules":
        await query.edit_message_text(
            rules_text(cfg), parse_mode="Markdown", reply_markup=build_rules_kb(cfg)
        )

    elif data == "s_sched":
        await query.edit_message_text(
            sched_text(cfg), parse_mode="Markdown", reply_markup=build_sched_kb(cfg)
        )

    elif data == "s_close":
        try:
            await query.message.delete()
        except Exception:
            await query.edit_message_reply_markup(reply_markup=None)

    elif data == "s_noop":
        await query.answer("This shows the current value.", show_alert=False)

    elif data.startswith("s_a_"):
        # Format: s_a_{short_key}_{delta}  (delta may be negative, e.g. s_a_kc_-15)
        # Split carefully: prefix is "s_a_", then short_key, then delta
        rest = data[4:]                          # e.g. "kc_-15"
        last_under = rest.rfind("_")
        short_key = rest[:last_under]            # "kc"
        delta_str  = rest[last_under + 1:]       # "-15"

        try:
            delta = int(delta_str)
        except ValueError:
            return

        if short_key not in KEY_FIELD:
            return

        field = KEY_FIELD[short_key]
        lo, hi, _ = LIMITS[short_key]
        current = cfg.get(field, lo)
        new_val = max(lo, min(hi, int(current) + delta))

        await db.update_group_setting(chat.id, field, new_val)
        cfg[field] = new_val

        # Re-render the correct submenu
        if short_key in ("pt", "piw", "pcw", "pcv", "pwv"):
            await query.edit_message_text(
                pts_text(cfg), parse_mode="Markdown", reply_markup=build_pts_kb(cfg)
            )
        elif short_key in ("kc", "sc2", "su", "shu", "au", "mm"):
            await query.edit_message_text(
                rules_text(cfg), parse_mode="Markdown", reply_markup=build_rules_kb(cfg)
            )
        elif short_key in ("ti", "vh", "rh", "si"):
            await query.edit_message_text(
                sched_text(cfg), parse_mode="Markdown", reply_markup=build_sched_kb(cfg)
            )
