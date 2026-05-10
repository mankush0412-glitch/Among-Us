from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters


def register_handlers(app: Application):
    from bot.handlers.start import start_cmd, help_cmd, register_cmd, mystats_cmd, score_cmd, dm_message_handler
    from bot.handlers.game import (
        startgame_cmd, joingame_cmd, leavegame_cmd,
        gamestatus_cmd, mytasks_cmd
    )
    from bot.handlers.abilities import (
        kill_cmd, vent_cmd, sabotage_cmd, scan_cmd,
        shield_cmd, report_cmd, watch_cmd, anon_cmd, faketask_cmd
    )
    from bot.handlers.voting import vote_cmd, meeting_cmd
    from bot.handlers.admin import (
        endgame_cmd, addtask_cmd, listtasks_cmd, deltask_cmd,
        settime_cmd, kickplayer_cmd, pingall_cmd
    )
    from bot.handlers.owner import (
        broadcast_cmd, addpremium_cmd, removepremium_cmd,
        ownerstats_cmd, banuser_cmd, unbanuser_cmd, allgroups_cmd, forceend_cmd
    )
    from bot.handlers.premium import premium_cmd
    from bot.handlers.settings import settings_cmd, settings_callback
    from bot.handlers.callbacks import button_callback

    # ── Private (DM) Commands ──────────────────────────────────
    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("register", register_cmd))
    app.add_handler(CommandHandler("mystats", mystats_cmd))
    app.add_handler(CommandHandler("premium", premium_cmd))
    app.add_handler(CommandHandler("score", score_cmd))

    # ── Game Commands ──────────────────────────────────────────
    app.add_handler(CommandHandler("startgame", startgame_cmd))
    app.add_handler(CommandHandler("joingame", joingame_cmd))
    app.add_handler(CommandHandler("leavegame", leavegame_cmd))
    app.add_handler(CommandHandler("status", gamestatus_cmd))
    app.add_handler(CommandHandler("mytasks", mytasks_cmd))

    # ── Ability Commands ───────────────────────────────────────
    app.add_handler(CommandHandler("kill", kill_cmd))
    app.add_handler(CommandHandler("vent", vent_cmd))
    app.add_handler(CommandHandler("sabotage", sabotage_cmd))
    app.add_handler(CommandHandler("scan", scan_cmd))
    app.add_handler(CommandHandler("shield", shield_cmd))
    app.add_handler(CommandHandler("report", report_cmd))
    app.add_handler(CommandHandler("watch", watch_cmd))
    app.add_handler(CommandHandler("anon", anon_cmd))
    app.add_handler(CommandHandler("faketask", faketask_cmd))

    # ── Voting Commands ────────────────────────────────────────
    app.add_handler(CommandHandler("vote", vote_cmd))
    app.add_handler(CommandHandler("meeting", meeting_cmd))

    # ── Settings Command (admin, per-group inline panel) ───────
    app.add_handler(CommandHandler("settings", settings_cmd))

    # ── Admin Commands ─────────────────────────────────────────
    app.add_handler(CommandHandler("endgame", endgame_cmd))
    app.add_handler(CommandHandler("addtask", addtask_cmd))
    app.add_handler(CommandHandler("listtasks", listtasks_cmd))
    app.add_handler(CommandHandler("deltask", deltask_cmd))
    app.add_handler(CommandHandler("settime", settime_cmd))
    app.add_handler(CommandHandler("kickplayer", kickplayer_cmd))
    app.add_handler(CommandHandler("pingall", pingall_cmd))

    # ── Owner Commands ─────────────────────────────────────────
    app.add_handler(CommandHandler("broadcast", broadcast_cmd))
    app.add_handler(CommandHandler("addpremium", addpremium_cmd))
    app.add_handler(CommandHandler("removepremium", removepremium_cmd))
    app.add_handler(CommandHandler("ownerstats", ownerstats_cmd))
    app.add_handler(CommandHandler("ban", banuser_cmd))
    app.add_handler(CommandHandler("unban", unbanuser_cmd))
    app.add_handler(CommandHandler("allgroups", allgroups_cmd))
    app.add_handler(CommandHandler("forceend", forceend_cmd))

    # ── Callback Queries ───────────────────────────────────────
    # Settings callbacks (s_ prefix) must be registered BEFORE the generic handler
    app.add_handler(CallbackQueryHandler(settings_callback, pattern=r"^s_"))
    app.add_handler(CallbackQueryHandler(button_callback))

    # ── DM catch-all (must be last) ───────────────────────────
    app.add_handler(MessageHandler(filters.ChatType.PRIVATE & ~filters.COMMAND, dm_message_handler))
