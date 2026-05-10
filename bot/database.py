import logging
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from bot.config import Config

logger = logging.getLogger(__name__)


class Database:
    def __init__(self):
        self.client: AsyncIOMotorClient = None
        self.db = None

    async def initialize(self):
        self.client = AsyncIOMotorClient(Config.MONGODB_URI)
        self.db = self.client[Config.DB_NAME]

        await self.db.users.create_index("user_id", unique=True)
        await self.db.groups.create_index("group_id", unique=True)
        await self.db.games.create_index([("group_id", 1), ("status", 1)])
        await self.db.game_players.create_index([("game_id", 1), ("user_id", 1)])
        await self.db.votes.create_index([("game_id", 1), ("voter_id", 1), ("phase", 1)])
        await self.db.scores.create_index([("user_id", 1), ("group_id", 1)], unique=True)
        await self.db.custom_tasks.create_index("group_id")
        await self.db.tasks.create_index([("game_id", 1), ("is_completed", 1)])
        logger.info("✅ MongoDB connected and indexes created")

    async def close(self):
        if self.client:
            self.client.close()

    # ─── Users ───────────────────────────────────────────────
    async def register_user(self, user_id: int, username: str, first_name: str, chat_id: int):
        update_fields = {
            "user_id": user_id,
            "username": username,
            "first_name": first_name,
            "last_seen": datetime.utcnow()
        }
        if chat_id is not None:
            update_fields["chat_id"] = chat_id

        await self.db.users.update_one(
            {"user_id": user_id},
            {
                "$set": update_fields,
                "$setOnInsert": {
                    "is_premium": False,
                    "is_banned": False,
                    "premium_expires": None,
                    "registered_at": datetime.utcnow()
                }
            },
            upsert=True
        )

    async def get_user(self, user_id: int):
        return await self.db.users.find_one({"user_id": user_id})

    async def get_user_by_username(self, username: str):
        return await self.db.users.find_one({"username": username})

    async def get_user_by_id(self, user_id: int):
        return await self.db.users.find_one({"user_id": user_id})

    async def ban_user(self, user_id: int):
        await self.db.users.update_one({"user_id": user_id}, {"$set": {"is_banned": True}})

    async def unban_user(self, user_id: int):
        await self.db.users.update_one({"user_id": user_id}, {"$set": {"is_banned": False}})

    async def is_premium(self, user_id: int) -> bool:
        user = await self.get_user(user_id)
        if not user:
            return False
        if not user.get("is_premium"):
            return False
        exp = user.get("premium_expires")
        if exp and exp < datetime.utcnow():
            await self.db.users.update_one({"user_id": user_id}, {"$set": {"is_premium": False}})
            return False
        return True

    # ─── Groups ──────────────────────────────────────────────
    async def register_group(self, group_id: int, title: str):
        await self.db.groups.update_one(
            {"group_id": group_id},
            {
                "$set": {"group_id": group_id, "title": title, "is_active": True},
                "$setOnInsert": {
                    "added_at": datetime.utcnow(),
                    "settings": {},
                    "last_task_at": None
                }
            },
            upsert=True
        )

    async def get_all_groups(self):
        return await self.db.groups.find({"is_active": True}).to_list(None)

    # ─── Group Settings ───────────────────────────────────────
    async def get_group_settings(self, group_id: int) -> dict:
        group = await self.db.groups.find_one({"group_id": group_id})
        if group:
            return group.get("settings", {})
        return {}

    async def update_group_setting(self, group_id: int, key: str, value):
        await self.db.groups.update_one(
            {"group_id": group_id},
            {"$set": {f"settings.{key}": value}},
            upsert=True
        )

    async def update_group_last_task_at(self, group_id: int):
        await self.db.groups.update_one(
            {"group_id": group_id},
            {"$set": {"last_task_at": datetime.utcnow()}}
        )

    async def get_group_cfg(self, group_id: int) -> dict:
        """
        Returns the effective config for a group.
        ALL interval timers (task, kill, sabotage, score) are in MINUTES.
        """
        defaults = {
            "points_task":         Config.POINTS_TASK_COMPLETE,
            "points_imposter_win": Config.POINTS_IMPOSTER_WIN,
            "points_crew_win":     Config.POINTS_CREW_WIN,
            "points_correct_vote": Config.POINTS_CORRECT_VOTE,
            "points_wrong_vote":   Config.POINTS_WRONG_VOTE,
            # ── All intervals in MINUTES ──
            "kill_cooldown":       Config.KILL_COOLDOWN_MINUTES,       # minutes
            "sabotage_cooldown":   Config.SABOTAGE_COOLDOWN_MINUTES,   # minutes
            "scan_uses":           Config.SCAN_USES,
            "shield_uses":         Config.SHIELD_USES,
            "anon_uses":           Config.ANON_MESSAGES_PER_GAME,
            "max_meetings":        Config.MAX_EMERGENCY_MEETINGS,
            "task_interval":       Config.TASK_INTERVAL_MINUTES,       # minutes
            "voting_hour":         Config.VOTING_START_HOUR,           # 0–23 UTC
            "reveal_hour":         Config.REVEAL_HOUR,                 # 0–23 UTC
            "score_interval":      Config.SCORE_INTERVAL_MINUTES,      # minutes
        }
        stored = await self.get_group_settings(group_id)

        # ── Migrate old hours-based values if they exist ──────────────────
        # (for anyone upgrading from the old version)
        migrations = {
            "task_interval_hours":       ("task_interval",      60),
            "kill_cooldown_hours":        ("kill_cooldown",      60),
            "sabotage_cooldown_hours":    ("sabotage_cooldown",  60),
            "score_interval_hours":       ("score_interval",     60),
        }
        for old_key, (new_key, multiplier) in migrations.items():
            if old_key in stored and new_key not in stored:
                stored[new_key] = stored.pop(old_key) * multiplier

        return {**defaults, **stored}

    # ─── Games ───────────────────────────────────────────────
    async def get_active_game(self, group_id: int):
        return await self.db.games.find_one(
            {"group_id": group_id, "status": {"$nin": ["ended", "cancelled"]}},
            sort=[("_id", -1)]
        )

    async def get_active_game_for_user(self, user_id: int):
        """
        Find any active game the user is currently a live player in.
        Returns (game_doc, group_id) or (None, None).
        """
        player_docs = await self.db.game_players.find(
            {"user_id": user_id, "is_alive": True}
        ).to_list(None)

        for p in player_docs:
            game = await self.get_game_by_id(p["game_id"])
            if game and game["status"] in ("active", "voting"):
                return game, game["group_id"]
        return None, None

    async def get_game_by_id(self, game_id: str):
        from bson import ObjectId
        try:
            return await self.db.games.find_one({"_id": ObjectId(game_id)})
        except Exception:
            return None

    async def create_game(self, group_id: int, started_by: int) -> str:
        from bson import ObjectId
        result = await self.db.games.insert_one({
            "group_id": group_id,
            "started_by": started_by,
            "status": "waiting",
            "started_at": datetime.utcnow(),
            "ended_at": None,
            "winner_role": None
        })
        return str(result.inserted_id)

    async def update_game_status(self, game_id: str, status: str):
        from bson import ObjectId
        update = {"$set": {"status": status}}
        if status in ("ended", "cancelled"):
            update["$set"]["ended_at"] = datetime.utcnow()
        await self.db.games.update_one({"_id": ObjectId(game_id)}, update)

    async def set_game_winner(self, game_id: str, winner_role: str):
        from bson import ObjectId
        await self.db.games.update_one(
            {"_id": ObjectId(game_id)},
            {"$set": {"winner_role": winner_role, "status": "ended", "ended_at": datetime.utcnow()}}
        )

    # ─── Players ─────────────────────────────────────────────
    async def add_player(self, game_id: str, user_id: int,
                         scan_uses: int = None, anon_uses: int = None, shield_uses: int = None):
        existing = await self.db.game_players.find_one({"game_id": game_id, "user_id": user_id})
        if existing:
            return
        await self.db.game_players.insert_one({
            "game_id": game_id,
            "user_id": user_id,
            "role": "crewmate",
            "is_alive": True,
            "points": 0,
            "tasks_done": 0,
            "kills_done": 0,
            "shields_used": 0,
            "emergency_used": 0,
            "scan_uses":    scan_uses   if scan_uses   is not None else Config.SCAN_USES,
            "shield_active": False,
            "anon_uses":    anon_uses   if anon_uses   is not None else Config.ANON_MESSAGES_PER_GAME,
            "max_shields":  shield_uses if shield_uses is not None else Config.SHIELD_USES,
            "last_kill": None,
            "last_sabotage": None,
            "watching_user": None,
            "joined_at": datetime.utcnow()
        })

    async def set_player_role(self, game_id: str, user_id: int, role: str):
        await self.db.game_players.update_one(
            {"game_id": game_id, "user_id": user_id},
            {"$set": {"role": role}}
        )

    async def get_players(self, game_id: str):
        players = await self.db.game_players.find({"game_id": game_id}).to_list(None)
        return await self._enrich_players(players)

    async def get_alive_players(self, game_id: str):
        players = await self.db.game_players.find(
            {"game_id": game_id, "is_alive": True}
        ).to_list(None)
        return await self._enrich_players(players)

    async def get_player(self, game_id: str, user_id: int):
        player = await self.db.game_players.find_one({"game_id": game_id, "user_id": user_id})
        if not player:
            return None
        enriched = await self._enrich_players([player])
        return enriched[0] if enriched else None

    async def _enrich_players(self, players: list):
        """
        Batch-fetch all user docs in ONE query instead of N separate calls.
        This eliminates the N+1 performance problem that caused slow responses.
        """
        if not players:
            return []

        user_ids = [p["user_id"] for p in players]
        user_docs = await self.db.users.find(
            {"user_id": {"$in": user_ids}}
        ).to_list(None)

        user_map = {u["user_id"]: u for u in user_docs}

        enriched = []
        for p in players:
            user = user_map.get(p["user_id"])
            if user:
                p["username"]   = user.get("username", "")
                p["first_name"] = user.get("first_name", "Player")
                p["chat_id"]    = user.get("chat_id", 0)
                p["is_premium"] = user.get("is_premium", False)
            enriched.append(p)
        return enriched

    async def kill_player(self, game_id: str, user_id: int):
        await self.db.game_players.update_one(
            {"game_id": game_id, "user_id": user_id},
            {"$set": {"is_alive": False}}
        )

    async def add_points(self, game_id: str, user_id: int, points: int):
        await self.db.game_players.update_one(
            {"game_id": game_id, "user_id": user_id},
            {"$inc": {"points": points}}
        )

    async def increment_tasks(self, game_id: str, user_id: int):
        await self.db.game_players.update_one(
            {"game_id": game_id, "user_id": user_id},
            {"$inc": {"tasks_done": 1}}
        )

    async def update_player_field(self, game_id: str, user_id: int, field: str, value):
        await self.db.game_players.update_one(
            {"game_id": game_id, "user_id": user_id},
            {"$set": {field: value}}
        )

    # ─── Votes ───────────────────────────────────────────────
    async def cast_vote(self, game_id: str, voter_id: int, target_id: int, phase: int) -> bool:
        existing = await self.db.votes.find_one(
            {"game_id": game_id, "voter_id": voter_id, "phase": phase}
        )
        if existing:
            return False
        await self.db.votes.insert_one({
            "game_id": game_id,
            "voter_id": voter_id,
            "target_id": target_id,
            "phase": phase,
            "voted_at": datetime.utcnow()
        })
        return True

    async def get_votes(self, game_id: str, phase: int):
        from collections import Counter
        votes = await self.db.votes.find(
            {"game_id": game_id, "phase": phase}
        ).to_list(None)
        if not votes:
            return []
        counts = Counter(v["target_id"] for v in votes)
        return [{"target_id": tid, "count": cnt}
                for tid, cnt in counts.most_common()]

    async def get_vote_count(self, game_id: str, phase: int) -> int:
        return await self.db.votes.count_documents(
            {"game_id": game_id, "phase": phase}
        )

    async def get_current_phase(self, game_id: str) -> int:
        last = await self.db.votes.find_one(
            {"game_id": game_id},
            sort=[("phase", -1)]
        )
        return last["phase"] if last else 1

    async def get_next_phase(self, game_id: str) -> int:
        phase = await self.get_current_phase(game_id)
        return phase + 1 if await self.get_vote_count(game_id, phase) > 0 else phase

    # ─── Tasks ───────────────────────────────────────────────
    async def post_task(self, game_id: str, group_id: int, task_text: str,
                        category: str, message_id: int) -> str:
        from bson import ObjectId
        result = await self.db.tasks.insert_one({
            "game_id": game_id,
            "group_id": group_id,
            "task_text": task_text,
            "category": category,
            "message_id": message_id,
            "is_completed": False,
            "completed_by": None,
            "posted_at": datetime.utcnow()
        })
        return str(result.inserted_id)

    async def get_task_by_id(self, task_id: str):
        from bson import ObjectId
        try:
            return await self.db.tasks.find_one({"_id": ObjectId(task_id)})
        except Exception:
            return None

    async def complete_task(self, task_id: str, user_id: int):
        from bson import ObjectId
        await self.db.tasks.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": {"is_completed": True, "completed_by": user_id,
                      "completed_at": datetime.utcnow()}}
        )

    async def get_task_count(self, game_id: str) -> int:
        return await self.db.tasks.count_documents({"game_id": game_id})

    async def get_custom_tasks(self, group_id: int):
        return await self.db.custom_tasks.find({"group_id": group_id}).to_list(None)

    async def add_custom_task(self, group_id: int, task_text: str, added_by: int):
        await self.db.custom_tasks.insert_one({
            "group_id": group_id,
            "task_text": task_text,
            "added_by": added_by,
            "added_at": datetime.utcnow()
        })

    # ─── Scores ──────────────────────────────────────────────
    async def update_scores(self, user_id: int, group_id: int, points: int,
                             won: bool, role: str, tasks: int, kills: int):
        await self.db.scores.update_one(
            {"user_id": user_id, "group_id": group_id},
            {
                "$inc": {
                    "total_points": points,
                    "games_played": 1,
                    "games_won": 1 if won else 0,
                    "tasks_done": tasks,
                    "kills_done": kills,
                    "imposter_games": 1 if role == "imposter" else 0,
                    "crew_games": 1 if role == "crewmate" else 0,
                },
                "$setOnInsert": {"user_id": user_id, "group_id": group_id}
            },
            upsert=True
        )

    async def get_scores(self, group_id: int, limit: int = 10):
        pipeline = [
            {"$match": {"group_id": group_id}},
            {"$sort": {"total_points": -1}},
            {"$limit": limit},
            {"$lookup": {
                "from": "users",
                "localField": "user_id",
                "foreignField": "user_id",
                "as": "user_info"
            }},
            {"$unwind": {"path": "$user_info", "preserveNullAndEmptyArrays": True}},
            {"$addFields": {
                "first_name": "$user_info.first_name",
                "username":   "$user_info.username",
                "is_premium": "$user_info.is_premium"
            }}
        ]
        return await self.db.scores.aggregate(pipeline).to_list(None)

    async def get_user_score(self, user_id: int, group_id: int):
        return await self.db.scores.find_one({"user_id": user_id, "group_id": group_id})

    # ─── Generic helpers ─────────────────────────────────────
    async def fetchone(self, collection: str, query: dict):
        return await self.db[collection].find_one(query)

    async def fetchall(self, collection: str, query: dict):
        return await self.db[collection].find(query).to_list(None)
