import random

RANDOM_EVENTS = [
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # BONUS & REWARD EVENTS
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    {"type": "bonus_task", "message": "⭐ BONUS ROUND! Next task is worth DOUBLE points! (20 pts)", "effect": "double_points"},
    {"type": "mystery_points", "message": "🎁 A mystery reward dropped! First person to type 'CLAIM' gets +25 points!", "effect": "claim_reward"},
    {"type": "crew_boost", "message": "🚀 Crewmate morale is HIGH! All alive crewmates get +5 bonus points!", "effect": "crew_boost"},
    {"type": "task_blitz", "message": "⚡ TASK BLITZ! 3 rapid-fire tasks incoming! Complete all 3 for +30 bonus points!", "effect": "blitz"},
    {"type": "speed_bonus", "message": "🏃 SPEED ROUND! Next 5 minutes — all correct answers get +5 extra points!", "effect": "speed_bonus"},
    {"type": "triple_points", "message": "🔥 TRIPLE SCORE EVENT! Next task answer = 3× points! Be fast!", "effect": "triple_points"},
    {"type": "mystery_gift", "message": "🎀 Secret gift incoming! Random player will get +20 points in 10 seconds!", "effect": "random_points"},
    {"type": "streak_bonus", "message": "🔗 STREAK BONUS! Player with most task completions today gets +15 extra points!", "effect": "streak"},
    {"type": "jackpot", "message": "💰 JACKPOT ALERT! First person to say 'JACKPOT' in chat gets +35 points!", "effect": "jackpot"},
    {"type": "comeback", "message": "💪 COMEBACK EVENT! Player with least points gets +20 points free! Keep fighting!", "effect": "comeback"},
    {"type": "team_reward", "message": "🤝 TEAM EVENT! If 5+ players complete next task, everyone gets +10 bonus!", "effect": "team_reward"},
    {"type": "hot_minute", "message": "🌡️ HOT MINUTE! Answer anything in the next 60 seconds for +15 bonus points!", "effect": "hot_minute"},
    {"type": "double_kill_reward", "message": "🔪 ASSASSIN REWARD! First player to use /kill today gets +10 bonus points!", "effect": "kill_reward"},
    {"type": "first_blood", "message": "🩸 FIRST BLOOD BONUS! First successful action this hour gets +20 points!", "effect": "first_blood"},
    {"type": "survivor_reward", "message": "🛡️ SURVIVOR BONUS! All alive players get +5 for still being in the game!", "effect": "survivor"},
    {"type": "trivia_storm", "message": "🌊 TRIVIA STORM! 5 rapid questions are coming! Each worth 15 points!", "effect": "trivia_storm"},
    {"type": "random_prize", "message": "🎲 LUCKY DRAW! One random player will win 30 points right now!", "effect": "lucky_draw"},
    {"type": "perfect_score", "message": "💯 PERFECTION BONUS! Get the next 3 tasks right for a 25 point bonus!", "effect": "perfect_score"},
    {"type": "activity_bonus", "message": "🎯 ACTIVITY REWARD! Most active player of the hour gets +20 points!", "effect": "activity"},
    {"type": "marathon_bonus", "message": "🏅 MARATHON BONUS! Players who've been active 6+ hours get +15 points!", "effect": "marathon"},

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # CHALLENGE EVENTS
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    {"type": "lockdown", "message": "🔒 LOCKDOWN! No abilities for the next 10 minutes. Complete 2 tasks to unlock!", "effect": "lockdown"},
    {"type": "blackout", "message": "🌑 BLACKOUT! No one can use abilities for 5 minutes. Survive!", "effect": "blackout"},
    {"type": "task_rush", "message": "⏰ TASK RUSH! Complete a task in the next 2 minutes or lose 5 points!", "effect": "task_rush"},
    {"type": "silence", "message": "🤫 SILENCE EVENT! No messages for 60 seconds. Violators lose 10 points!", "effect": "silence"},
    {"type": "reverse_day", "message": "🔄 REVERSE DAY! For next 10 minutes, impostors get task points, crewmates get nothing!", "effect": "reverse"},
    {"type": "chaos_mode", "message": "💥 CHAOS MODE! All cooldowns reset! Everyone has abilities again right now!", "effect": "chaos"},
    {"type": "freeze", "message": "🧊 DEEP FREEZE! All kills are blocked for the next 15 minutes!", "effect": "freeze"},
    {"type": "no_shields", "message": "🛡️ SHIELD BREAKER! All shields are disabled for 10 minutes!", "effect": "no_shields"},
    {"type": "vote_block", "message": "🚫 VOTE LOCK! Emergency meetings disabled for next 20 minutes!", "effect": "vote_block"},
    {"type": "identity_crisis", "message": "🎭 IDENTITY CRISIS! Everyone's display name is hidden for 10 minutes!", "effect": "identity"},
    {"type": "double_damage", "message": "💀 DOUBLE THREAT! Next kill attempt removes 2 abilities from the victim!", "effect": "double_damage"},
    {"type": "penalty_round", "message": "⚠️ PENALTY ROUND! Wrong answer in next task = -15 points. Be careful!", "effect": "penalty"},
    {"type": "speed_kill", "message": "⚡ BLITZ KILL! Kill cooldown reduced to 0 for next 5 minutes!", "effect": "speed_kill"},
    {"type": "scramble", "message": "🌀 SCRAMBLE! Scan results are inverted for next 15 minutes!", "effect": "scramble"},
    {"type": "dark_mode", "message": "🌚 DARK MODE! No task hints for next 30 minutes. Raw knowledge only!", "effect": "dark_mode"},
    {"type": "hard_mode", "message": "💪 HARD MODE! Next 3 tasks have double the difficulty!", "effect": "hard_mode"},
    {"type": "sudden_death", "message": "☠️ SUDDEN DEATH! Next player to get 3 wrong answers is penalized -25 points!", "effect": "sudden_death"},
    {"type": "power_surge", "message": "⚡ POWER SURGE! All ability cooldowns reset for everyone right now!", "effect": "power_surge"},
    {"type": "task_bomb", "message": "💣 TASK BOMB! Complete 3 tasks before the timer or lose 10 points each!", "effect": "task_bomb"},
    {"type": "traitor_hunt", "message": "🕵️ TRAITOR HUNT! Enhanced voting — one vote = worth 2 in next meeting!", "effect": "traitor_hunt"},

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # INVESTIGATION EVENTS
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    {"type": "spy_report", "message": "🕵️ INTEL BREACH! A random player's room location has been leaked to everyone!", "effect": "spy_report"},
    {"type": "impostor_hint", "message": "👀 SYSTEM ALERT: Unusual activity detected. Someone was near the vents...", "effect": "impostor_hint"},
    {"type": "camera_feed", "message": "📹 SECURITY CAMS ONLINE! Suspicious movement logged in 2 rooms. Investigate!", "effect": "camera"},
    {"type": "admin_leak", "message": "📡 ADMIN BREACH! Player positions visible on admin panel for next 5 minutes!", "effect": "admin_leak"},
    {"type": "lie_detector", "message": "🔍 LIE DETECTOR ACTIVE! Next player to make a false claim loses 15 points!", "effect": "lie_detector"},
    {"type": "footprint", "message": "👣 FOOTPRINTS FOUND! A trail leads from the crime scene... follow it!", "effect": "footprint"},
    {"type": "anonymous_tip", "message": "📧 ANONYMOUS TIP RECEIVED! 'The impostor has used a vent in the last hour...'", "effect": "anon_tip"},
    {"type": "blood_trail", "message": "🩸 BLOOD TRAIL SPOTTED! Evidence of a recent kill was found near Electrical!", "effect": "blood_trail"},
    {"type": "witness", "message": "👤 WITNESS COMES FORWARD! Someone claims to have seen suspicious activity near Reactor!", "effect": "witness"},
    {"type": "glitch", "message": "💻 SYSTEM GLITCH! Task data for 2 players has been temporarily corrupted. Reverify!", "effect": "glitch"},
    {"type": "forensics", "message": "🔬 FORENSICS UPDATE! Time of death analysis reveals kill happened during lights out!", "effect": "forensics"},
    {"type": "body_found", "message": "💀 BODY DISCOVERED! Emergency meeting auto-called in 2 minutes if no one reports!", "effect": "body_found"},
    {"type": "scan_reveal", "message": "🔍 THERMAL SCAN COMPLETE! Detected unusual heat signature near vent system!", "effect": "scan_reveal"},
    {"type": "access_log", "message": "🔐 ACCESS LOG LEAKED! Admin area was accessed by someone without clearance!", "effect": "access_log"},
    {"type": "pattern_detected", "message": "📊 PATTERN ANALYSIS: The impostor tends to act after emergency meetings!", "effect": "pattern"},
    {"type": "hallway_cam", "message": "📷 HALLWAY CAM ACTIVATED! Movement detected in Electrical 5 minutes ago!", "effect": "hallway_cam"},
    {"type": "voice_recording", "message": "🎙️ VOICE RECORDING FOUND! Someone made a suspicious call from comms room!", "effect": "voice_rec"},
    {"type": "location_ping", "message": "📍 EMERGENCY PING! One player's location is being broadcast publicly for 3 minutes!", "effect": "location_ping"},
    {"type": "document_leak", "message": "📄 DOCUMENT LEAK! Task completion records show a discrepancy in the logs!", "effect": "doc_leak"},
    {"type": "database_hack", "message": "💾 DATABASE COMPROMISED! Player identities scrambled for next 5 minutes!", "effect": "db_hack"},

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # ATMOSPHERE EVENTS
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    {"type": "meteor_shower", "message": "☄️ METEOR SHOWER! The ship is shaking! All players lose 1 point but gain excitement!", "effect": "meteor"},
    {"type": "warp_speed", "message": "🚀 WARP SPEED ENGAGED! Travel time between rooms halved for 10 minutes!", "effect": "warp"},
    {"type": "solar_flare", "message": "🌟 SOLAR FLARE! Communications disrupted for 5 minutes. No anonymous messages!", "effect": "flare"},
    {"type": "asteroid_field", "message": "🪨 ASTEROID FIELD! Extra caution required. No movement abilities for 5 minutes!", "effect": "asteroid"},
    {"type": "nebula", "message": "🌌 NEBULA DETECTED! Vision reduced — scans are 50% less accurate for 10 minutes!", "effect": "nebula"},
    {"type": "cosmic_ray", "message": "☢️ COSMIC RAY HIT! Random player loses their active shield right now!", "effect": "cosmic_ray"},
    {"type": "space_storm", "message": "⛈️ SPACE STORM! All sabotage cooldowns reset — impostors can sabotage again!", "effect": "storm"},
    {"type": "gravity_anomaly", "message": "🌀 GRAVITY ANOMALY! All vent travel disabled for 10 minutes!", "effect": "gravity"},
    {"type": "oxygen_low", "message": "😮‍💨 OXYGEN DROPPING! Complete 3 tasks in 5 minutes or the ship loses oxygen!", "effect": "oxygen_low"},
    {"type": "power_fluctuation", "message": "⚡ POWER FLUCTUATION! Abilities use twice the energy for 5 minutes!", "effect": "power_flux"},
    {"type": "signal_boost", "message": "📡 SIGNAL BOOSTED! All anonymous messages will reveal sender for 5 minutes!", "effect": "signal_boost"},
    {"type": "time_warp", "message": "⏰ TIME WARP! All cooldowns jump ahead by 1 hour instantly!", "effect": "time_warp"},
    {"type": "quantum_tunnel", "message": "🔮 QUANTUM TUNNEL! Vents teleport to random locations for 10 minutes!", "effect": "quantum"},
    {"type": "dark_energy", "message": "🌑 DARK ENERGY SURGE! Impostor vision enhanced for 5 minutes!", "effect": "dark_energy"},
    {"type": "light_burst", "message": "💡 LIGHT BURST! All rooms fully lit — lights sabotage blocked for 15 minutes!", "effect": "light_burst"},
    {"type": "ion_storm", "message": "🌩️ ION STORM! Electronic abilities malfunction for 5 minutes!", "effect": "ion_storm"},
    {"type": "wormhole", "message": "🕳️ WORMHOLE DETECTED! One random player teleports to a different location!", "effect": "wormhole"},
    {"type": "star_alignment", "message": "⭐ STAR ALIGNMENT! Every task completed in next 30 min gets +3 bonus points!", "effect": "star_align"},
    {"type": "solar_wind", "message": "💨 SOLAR WIND! Shield effectiveness doubled for next 10 minutes!", "effect": "solar_wind"},
    {"type": "black_hole", "message": "🕳️ BLACK HOLE NEARBY! All ability ranges are reduced to half for 10 minutes!", "effect": "black_hole"},

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # SOCIAL & DRAMA EVENTS
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    {"type": "trust_fall", "message": "🤝 TRUST FALL! Players must publicly declare one person they trust. Most trusted gets +10 pts!", "effect": "trust_fall"},
    {"type": "confession", "message": "🙏 CONFESSION HOUR! Anyone who confesses to a wrong action gets partial immunity!", "effect": "confession"},
    {"type": "alliance", "message": "🤜 ALLIANCE FORMED! Two random players are temporarily protected by each other's shields!", "effect": "alliance"},
    {"type": "betrayal", "message": "🗡️ BETRAYAL EVENT! A random crewmate and impostor swap awareness for 5 minutes!", "effect": "betrayal"},
    {"type": "therapy_session", "message": "🧠 THERAPY SESSION! All negative point penalties are halved for next 30 minutes!", "effect": "therapy"},
    {"type": "town_hall", "message": "🏛️ TOWN HALL! All players must vote on one thing in next 5 minutes!", "effect": "town_hall"},
    {"type": "rumor_mill", "message": "👂 RUMOR MILL! A false clue is added to the evidence pool. Beware red herrings!", "effect": "rumor"},
    {"type": "group_hug", "message": "🤗 GROUP HUG! All alive players get +3 points for morale!", "effect": "group_hug"},
    {"type": "double_agent", "message": "🕵️ DOUBLE AGENT! One crewmate secretly gets impostor-level info for 10 minutes!", "effect": "double_agent"},
    {"type": "ultimatum", "message": "⚠️ ULTIMATUM! One player must be voted out in next meeting or crewmates lose 10 pts each!", "effect": "ultimatum"},
    {"type": "celebrity", "message": "🌟 CELEBRITY MOMENT! Random player gets their last 3 actions broadcasted to everyone!", "effect": "celebrity"},
    {"type": "witch_hunt", "message": "🔥 WITCH HUNT! Next 5 votes require justification or they don't count!", "effect": "witch_hunt"},
    {"type": "mercy_rule", "message": "💝 MERCY RULE! Last-place player gets +20 free points to stay competitive!", "effect": "mercy"},
    {"type": "paranoia", "message": "😱 PARANOIA EVENT! Everyone's roles are secretly hinted to their most trusted contact!", "effect": "paranoia"},
    {"type": "information_war", "message": "📰 INFO WAR! Next 10 minutes — sharing any evidence is worth +5 points!", "effect": "info_war"},
    {"type": "gossip", "message": "💬 GOSSIP ROUND! Every message shared publicly for 5 minutes earns +2 points!", "effect": "gossip"},
    {"type": "immunity_idol", "message": "🏆 IMMUNITY IDOL! Random player is immune from next vote. Who will it be?", "effect": "immunity"},
    {"type": "trial", "message": "⚖️ PUBLIC TRIAL! Most suspicious player has 60 seconds to defend themselves!", "effect": "trial"},
    {"type": "spy_network", "message": "🕸️ SPY NETWORK ACTIVATED! Players can now see where others have been in last hour!", "effect": "spy_net"},
    {"type": "defection", "message": "🚪 DEFECTION ALERT! One random player may choose to switch sides... watch carefully!", "effect": "defection"},
]

