from dataclasses import dataclass, field
from typing import List
from bot.config import Config


@dataclass
class Role:
    name: str
    display: str
    emoji: str
    color: str
    description: str
    abilities: List[str]
    win_condition: str


IMPOSTER_ROLE = Role(
    name="imposter",
    display="Impostor",
    emoji="🔴",
    color="red",
    description="Sabotage tasks and eliminate crewmates without getting caught!",
    abilities=["kill", "vent", "sabotage", "anon", "faketask"],
    win_condition="Eliminate enough crewmates or survive the vote."
)

CREWMATE_ROLE = Role(
    name="crewmate",
    display="Crewmate",
    emoji="🟢",
    color="green",
    description="Complete tasks and find the Impostor before it's too late!",
    abilities=["scan", "shield", "report", "watch", "vote"],
    win_condition="Vote out the Impostor or complete all tasks."
)

GHOST_ROLE = Role(
    name="ghost",
    display="Ghost",
    emoji="👻",
    color="gray",
    description="You've been eliminated but can still watch the game.",
    abilities=["observe"],
    win_condition="Cheer for your team!"
)


def get_role(role_name: str) -> Role:
    roles = {
        "imposter": IMPOSTER_ROLE,
        "crewmate": CREWMATE_ROLE,
        "ghost": GHOST_ROLE
    }
    return roles.get(role_name, CREWMATE_ROLE)


def role_dm_header(role_name: str) -> str:
    if role_name == "imposter":
        return """
🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴
⚠️  YOU ARE THE IMPOSTOR  ⚠️
🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴

Keep this SECRET. Act like a crewmate.
Eliminate players. Win the game.
"""
    else:
        return """
🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢
👷  YOU ARE A CREWMATE  👷
🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢

Complete tasks. Find the Impostor. Trust no one.
"""


def get_role_abilities_text(role_name: str) -> str:
    if role_name == "imposter":
        return (
            "🔪 /kill @player — Eliminate a crewmate\n"
            "🌀 /vent — Teleport between rooms\n"
            "💣 /sabotage — Trigger group emergency\n"
            "📨 /anon [msg] — Send anonymous message\n"
            "📋 /faketask — Announce fake task completion\n"
            f"\n⚡ Kill cooldown: {Config.KILL_COOLDOWN_HOURS}h\n"
            f"📨 Anon uses: {Config.ANON_MESSAGES_PER_GAME}/game"
        )
    else:
        return (
            "🔍 /scan @player — Get a sus hint\n"
            "🛡 /shield — Protect yourself from one kill\n"
            "📢 /report — Call emergency meeting\n"
            "👁 /watch @player — Track their activity\n"
            "🗳️ /vote @player — Vote to eject\n"
            f"\n🔍 Scan uses: {Config.SCAN_USES}/game\n"
            f"🛡 Shield uses: {Config.SHIELD_USES}/game"
        )
