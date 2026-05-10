from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

# ─── Default ranges for clamping ────────────────────────────────────────────
LIMITS = {
    "pt":  (1,   50,   1),   # points_task
    "piw": (10, 200,   5),   # points_imposter_win
    "pcw": (10, 200,   5),   # points_crew_win
    "pcv": (5,   50,   5),   # points_correct_vote
    "pwv": (-30,  0,   5),   # points_wrong_vote  (negative, step up/down by 5)
    "kc":  (1,   48,   1),   # kill_cooldown (hours)
    "sc2": (1,   24,   1),   # sabotage_cooldown (hours)
    "su":  (1,   10,   1),   # scan_uses
    "shu": (1,    5,   1),   # shield_uses
    "au":  (1,   15,   1),   # anon_uses
    "mm":  (1,    5,   1),   # max_meetings
    "ti":  (1,   24,   1),   # task_interval (hours)
    "vh":  (0,   23,   1),   # voting_hour
    "rh":  (0,   23,   1),   # reveal_hour
    "si":  (1,   24,   1),   # score_interval (hours)
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


async def _is_admin(bot, chat_id: int, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id, user_id)
        return member.status in ("administrator", "creator")
    except Exception:
        return False


def _fmt(key: str, val) -> str:
    if key in ("vh", "rh"):
        return f"{int(val):02d}:00"
    if key in ("kc", "sc2", "ti", "si"):
        return f"{val}h"
    if key in ("pt", "piw", "pcw", "pcv", "pwv"):
        return f"{val} pts"
    return str(val)


# ─── Keyboard builders ───────────────────────────────────────────────────────

def _adj_row(label: str, short_key: str, val) -> list:
    minus = LIMITS[short_key][2]
    return [
        InlineKeyboardButton(f"➖", callback_data=f"s_a_{short_key}_{-minus}"),
        InlineKeyboardButton(f"{label}: {_fmt(short_key, val)}", callback_data="s_noop"),
        InlineKeyboardButton(f"➕", callback_data=f"s_a_{short_key}_{minus}"),
    ]


def build_main_kb():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("💎 Points",    callback_data="s_pts"),
            InlineKeyboardButton("🎮 Game Rules", callback_data="s_rules"),
        ],
        [
            InlineKeyboardButton("⏱ Schedule",   callback_data="s_sched"),
            InlineKeyboardButton("❌ Close",      callback_data="s_close"),
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
        _adj_row("Kill cooldown",   "kc",  cfg["kill_cooldown"]),
        _adj_row("Sabotage CD",     "sc2", cfg["sabotage_cooldown"]),
        _adj_row("Scan uses",       "su",  cfg["scan_uses"]),
        _adj_row("Shield uses",     "shu", cfg["shield_uses"]),
        _adj_row("Anon messages",   "au",  cfg["anon_uses"]),
        _adj_row("Max meetings",    "mm",  cfg["max_meetings"]),
        [InlineKeyboardButton("◀️ Back", callback_data="s_main")],
    ])


def build_sched_kb(cfg: dict):
    return InlineKeyboardMarkup([
        _adj_row("Task every",     "ti", cfg["task_interval"]),
        _adj_row("Voting at",      "vh", cfg["voting_hour"]),
        _adj_row("Reveal at",      "rh", cfg["reveal_hour"]),
        _adj_row("Scoreboard every","si", cfg["score_interval"]),
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
        f"⏱ *Schedule* — task timing & voting hours"
    )


def pts_text(cfg: dict) -> str:
    return (
        f"💎 *Points Settings*\n"
        f"{'─' * 28}\n\n"
        f"Use ➖ / ➕ to adjust each value.\n\n"
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
        f"Use ➖ / ➕ to adjust each value.\n\n"
        f"• Kill cooldown:   *{cfg['kill_cooldown']}h*\n"
        f"• Sabotage CD:     *{cfg['sabotage_cooldown']}h*\n"
        f"• Scan uses:       *{cfg['scan_uses']}x*\n"
        f"• Shield uses:     *{cfg['shield_uses']}x*\n"
        f"• Anon messages:   *{cfg['anon_uses']}x*\n"
        f"• Max meetings:    *{cfg['max_meetings']}x*"
    )


def sched_text(cfg: dict) -> str:
    return (
        f"⏱ *Schedule Settings*\n"
        f"{'─' * 28}\n\n"
        f"Use ➖ / ➕ to adjust each value.\n\n"
        f"• Task every:       *{cfg['task_interval']}h*\n"
        f"• Voting starts at: *{cfg['voting_hour']:02d}:00*\n"
        f"• Reveal at:        *{cfg['reveal_hour']:02d}:00*\n"
        f"• Scoreboard every: *{cfg['score_interval']}h*"
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
    cfg = await db.get_group_cfg(chat.id)
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

    # ── Main menu ────────────────────────────────────────────────
    if data == "s_main":
        await query.edit_message_text(
            main_text(title),
            parse_mode="Markdown",
            reply_markup=build_main_kb()
        )

    # ── Category: Points ─────────────────────────────────────────
    elif data == "s_pts":
        await query.edit_message_text(
            pts_text(cfg),
            parse_mode="Markdown",
            reply_markup=build_pts_kb(cfg)
        )

    # ── Category: Game Rules ──────────────────────────────────────
    elif data == "s_rules":
        await query.edit_message_text(
            rules_text(cfg),
            parse_mode="Markdown",
            reply_markup=build_rules_kb(cfg)
        )

    # ── Category: Schedule ────────────────────────────────────────
    elif data == "s_sched":
        await query.edit_message_text(
            sched_text(cfg),
            parse_mode="Markdown",
            reply_markup=build_sched_kb(cfg)
        )

    # ── Close ─────────────────────────────────────────────────────
    elif data == "s_close":
        try:
            await query.message.delete()
        except Exception:
            await query.edit_message_reply_markup(reply_markup=None)

    # ── No-op (display button tapped) ────────────────────────────
    elif data == "s_noop":
        await query.answer("This shows the current value.", show_alert=False)

    # ── Adjust a value ────────────────────────────────────────────
    elif data.startswith("s_a_"):
        # Format: s_a_{short_key}_{delta}
        parts = data.split("_", 4)   # ['s', 'a', key, delta]
        if len(parts) < 4:
            return

        short_key = parts[2]
        delta_str = parts[3]

        try:
            delta = int(delta_str)
        except ValueError:
            return

        if short_key not in KEY_FIELD:
            return

        field = KEY_FIELD[short_key]
        lo, hi, _ = LIMITS[short_key]
        current = cfg.get(field, cfg.get(field, lo))
        new_val = max(lo, min(hi, current + delta))

        await db.update_group_setting(chat.id, field, new_val)
        cfg[field] = new_val

        # Re-render the right submenu
        if short_key in ("pt", "piw", "pcw", "pcv", "pwv"):
            await query.edit_message_text(
                pts_text(cfg),
                parse_mode="Markdown",
                reply_markup=build_pts_kb(cfg)
            )
        elif short_key in ("kc", "sc2", "su", "shu", "au", "mm"):
            await query.edit_message_text(
                rules_text(cfg),
                parse_mode="Markdown",
                reply_markup=build_rules_kb(cfg)
            )
        elif short_key in ("ti", "vh", "rh", "si"):
            await query.edit_message_text(
                sched_text(cfg),
                parse_mode="Markdown",
                reply_markup=build_sched_kb(cfg)
            )