IMPOSTER_SLIP_HINTS = [
    "📡 Security cameras caught someone in Electrical who had no task assigned there.",
    "🔍 A crew log shows someone completed a task in 0.3 seconds — physically impossible!",
    "💬 An anonymous message was traced back to a device signature... interesting.",
    "🌀 Vent system detected unauthorized usage near the Reactor area.",
    "📊 Task anomaly: someone marked a task complete before it was even assigned.",
    "🎭 Body language analysis: someone has been avoiding cameras strategically.",
    "🔧 Maintenance log shows someone 'fixed' a system that wasn't broken.",
    "📍 Location ping shows a player teleported across the ship in under a second.",
    "🚨 Alert: Two players were in the same room but one didn't report seeing the other.",
    "💡 Power usage spiked in a room where no task should be active.",
    "🔬 Biometric scan shows elevated stress in someone during the last meeting.",
    "📷 Camera footage: someone walked into MedBay but the scan animation never played.",
    "⏱️ Activity log: player was in Lower Engine for 0.1 seconds — not enough to complete any task.",
    "🎵 Audio analysis: ventilation system made unusual sounds near Cafeteria.",
    "🔐 Access log: someone tried to open a secured door without credentials.",
    "📱 Digital trace: a device pinged from two different rooms in less than 10 seconds.",
    "🌡️ Thermal scan: someone generated heat in a room — but not from completing a task.",
    "👥 Witness report: a player was seen 'waiting' near an inactive task panel.",
    "🔭 Navigation log: ship briefly veered off course — someone touched the controls.",
    "💻 System log: admin panel was accessed by someone who claimed to be elsewhere.",
    "🎥 CCTV playback: a shadow was seen entering a vent 3 minutes ago.",
    "📉 Task completion graph shows a suspicious spike from one player.",
    "🛸 Emergency log: life support was nearly disabled without anyone reporting it.",
    "🧪 Chemical residue found near the oxygen tanks — someone tampered with them.",
    "📣 Voice pattern analysis: someone's speech pattern was inconsistent in last meeting.",
    "🗂️ File corruption detected in the task database — someone modified records.",
    "⚡ Power grid shows unauthorized energy draw in the vent network.",
    "🌊 Oxygen level dropped briefly in Electrical — someone triggered and aborted a sabotage.",
    "🔑 Keycard access denied twice — someone tried to enter a restricted zone.",
    "📡 Signal interference from Reactor area at the exact time of the last kill.",
    "🕶️ Thermal overlay shows two heat signatures in a room where only one player was reported.",
    "🧲 Magnetic anomaly near weapons bay — someone activated a system without authorization.",
    "⏰ Time-motion analysis: a player's route between tasks is geometrically impossible without vents.",
    "💾 Memory log: one player's task log has been partially deleted.",
    "🔊 Sound analysis: footsteps tracked moving faster than human pace near reactor.",
    "🌐 Network traffic: unusual data burst from admin console 20 minutes ago.",
    "🪟 Window sensor: someone exited and re-entered the cafeteria in under 2 seconds.",
    "🔩 Screws on vent panel near MedBay appear freshly disturbed.",
    "🎭 Stress analysis: one player showed elevated cortisol during every emergency meeting.",
    "📋 Task board discrepancy: a task was marked done but the completion token wasn't generated.",
    "🕳️ Vacuum pressure anomaly detected in vent between Security and Admin rooms.",
    "💼 Briefcase scan: one player's locker contains items inconsistent with their assigned tasks.",
    "🖥️ Screen grab: admin terminal shows dual login — someone was remote controlling tasks.",
    "🔭 Satellite imagery: heat bloom detected at exact vent locations during lights out.",
    "📌 GPS data shows a player was in two places simultaneously — impossible... unless they used vents.",
    "🧬 DNA trace found near emergency button — doesn't match anyone who was in that area.",
    "🎯 Trajectory analysis of last kill suggests attacker came from vent, not door.",
    "📻 Comms log: encrypted message sent at 03:00 from admin room. No one was scheduled there.",
    "🌡️ Body temperature scan: one player's heat signature disappeared briefly — vent transit?",
    "🔦 UV light reveals handprints on the vent cover near Navigation.",
]

