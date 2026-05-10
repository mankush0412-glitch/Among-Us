import logging
from datetime import datetime, timedelta
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

        # Create indexes for performance
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
        await self.db.users.update_one(
            {"user_id": user_id},
            {"$set": {
                "user_id": user_id,
                "username": username,
                "first_name": first_name,
                "chat_id": chat_id,
                "last_seen": datetime.utcnow()
            }, "$setOnInsert": {
                "is_premium": False,
                "is_banned": False,
                "premium_expires": None,
                "registered_at": datetime.utcnow()
            }},
            upsert=True
        )

    async def get_user(self, user_id: int):
        return await self.db.users.find_one({"user_id": user_id})

    async def get_user_by_username(self, username: str):
        return await self.db.users.find_one({"username": username})

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
            {"$set": {"group_id": group_id, "title": title, "is_active": True},
             "$setOnInsert": {"added_at": datetime.utcnow()}},
            upsert=True
        )

    async def get_all_groups(self):
        return await self.db.groups.find({"is_active": True}).to_list(None)

    # ─── Games ───────────────────────────────────────────────
    async def get_active_game(self, group_id: int):
        return await self.db.games.find_one(
            {"group_id": group_id, "status": {"$nin": ["ended", "cancelled"]}},
            sort=[("_id", -1)]
        )

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
    async def add_player(self, game_id: str, user_id: int):
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
            "scan_uses": Config.SCAN_USES,
            "shield_active": False,
            "anon_uses": Config.ANON_MESSAGES_PER_GAME,
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
        enriched = []
        for p in players:
            user = await self.get_user(p["user_id"])
            if user:
                p["username"] = user.get("username", "")
                p["first_name"] = user.get("first_name", "Player")
                p["chat_id"] = user.get("chat_id", 0)
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

    # ─── Tasks ───────────────────────────────────────────────
    async def post_task(self, game_id: str, group_id: int, task_text: str,
                        category: str, message_id: int = None) -> str:
        result = await self.db.tasks.insert_one({
            "game_id": game_id,
            "group_id": group_id,
            "task_text": task_text,
            "task_category": category,
            "assigned_to": None,
            "is_completed": False,
            "is_fake": False,
            "posted_at": datetime.utcnow(),
            "completed_at": None,
            "completed_by": None,
            "message_id": message_id
        })
        return str(result.inserted_id)

    async def complete_task(self, task_id: str, user_id: int):
        from bson import ObjectId
        await self.db.tasks.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": {"is_completed": True, "completed_by": user_id, "completed_at": datetime.utcnow()}}
        )

    async def get_active_task(self, game_id: str):
        return await self.db.tasks.find_one(
            {"game_id": game_id, "is_completed": False, "is_fake": False},
            sort=[("_id", -1)]
        )

    # ─── Votes ───────────────────────────────────────────────
    async def cast_vote(self, game_id: str, voter_id: int, target_id: int, phase: int) -> bool:
        existing = await self.db.votes.find_one({"game_id": game_id, "voter_id": voter_id, "phase": phase})
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
        pipeline = [
            {"$match": {"game_id": game_id, "phase": phase}},
            {"$group": {"_id": "$target_id", "vote_count": {"$sum": 1}}},
            {"$sort": {"vote_count": -1}}
        ]
        results = await self.db.votes.aggregate(pipeline).to_list(None)
        return [{"target_id": r["_id"], "vote_count": r["vote_count"]} for r in results]

    # ─── Scores ──────────────────────────────────────────────
    async def get_scores(self, group_id: int, limit: int = 10):
        scores = await self.db.scores.find(
            {"group_id": group_id}
        ).sort("total_points", -1).limit(limit).to_list(None)

        enriched = []
        for s in scores:
            user = await self.get_user(s["user_id"])
            if user:
                s["username"] = user.get("username", "")
                s["first_name"] = user.get("first_name", "Player")
                s["is_premium"] = user.get("is_premium", False)
            enriched.append(s)
        return enriched

    async def update_scores(self, user_id: int, group_id: int, points: int,
                            won: bool = False, role: str = "crewmate",
                            tasks: int = 0, kills: int = 0, correct_vote: bool = False):
        await self.db.scores.update_one(
            {"user_id": user_id, "group_id": group_id},
            {"$inc": {
                "total_points": points,
                "games_played": 1,
                "games_won": 1 if won else 0,
                "imposter_wins": 1 if (won and role == "imposter") else 0,
                "crew_wins": 1 if (won and role == "crewmate") else 0,
                "tasks_completed": tasks,
                "kills_made": kills,
                "correct_votes": 1 if correct_vote else 0
            }, "$setOnInsert": {
                "user_id": user_id,
                "group_id": group_id,
                "created_at": datetime.utcnow()
            }},
            upsert=True
        )

    # ─── Premium ─────────────────────────────────────────────
    async def add_premium(self, user_id: int, granted_by: int, days: int):
        expires_at = datetime.utcnow() + timedelta(days=days)
        await self.db.users.update_one(
            {"user_id": user_id},
            {"$set": {"is_premium": True, "premium_expires": expires_at}}
        )
        await self.db.premium_users.update_one(
            {"user_id": user_id},
            {"$set": {"user_id": user_id, "granted_by": granted_by,
                      "expires_at": expires_at, "granted_at": datetime.utcnow()}},
            upsert=True
        )
        return expires_at

    async def remove_premium(self, user_id: int):
        await self.db.users.update_one(
            {"user_id": user_id},
            {"$set": {"is_premium": False, "premium_expires": None}}
        )
        await self.db.premium_users.delete_one({"user_id": user_id})

    # ─── Custom Tasks ────────────────────────────────────────
    async def add_custom_task(self, group_id: int, task_text: str, added_by: int):
        await self.db.custom_tasks.insert_one({
            "group_id": group_id,
            "task_text": task_text,
            "added_by": added_by,
            "category": "custom",
            "added_at": datetime.utcnow()
        })

    async def get_custom_tasks(self, group_id: int):
        return await self.db.custom_tasks.find({"group_id": group_id}).to_list(None)

    async def delete_custom_task(self, group_id: int, task_text: str):
        result = await self.db.custom_tasks.delete_one(
            {"group_id": group_id, "task_text": {"$regex": task_text, "$options": "i"}}
        )
        return result.deleted_count > 0

    async def list_custom_tasks(self, group_id: int):
        tasks = await self.get_custom_tasks(group_id)
        return tasks

    # ─── Broadcasts ──────────────────────────────────────────
    async def save_broadcast(self, message: str, sent_by: int, groups_reached: int):
        await self.db.broadcasts.insert_one({
            "message": message,
            "sent_by": sent_by,
            "sent_at": datetime.utcnow(),
            "groups_reached": groups_reached
        })

    # ─── Global Stats ────────────────────────────────────────
    async def get_global_stats(self) -> dict:
        users = await self.db.users.count_documents({})
        groups = await self.db.groups.count_documents({"is_active": True})
        games = await self.db.games.count_documents({"status": "ended"})
        premium = await self.db.users.count_documents({"is_premium": True})
        return {"users": users, "groups": groups, "games": games, "premium": premium}

    # ─── Game by ID ──────────────────────────────────────────
    async def get_game_by_id(self, game_id: str):
        from bson import ObjectId
        try:
            return await self.db.games.find_one({"_id": ObjectId(game_id)})
        except Exception:
            return None

    # ─── Phase helper ─────────────────────────────────────────
    async def get_current_phase(self, game_id: str) -> int:
        pipeline = [
            {"$match": {"game_id": game_id}},
            {"$group": {"_id": None, "max_phase": {"$max": "$phase"}}}
        ]
        result = await self.db.votes.aggregate(pipeline).to_list(1)
        if result and result[0].get("max_phase") is not None:
            return result[0]["max_phase"]
        return 1

    async def get_next_phase(self, game_id: str) -> int:
        return (await self.get_current_phase(game_id)) + 1

    # ─── Remove player ────────────────────────────────────────
    async def remove_player(self, game_id: str, user_id: int):
        await self.db.game_players.delete_one({"game_id": game_id, "user_id": user_id})

    # ─── Task by ID ───────────────────────────────────────────
    async def get_task_by_id(self, task_id: str):
        from bson import ObjectId
        try:
            return await self.db.tasks.find_one({"_id": ObjectId(task_id)})
        except Exception:
            return None

    async def get_recent_tasks(self, game_id: str, limit: int = 5):
        return await self.db.tasks.find(
            {"game_id": game_id, "is_completed": False, "is_fake": False}
        ).sort("_id", -1).limit(limit).to_list(None)

    async def get_task_count(self, game_id: str) -> int:
        return await self.db.tasks.count_documents({"game_id": game_id})

    # ─── Fetchone/fetchall helpers (for owner/admin handlers) ─
    async def fetchone(self, collection: str, query: dict):
        return await self.db[collection].find_one(query)

    async def fetchall(self, collection: str, query: dict = None, sort=None, limit=0):
        cursor = self.db[collection].find(query or {})
        if sort:
            cursor = cursor.sort(sort)
        if limit:
            cursor = cursor.limit(limit)
        return await cursor.to_list(None)
