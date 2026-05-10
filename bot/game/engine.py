import random
import logging
from datetime import datetime
from bot.database import Database
from bot.config import Config
from bot.utils.helpers import calculate_imposters, pick_imposters, send_dm, get_display_name
from bot.utils.messages import (
    game_start_msg, IMPOSTER_DM_MSG, CREWMATE_DM_MSG,
    eject_msg, game_over_imposter_wins, game_over_crew_wins, kill_announcement
)
from bot.game.roles import get_role_abilities_text, role_dm_header

logger = logging.getLogger(__name__)


class GameEngine:
    def __init__(self, db: Database):
        self.db = db

    async def create_game(self, group_id: int, started_by: int) -> str:
        existing = await self.db.get_active_game(group_id)
        if existing and existing["status"] in ("waiting", "active", "voting"):
            return None
        game_id = await self.db.create_game(group_id, started_by)
        return game_id

    async def add_player(self, game_id: str, user_id: int) -> bool:
        game = await self.db.get_game_by_id(game_id)
        if not game or game["status"] not in ("waiting",):
            return False
        existing = await self.db.get_player(game_id, user_id)
        if existing:
            return False
        await self.db.add_player(game_id, user_id)
        return True

    async def start_game(self, bot, game_id: str, group_id: int) -> dict:
        players = await self.db.get_players(game_id)
        if len(players) < 3:
            return {"success": False, "reason": "Need at least 3 players to start!"}

        imposter_count = calculate_imposters(len(players))
        imposter_ids = pick_imposters(players, imposter_count)

        for player in players:
            role = "imposter" if player["user_id"] in imposter_ids else "crewmate"
            await self.db.set_player_role(game_id, player["user_id"], role)

        await self.db.update_game_status(game_id, "active")

        for player in players:
            role = "imposter" if player["user_id"] in imposter_ids else "crewmate"
            chat_id = player.get("chat_id")
            if chat_id:
                header = role_dm_header(role)
                abilities = get_role_abilities_text(role)
                dm_text = f"{header}\n🛠️ **Your Abilities:**\n{abilities}"
                await send_dm(bot, chat_id, dm_text)

        return {
            "success": True,
            "player_count": len(players),
            "imposter_count": imposter_count
        }

    async def process_kill(self, bot, game_id: str, group_id: int,
                           killer_id: int, target_id: int) -> dict:
        killer = await self.db.get_player(game_id, killer_id)
        target = await self.db.get_player(game_id, target_id)

        if not killer or killer["role"] != "imposter":
            return {"success": False, "reason": "Only Impostors can kill!"}
        if not killer["is_alive"]:
            return {"success": False, "reason": "You're a ghost, you can't kill!"}
        if not target or not target["is_alive"]:
            return {"success": False, "reason": "Target is already dead or doesn't exist!"}
        if target["role"] == "imposter":
            return {"success": False, "reason": "You can't kill your fellow Impostor!"}
        if target_id == killer_id:
            return {"success": False, "reason": "You can't kill yourself!"}

        if killer.get("last_kill"):
            last = datetime.fromisoformat(killer["last_kill"])
            diff = (datetime.now() - last).total_seconds() / 3600
            if diff < Config.KILL_COOLDOWN_HOURS:
                remaining = round(Config.KILL_COOLDOWN_HOURS - diff, 1)
                return {"success": False, "reason": f"Kill on cooldown! Wait {remaining}h more."}

        if target.get("shield_active"):
            await self.db.update_player_field(game_id, target_id, "shield_active", False)
            return {"success": False, "reason": "Target had a shield! Kill blocked. Shield consumed.", "shielded": True}

        await self.db.kill_player(game_id, target_id)
        await self.db.update_player_field(game_id, killer_id, "last_kill", datetime.now().isoformat())
        await self.db.update_player_field(game_id, killer_id, "kills_done",
                                          (killer.get("kills_done") or 0) + 1)
        await self.db.add_points(game_id, killer_id, 5)

        killer_name = get_display_name(killer)
        victim_name = get_display_name(target)

        if target.get("chat_id"):
            await send_dm(bot, target["chat_id"],
                          "💀 You have been eliminated! You're now a Ghost. You can still watch the game.")

        await self.check_win_condition(bot, game_id, group_id)

        return {
            "success": True,
            "victim_name": victim_name,
            "announcement": kill_announcement(killer_name, victim_name)
        }

    async def process_vote(self, game_id: str, voter_id: int, target_id: int, phase: int) -> dict:
        voter = await self.db.get_player(game_id, voter_id)
        if not voter:
            return {"success": False, "reason": "You're not in this game!"}
        if not voter["is_alive"]:
            return {"success": False, "reason": "Ghosts can't vote!"}

        success = await self.db.cast_vote(game_id, voter_id, target_id, phase)
        if not success:
            return {"success": False, "reason": "You already voted this round!"}

        return {"success": True}

    async def process_eject(self, bot, game_id: str, group_id: int, phase: int) -> dict:
        votes = await self.db.get_votes(game_id, phase)
        if not votes:
            return {"ejected": False, "message": "No votes were cast. Skipping eject."}

        top_vote = votes[0]
        target_id = top_vote["target_id"]

        if target_id == 0:
            return {"ejected": False, "message": "🗳️ Vote was skipped. No one was ejected!"}

        target = await self.db.get_player(game_id, target_id)
        if not target:
            return {"ejected": False, "message": "Vote target not found."}

        was_imposter = target["role"] == "imposter"
        target_name = get_display_name(target)

        await self.db.kill_player(game_id, target_id)

        if was_imposter:
            await self.db.add_points(game_id, target_id, -10)
        else:
            await self.db.add_points(game_id, target_id, -5)

        # Reward voters who voted correctly
        voters = await self.db.fetchall("votes", {
            "game_id": game_id, "phase": phase, "target_id": target_id
        })
        for v in voters:
            if was_imposter:
                await self.db.add_points(game_id, v["voter_id"], Config.POINTS_CORRECT_VOTE)
            else:
                await self.db.add_points(game_id, v["voter_id"], Config.POINTS_WRONG_VOTE)

        message = eject_msg(target_name, was_imposter, target["role"])
        win_result = await self.check_win_condition(bot, game_id, group_id)

        return {
            "ejected": True,
            "target_name": target_name,
            "was_imposter": was_imposter,
            "message": message,
            "game_over": win_result.get("game_over", False)
        }

    async def check_win_condition(self, bot, game_id: str, group_id: int) -> dict:
        alive_players = await self.db.get_alive_players(game_id)
        alive_imposters = [p for p in alive_players if p["role"] == "imposter"]
        alive_crew = [p for p in alive_players if p["role"] == "crewmate"]

        if not alive_imposters:
            await self._end_game(bot, game_id, group_id, "crewmate")
            return {"game_over": True, "winner": "crewmate"}

        if len(alive_imposters) >= len(alive_crew):
            await self._end_game(bot, game_id, group_id, "imposter")
            return {"game_over": True, "winner": "imposter"}

        return {"game_over": False}

    async def _end_game(self, bot, game_id: str, group_id: int, winner: str):
        await self.db.set_game_winner(game_id, winner)

        all_players = await self.db.get_players(game_id)
        imposters = [p for p in all_players if p["role"] == "imposter"]
        imposter_name = get_display_name(imposters[0]) if imposters else "Unknown"

        for player in all_players:
            role = player["role"]
            won = (role == winner)
            points = player.get("points") or 0
            bonus = Config.POINTS_IMPOSTER_WIN if (role == "imposter" and won) else \
                (Config.POINTS_CREW_WIN if (role == "crewmate" and won) else 0)
            total = points + bonus

            await self.db.update_scores(
                user_id=player["user_id"],
                group_id=group_id,
                points=total,
                won=won,
                role=role,
                tasks=player.get("tasks_done") or 0,
                kills=player.get("kills_done") or 0
            )

        if winner == "imposter":
            msg = game_over_imposter_wins(imposter_name)
        else:
            msg = game_over_crew_wins(imposter_name)

        try:
            await bot.send_message(chat_id=group_id, text=msg, parse_mode="Markdown")
        except Exception as e:
            logger.error(f"Failed to send game over message: {e}")

    async def get_game_status(self, game_id: str) -> dict:
        game = await self.db.get_game_by_id(game_id)
        players = await self.db.get_players(game_id)
        alive = [p for p in players if p["is_alive"]]
        return {
            "game": game,
            "total_players": len(players),
            "alive_players": len(alive),
            "players": players
        }