AMBIENT_MESSAGES = [
    "🌌 The ship is quiet... too quiet.",
    "💨 You hear footsteps behind you...",
    "👁️ Someone is watching from the shadows.",
    "🔧 A distant clang echoes through the vents.",
    "⚡ The lights flicker for a moment.",
    "🚨 An alarm briefly sounds then cuts off.",
    "📡 Communications feel... monitored.",
    "🌡️ The temperature in the reactor dropped suddenly.",
    "🔴 Emergency lights flashed in the lower deck.",
    "💀 You found a suspicious stain near the cafeteria...",
    "👤 A shadow moves quickly past the window.",
    "🛸 The ship drifts slightly off course.",
    "🔒 Someone tried to access a locked room.",
    "📹 Security footage from 2 minutes ago is missing.",
    "🧪 Lab samples have been tampered with.",
    "🌑 For a split second, everything went dark.",
    "🔊 Was that... laughter? From the vents?",
    "🕶️ Two players were seen whispering privately.",
    "⏰ Time feels slower today. Something is off.",
    "🗺️ The admin map glitched for 3 seconds.",
    "💼 Someone left their task kit unattended.",
    "🔑 A keycard was found on the floor of Storage.",
    "👟 Fresh footprints lead toward the Reactor area.",
    "🌬️ The vents are unusually active today.",
    "📝 Someone wrote 'trust no one' in the cafeteria.",
    "🎭 A crewmate is acting... differently today.",
    "🔬 The MedBay scanner returned unusual readings.",
    "💻 The admin console flickered when no one was near it.",
    "🐾 Something moved in the darkness near Electrical.",
    "🌊 The oxygen gauge dipped briefly without explanation.",
    "📺 The security feed cut out for exactly 4 seconds.",
    "🧲 Metal objects near Weapons keep moving on their own.",
    "🎵 The ship's ambient music stopped. Why?",
    "🛠️ Maintenance reported a vent cover was loose this morning.",
    "🔭 Something is tracking the ship from outside.",
    "📦 Boxes in Storage have been moved during the night.",
    "🌠 A shooting star crossed the viewport... or was it a ship?",
    "💡 The lights in Navigation are slightly dimmer than usual.",
    "🧊 The temperature in the freezer room is 3 degrees off.",
    "🎯 Three tasks were marked 'attempted' but not completed.",
    "🔔 An alert sound played from an empty room.",
    "📻 Static on comms channel 7. No one was transmitting.",
    "👻 The motion sensor in Security detected movement. No one was there.",
    "🌀 The gravity plating in Lower Engine fluctuated for a second.",
    "🎪 Someone rearranged chairs in the cafeteria. Why?",
    "🔦 The emergency flashlights were all switched to 'on' position.",
    "💬 A message was left in the comms log: just three dots...",
    "🔮 The ship's AI said something unprompted: 'ANOMALY DETECTED.'",
    "🌪️ Air pressure in Reactor is slightly elevated.",
    "⛵ The ship changed course by 0.2 degrees. Someone touched navigation.",
]

SABOTAGE_CHALLENGES = {
    "power": {"question": "⚡ Type 'RESTORE POWER' to fix the electrical system!", "answer": "RESTORE POWER", "time": 60},
    "oxygen": {"question": "😮‍💨 What percentage of Earth's atmosphere is oxygen? Type the number!", "answer": "21", "time": 45},
    "reactor": {"question": "☢️ Type 'CORE STABLE' to prevent meltdown!", "answer": "CORE STABLE", "time": 30},
    "comms": {"question": "📡 Type 'SIGNAL FIXED' to restore communications!", "answer": "SIGNAL FIXED", "time": 90},
    "lights": {"question": "🌑 Type 'LIGHTS ON' to restore power to lighting grid!", "answer": "LIGHTS ON", "time": 30},
}

SABOTAGE_EVENTS = [
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # SYSTEM SABOTAGES (Engineering/Technical)
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    {"type": "power", "emoji": "⚡", "name": "POWER OUTAGE", "message": "Type 'RESTORE POWER' in {time} seconds!", "answer": "RESTORE POWER", "time": 60},
    {"type": "oxygen", "emoji": "😮‍💨", "name": "OXYGEN DEPLETED", "message": "What % of air is oxygen? Answer in {time} seconds!", "answer": "21", "time": 45},
    {"type": "reactor", "emoji": "☢️", "name": "REACTOR MELTDOWN", "message": "Type 'CORE STABLE' to prevent meltdown in {time} seconds!", "answer": "CORE STABLE", "time": 30},
    {"type": "comms", "emoji": "📡", "name": "COMMS DOWN", "message": "Type 'SIGNAL FIXED' to restore communications in {time} seconds!", "answer": "SIGNAL FIXED", "time": 90},
    {"type": "lights", "emoji": "🌑", "name": "LIGHTS OUT", "message": "Type 'LIGHTS ON' to restore power in {time} seconds!", "answer": "LIGHTS ON", "time": 30},
    {"type": "engines", "emoji": "🔧", "name": "ENGINE FAILURE", "message": "What fuels most rockets? Answer in {time} seconds!", "answer": "Liquid hydrogen", "time": 60},
    {"type": "navigation", "emoji": "🧭", "name": "NAV MALFUNCTION", "message": "What is the North Pole's latitude? Answer in {time} seconds!", "answer": "90", "time": 45},
    {"type": "cooling", "emoji": "🌡️", "name": "COOLING SYSTEM FAIL", "message": "Water boils at how many Celsius? Answer in {time} seconds!", "answer": "100", "time": 30},
    {"type": "shields", "emoji": "🛡️", "name": "SHIELDS OFFLINE", "message": "Type 'SHIELDS UP' to reactivate defense grid in {time} seconds!", "answer": "SHIELDS UP", "time": 45},
    {"type": "life_support", "emoji": "🫁", "name": "LIFE SUPPORT CRITICAL", "message": "How many liters of oxygen does a human need per hour? Answer in {time} seconds!", "answer": "300", "time": 60},
    {"type": "fuel", "emoji": "⛽", "name": "FUEL LEAK", "message": "Type 'SEAL LEAK' to stop the fuel from escaping in {time} seconds!", "answer": "SEAL LEAK", "time": 45},
    {"type": "hull", "emoji": "🚀", "name": "HULL BREACH", "message": "Type 'HULL SEALED' to close the breach in {time} seconds!", "answer": "HULL SEALED", "time": 30},
    {"type": "gravity", "emoji": "🌀", "name": "GRAVITY PLATING OFFLINE", "message": "Type 'GRAVITY ON' to restore normal gravity in {time} seconds!", "answer": "GRAVITY ON", "time": 45},
    {"type": "thermal", "emoji": "🔥", "name": "THERMAL OVERLOAD", "message": "What absorbs heat? Type the answer in {time} seconds!", "answer": "Water", "time": 60},
    {"type": "pressure", "emoji": "💨", "name": "PRESSURE DROP", "message": "Normal air pressure in atm? Answer in {time} seconds!", "answer": "1", "time": 45},

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # KNOWLEDGE SABOTAGES (Quiz-based)
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    {"type": "quiz_math", "emoji": "🔢", "name": "MATH CRISIS", "message": "SOLVE: What is 25 × 25? Answer in {time} seconds!", "answer": "625", "time": 30},
    {"type": "quiz_science", "emoji": "🔬", "name": "SCIENCE EMERGENCY", "message": "What is the chemical symbol for gold? Answer in {time} seconds!", "answer": "Au", "time": 30},
    {"type": "quiz_geo", "emoji": "🌍", "name": "NAVIGATION SYSTEM NEEDS GEO DATA", "message": "What is the capital of France? Answer in {time} seconds!", "answer": "Paris", "time": 20},
    {"type": "quiz_history", "emoji": "📜", "name": "HISTORICAL DATABASE CORRUPTED", "message": "What year did India get independence? Answer in {time} seconds!", "answer": "1947", "time": 25},
    {"type": "quiz_space", "emoji": "🌌", "name": "SPACE KNOWLEDGE REQUIRED", "message": "Which planet is largest? Answer in {time} seconds!", "answer": "Jupiter", "time": 25},
    {"text": "BIOLOGY CRISIS", "type": "quiz_bio", "emoji": "🧬", "name": "BIOLOGY DATABASE NEEDED", "message": "How many chromosomes do humans have? Answer in {time} seconds!", "answer": "46", "time": 30},
    {"type": "quiz_speed", "emoji": "⚡", "name": "SPEED CALCULATION NEEDED", "message": "What is the speed of light in km/s? Answer in {time} seconds!", "answer": "300000", "time": 20},
    {"type": "quiz_elements", "emoji": "⚗️", "name": "ELEMENT IDENTIFICATION REQUIRED", "message": "What is the atomic number of Carbon? Answer in {time} seconds!", "answer": "6", "time": 25},
    {"type": "quiz_pi", "emoji": "🥧", "name": "MATHEMATICAL CONSTANT NEEDED", "message": "What is the value of pi to 2 decimal places? Answer in {time} seconds!", "answer": "3.14", "time": 20},
    {"type": "quiz_water", "emoji": "💧", "name": "COMPOUND IDENTIFICATION", "message": "What is the chemical formula for water? Answer in {time} seconds!", "answer": "H2O", "time": 15},

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # ACTION SABOTAGES (Type specific phrases)
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    {"type": "action_all", "emoji": "📢", "name": "CREW ROLL CALL", "message": "ALL CREW type 'PRESENT' in {time} seconds or lose 5 points each!", "answer": "PRESENT", "time": 30},
    {"type": "action_sos", "emoji": "🆘", "name": "DISTRESS SIGNAL", "message": "Send 'SOS' to acknowledge emergency in {time} seconds!", "answer": "SOS", "time": 20},
    {"type": "action_code", "emoji": "🔐", "name": "SECURITY CODE NEEDED", "message": "The security override code is 'ALPHA ZETA'. Type it in {time} seconds!", "answer": "ALPHA ZETA", "time": 45},
    {"type": "action_manual", "emoji": "📖", "name": "MANUAL OVERRIDE", "message": "Type 'MANUAL OVERRIDE ENGAGED' to bypass automatic shutdown in {time} seconds!", "answer": "MANUAL OVERRIDE ENGAGED", "time": 60},
    {"type": "action_confirm", "emoji": "✅", "name": "CREW CONFIRMATION NEEDED", "message": "Type 'CREW CONFIRMED' to verify headcount in {time} seconds!", "answer": "CREW CONFIRMED", "time": 30},
    {"type": "action_launch", "emoji": "🚀", "name": "EMERGENCY LAUNCH PROTOCOL", "message": "Type 'ABORT LAUNCH' to stop the unauthorized launch in {time} seconds!", "answer": "ABORT LAUNCH", "time": 30},
    {"type": "action_lock", "emoji": "🔒", "name": "LOCKDOWN PROTOCOL", "message": "Type 'LOCKDOWN LIFTED' to restore normal operations in {time} seconds!", "answer": "LOCKDOWN LIFTED", "time": 45},
    {"type": "action_emergency", "emoji": "🚨", "name": "EMERGENCY PROTOCOL", "message": "Type 'ALL CLEAR' to signal the all-clear in {time} seconds!", "answer": "ALL CLEAR", "time": 25},
    {"type": "action_restart", "emoji": "🔄", "name": "SYSTEM RESTART", "message": "Type 'SYSTEM RESTART AUTHORIZED' to reboot core in {time} seconds!", "answer": "SYSTEM RESTART AUTHORIZED", "time": 60},
    {"type": "action_beacon", "emoji": "📡", "name": "BEACON ACTIVATION", "message": "Type 'BEACON ACTIVE' to signal rescue in {time} seconds!", "answer": "BEACON ACTIVE", "time": 30},

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # ROLEPLAY SABOTAGES (Fun scenarios)
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    {"type": "roleplay_cook", "emoji": "🍳", "name": "CAFETERIA FIRE", "message": "The cafeteria is on fire! What do you do? First to say 'EXTINGUISHER' wins +15 pts!", "answer": "EXTINGUISHER", "time": 30},
    {"type": "roleplay_med", "emoji": "🏥", "name": "MEDICAL EMERGENCY", "message": "A crewmate is hurt! What's the emergency number? Type 'MEDIC CALLED' in {time} seconds!", "answer": "MEDIC CALLED", "time": 30},
    {"type": "roleplay_ghost", "emoji": "👻", "name": "GHOST SIGNAL DETECTED", "message": "A ghost is trying to communicate! Type 'HELLO GHOST' to acknowledge in {time} seconds!", "answer": "HELLO GHOST", "time": 25},
    {"type": "roleplay_alien", "emoji": "👽", "name": "UNKNOWN SIGNAL", "message": "Alien signal received! Respond with 'WE COME IN PEACE' in {time} seconds!", "answer": "WE COME IN PEACE", "time": 40},
    {"type": "roleplay_captain", "emoji": "⚓", "name": "CAPTAIN IS DOWN", "message": "The captain is unconscious! Who takes over? First to say 'I TAKE COMMAND' gets +20 pts!", "answer": "I TAKE COMMAND", "time": 20},
    {"type": "roleplay_vote", "emoji": "🗳️", "name": "EMERGENCY REFERENDUM", "message": "Emergency crew vote! Type 'AYE' to support crisis protocols in {time} seconds!", "answer": "AYE", "time": 30},
    {"type": "roleplay_escape", "emoji": "🏃", "name": "ESCAPE POD NEEDED", "message": "Ship is going down! Only those who type 'ESCAPE POD' in {time} seconds survive!", "answer": "ESCAPE POD", "time": 20},
    {"type": "roleplay_supply", "emoji": "📦", "name": "SUPPLY SHORTAGE", "message": "Critical supplies needed! Type 'REQUESTING SUPPLIES' in {time} seconds!", "answer": "REQUESTING SUPPLIES", "time": 35},
    {"type": "roleplay_drill", "emoji": "🔔", "name": "EMERGENCY DRILL", "message": "EMERGENCY DRILL! All crew type 'DRILL ACKNOWLEDGED' in {time} seconds!", "answer": "DRILL ACKNOWLEDGED", "time": 30},
    {"type": "roleplay_search", "emoji": "🔍", "name": "SEARCH PROTOCOL", "message": "Initiate search for intruder! Type 'SEARCHING' in {time} seconds!", "answer": "SEARCHING", "time": 25},

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # PUZZLE SABOTAGES
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    {"type": "puzzle_sequence", "emoji": "🔢", "name": "SEQUENCE ERROR", "message": "Fix the sequence! What comes next: 2, 4, 8, 16, ___? Answer in {time} seconds!", "answer": "32", "time": 30},
    {"type": "puzzle_word", "emoji": "📝", "name": "WORD DECRYPTION", "message": "Decrypt: OITSMPRO (hint: Among Us role). Answer in {time} seconds!", "answer": "IMPOSTOR", "time": 45},
    {"type": "puzzle_color", "emoji": "🎨", "name": "COLOR CODE", "message": "Red + Blue = ? Type the color in {time} seconds!", "answer": "Purple", "time": 20},
    {"type": "puzzle_riddle", "emoji": "🧩", "name": "SECURITY RIDDLE", "message": "What has keys but no locks? (Security answer) Answer in {time} seconds!", "answer": "keyboard", "time": 30},
    {"type": "puzzle_number", "emoji": "🔢", "name": "NUMBER PUZZLE", "message": "EMERGENCY CODE: What is 12 × 12? Type in {time} seconds!", "answer": "144", "time": 20},
    {"type": "puzzle_password", "emoji": "🔐", "name": "PASSWORD SYSTEM", "message": "Password hint: Opposite of 'closed'. Type in {time} seconds!", "answer": "open", "time": 25},
    {"type": "puzzle_direction", "emoji": "🧭", "name": "NAVIGATION PUZZLE", "message": "Opposite of North? Answer in {time} seconds!", "answer": "South", "time": 15},
    {"type": "puzzle_element", "emoji": "⚗️", "name": "CHEMICAL PUZZLE", "message": "H2O is? Answer in {time} seconds!", "answer": "water", "time": 15},
    {"type": "puzzle_pattern", "emoji": "🔮", "name": "PATTERN RECOGNITION", "message": "Complete the pattern: 1, 1, 2, 3, 5, 8, ___? Answer in {time} seconds!", "answer": "13", "time": 25},
    {"type": "puzzle_logic", "emoji": "🧠", "name": "LOGIC GATE ERROR", "message": "If all A are B, and all B are C, are all A C? Type YES or NO in {time} seconds!", "answer": "YES", "time": 20},

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # WILDCARD SABOTAGES
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    {"type": "wild_emoji", "emoji": "🎭", "name": "EMOJI SYSTEM CRASH", "message": "Send this exact emoji sequence in {time} seconds: 🚀🔴🟢⭐", "answer": "🚀🔴🟢⭐", "time": 30},
    {"type": "wild_backwards", "emoji": "🔄", "name": "MIRROR PROTOCOL", "message": "Type 'SPACE SHIP' BACKWARDS in {time} seconds!", "answer": "PIHS ECAPS", "time": 45},
    {"type": "wild_caps", "emoji": "🔊", "name": "BROADCAST EMERGENCY", "message": "SHOUT THE EMERGENCY! Type 'HELP US ALL' in all caps in {time} seconds!", "answer": "HELP US ALL", "time": 20},
    {"type": "wild_song", "emoji": "🎵", "name": "MORALE EMERGENCY", "message": "Send 5 music emojis in {time} seconds to boost crew morale!", "answer": "🎵🎵🎵🎵🎵", "time": 20},
    {"type": "wild_spell", "emoji": "✍️", "name": "SPELLING TEST EMERGENCY", "message": "Spell 'CREWMATE' correctly in {time} seconds!", "answer": "CREWMATE", "time": 20},
    {"type": "wild_count", "emoji": "🔢", "name": "COUNT PROTOCOL", "message": "Count from 1 to 5 in {time} seconds (type: 1 2 3 4 5)!", "answer": "1 2 3 4 5", "time": 25},
    {"type": "wild_rhyme", "emoji": "🎤", "name": "RHYME EMERGENCY", "message": "Rhyme with 'SPACE': What rhymes? First correct answer wins +20 pts! (in {time}s)", "answer": None, "time": 30},
    {"type": "wild_flag", "emoji": "🏳️", "name": "FLAG SIGNAL", "message": "Wave the flag! Type 'I SURRENDER' for mercy from sabotage penalty!", "answer": "I SURRENDER", "time": 30},
    {"type": "wild_chant", "emoji": "📣", "name": "WAR CRY NEEDED", "message": "Battle cry! Type 'FOR THE CREW' to rally the team in {time} seconds!", "answer": "FOR THE CREW", "time": 20},
    {"type": "wild_vote_now", "emoji": "🗳️", "name": "INSTANT VOTE PROTOCOL", "message": "RAPID VOTE: Most suspicious player right now? First 5 responses get +5 pts each!", "answer": None, "time": 60},
]


def get_random_event() -> dict:
    return random.choice(RANDOM_EVENTS)


def get_impostor_hint() -> str:
    return random.choice(IMPOSTER_SLIP_HINTS)


def get_ambient_message() -> str:
    return random.choice(AMBIENT_MESSAGES)


def get_random_sabotage() -> dict:
    return random.choice(SABOTAGE_EVENTS)


def get_sabotage_by_type(sabotage_type: str) -> dict:
    for s in SABOTAGE_EVENTS:
        if s["type"] == sabotage_type:
            return s
    return SABOTAGE_EVENTS[0]


def get_sabotage_challenge(sabotage_type: str) -> dict:
    basic = SABOTAGE_CHALLENGES.get(sabotage_type)
    if basic:
        return basic
    full = get_sabotage_by_type(sabotage_type)
    return {
        "question": full["message"].format(time=full["time"]),
        "answer": full.get("answer", None),
        "time": full["time"]
    }


def get_event_count() -> int:
    return len(RANDOM_EVENTS)


def get_sabotage_count() -> int:
    return len(SABOTAGE_EVENTS)
