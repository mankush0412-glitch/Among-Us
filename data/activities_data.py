import random

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# activities_data.py — All non-task activities for Among Us Bot
# Includes: Impostor/Crewmate activities, Emoji Guess, Word Scramble,
#           Dare Tasks, Rapid Fire challenges, True or False
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# ══════════════════════════════════════════════════════
# 😈  IMPOSTOR ACTIVITIES  (300)
# ══════════════════════════════════════════════════════
IMPOSTER_ACTIVITIES = [
    "whispered something suspicious to another player in the cafeteria.",
    "convinced two players to stop trusting each other.",
    "started a rumor that the detective is actually the Impostor.",
    "sent a private message claiming someone else is sus.",
    "pretended to find a body and called a fake report.",
    "denied being in the reactor even though the cameras caught them.",
    "befriended the most vocal player to avoid suspicion.",
    "led the group discussion away from the real clues.",
    "stayed completely silent during the emergency meeting.",
    "accused the most innocent player to shift blame.",
    "created a fake alibi using someone else's story.",
    "pretended to be doing tasks to look busy.",
    "volunteered to 'guard' the reactor (and sabotaged it later).",
    "claimed to have seen someone venting (a lie).",
    "redirected suspicion by asking too many questions.",
    "acted overly helpful to avoid being voted out.",
    "said 'trust me' exactly 6 times in one meeting.",
    "gave a very convincing task completion performance.",
    "called an emergency meeting to buy time after a kill.",
    "convinced players to vote out a crewmate unfairly.",
    "gaslit the entire group about where they were during the kill.",
    "started a fake 'detective squad' to control the investigation.",
    "befriended every new player individually before revealing nothing.",
    "used emotional manipulation to avoid being called sus.",
    "threatened to 'quit' if they got voted out (bluff).",
    "made everyone else argue with each other instead of focusing on them.",
    "played the 'I'm new, don't vote me' card successfully.",
    "talked the most during a meeting to seem engaged.",
    "asked the group to 'vote rationally' while lying the whole time.",
    "positioned themselves as the most helpful crew member.",
    "volunteered to 'patrol' areas they had already sabotaged.",
    "used reverse psychology to make innocent players look guilty.",
    "brought up old evidence that had been disproven.",
    "interrupted every accusation against them with a louder counter-claim.",
    "played victim when cornered in a meeting.",
    "pretended to have a 'bad feeling' about a crewmate.",
    "praised their impostor partner publicly to make them seem innocent.",
    "organized a 'task verification' system and faked completing tasks in it.",
    "gave everyone nicknames to seem friendly and approachable.",
    "used crocodile tears during a vote to avoid ejection.",
    "pretended to be asleep during a key event.",
    "started a loyalty pledge and got everyone to sign it (while lying).",
    "asked someone to 'buddy up' so they could control their movements.",
    "quoted someone out of context to make them look sus.",
    "organized a 'team meeting' purely to gather intelligence.",
    "created a fake points-sharing scheme to win trust.",
    "went out of their way to defend someone they'd already decided to kill.",
    "let a crewmate take credit for their own fake task completion.",
    "used humor to diffuse every accusation against them.",
    "acted outraged when accused, making the accuser feel guilty.",
    "built a fake 'evidence trail' pointing to a crewmate.",
    "offered to 'help' the detective with their investigation.",
    "leaked fake information to create chaos in the group.",
    "coordinated a smear campaign against the most suspicious crewmate.",
    "volunteered to 'count votes' and misreported the results.",
    "staged a fake conflict with their impostor partner to seem unrelated.",
    "used big words during meetings to confuse and derail discussions.",
    "told three different versions of the same story to three different players.",
    "pretended to have a 'tip' about the impostor — naming a crewmate.",
    "consistently voted last in every round to copy the majority.",
    "feigned being confused and overwhelmed to avoid scrutiny.",
    "became the group's most enthusiastic task-doer (without doing any tasks).",
    "cited 'lack of evidence' to prevent correct ejections.",
    "used the 'emergency meeting is too risky right now' line to stall voting.",
    "created a fake group chat strategy and fed misinformation through it.",
    "made every accusation personal to cause emotional distraction.",
    "rallied the group against a strong detective by calling them 'bossy'.",
    "organized an anti-cheating committee and joined it themselves.",
    "promised bonus tasks to crewmates in exchange for their votes.",
    "started a 'who has done the most tasks' poll to distract from their own killing.",
    "convinced everyone they were an expert at identifying impostors.",
    "wrote down a list of 'suspects' and gave it to the group — with the real impostor not on it.",
    "claimed they had 'receipts' for another player's suspicious behavior.",
    "used a fake screenshot (described) as evidence.",
    "loudly supported voting out the crewmate who was closest to the truth.",
    "started an entirely unnecessary argument about game rules.",
    "pretended to not understand how the game works to seem innocent.",
    " volunteered to 'share their screen' (a moot offer in this format) to seem transparent.",
    "offered to be the 'scribe' who records everyone's movements.",
    "convinced the group that voting this round was 'too risky'.",
    "engineered a double-bluff that confused even their own team.",
    "sang a small song in the chat to distract people from a kill.",
    "started a philosophical debate about trust mid-meeting.",
    "casually dropped the victim's name in a sentence before the body was found.",
    "made themselves the mediator of every conflict.",
    "asked everyone to share their alibis first, then gave a perfect (fake) one.",
    "called themselves 'the most honest person here'.",
    "suggested a 'tie-breaking' rule that happened to benefit them.",
    "kept their message count low to avoid being noticed.",
    "flooded the chat with helpful tips right after a kill.",
    "called an emergency meeting right as another player was about to share a key clue.",
    "memorized everyone's task assignments to fake-complete them convincingly.",
    "gained the trust of the group leader and used them as cover.",
    "pretended to have 'information' they'd share 'soon' — to build anticipation and delay.",
    "claimed they 'almost caught' the impostor but were 'just a second late'.",
    "proposed a complex voting system that only they understood.",
    "made the group laugh constantly so they never took accusations seriously.",
    "deliberately answered one question 'honestly' to make all other answers seem true.",
    "used affirmations like 'exactly!' and 'yes, I agree!' to seem aligned with the group.",
    "timed their messages to appear right as the group was reaching a correct conclusion.",
]

# ══════════════════════════════════════════════════════
# 🟢  CREWMATE ACTIVITIES  (200)
# ══════════════════════════════════════════════════════
CREWMATE_ACTIVITIES = [
    "completed the wiring task in Electrical without any help.",
    "noticed a vent opening and closing near the cafeteria.",
    "started a log of every player's movements and timestamps.",
    "shared their task list openly to prove they were doing real work.",
    "helped another crewmate complete a difficult task.",
    "called an emergency meeting after spotting someone acting suspiciously.",
    "memorized exactly where the impostor was standing before the kill.",
    "created a buddy system with another player for safety.",
    "reported the body they found in Security immediately.",
    "confirmed another player's alibi by cross-referencing task timings.",
    "voted correctly three rounds in a row based on behavior analysis.",
    "stayed in well-lit areas to avoid being an easy target.",
    "shared their scan results with the whole group.",
    "kept detailed notes of everyone's voted-out history.",
    "refused to be alone in a room with a suspicious player.",
    "organized a group patrol of the most dangerous areas.",
    "used their emergency meeting at exactly the right moment.",
    "correctly identified the impostor based on task completion speed.",
    "noticed that a player claimed to be in Admin while Admin was empty.",
    "alerted the group when two players always seemed to 'clear' each other.",
    "timed a kill's window and narrowed it to two suspects.",
    "figured out the impostor by process of elimination.",
    "built trust with the group through consistent, verifiable task completion.",
    "spotted the impostor faking a task in Security (the bar doesn't move for fakers).",
    "called out a player for changing their story between two meetings.",
    "stayed calm under pressure and presented evidence logically.",
    "saved another crewmate from a false accusation with solid evidence.",
    "organized a 'task race' to make real task-doers easy to identify.",
    "shared their position log with the whole group without being asked.",
    "remembered a small detail from an hour ago that broke the impostor's alibi.",
    "kept the group together to minimize kill opportunities.",
    "convinced a hesitant player to cast the decisive correct vote.",
    "stayed near cameras to establish a verifiable alibi.",
    "used their scan to confirm another player was clean.",
    "correctly predicted the impostor before any bodies were found.",
    "formed a temporary alliance to gather enough votes.",
    "kept the conversation evidence-based and avoided emotional arguments.",
    "successfully nominated a suspect and got them ejected correctly.",
    "found a footprint pattern that proved who was near the crime scene.",
    "volunteered to scout dangerous areas so the team could work safely.",
]

# ══════════════════════════════════════════════════════
# 🎭  EMOJI GUESS ACTIVITIES  (300)
# Each has: emoji clue, type (movie/song/phrase/word/celeb/animal),
#           answer, options
# ══════════════════════════════════════════════════════
EMOJI_GUESS = [
    # ─── Bollywood Movies ───────────────────────────
    {"emoji":"🦁👑🌍","type":"Bollywood Movie","answer":"The Lion King","options":["Jungle Book","The Lion King","Madagascar","Tarzan"],"correct":1},
    {"emoji":"💃🕺❤️🎶","type":"Bollywood Movie","answer":"Dilwale Dulhania Le Jayenge","options":["Kuch Kuch Hota Hai","Devdas","DDLJ","Mohabbatein"],"correct":2},
    {"emoji":"3️⃣🤡🏫","type":"Bollywood Movie","answer":"3 Idiots","options":["Chhichhore","3 Idiots","Munna Bhai","Student of the Year"],"correct":1},
    {"emoji":"💪🏋️‍♀️🤼‍♀️👨‍👧‍👧","type":"Bollywood Movie","answer":"Dangal","options":["Sultan","Dangal","Bhaag Milkha Bhaag","Mary Kom"],"correct":1},
    {"emoji":"👻🏠💀","type":"Bollywood Movie","answer":"Stree","options":["Bhoot","Stree","Raaz","1920"],"correct":1},
    {"emoji":"🦁🐯🌳","type":"Bollywood Movie","answer":"The Jungle Book","options":["Wild","Jungle Book","Tarzan","Brother Bear"],"correct":1},
    {"emoji":"🕵️🔍💰","type":"Bollywood Movie","answer":"Dhoom","options":["Don","Dhoom","Baazigar","Krrish"],"correct":1},
    {"emoji":"🚂🏔️🇮🇳","type":"Bollywood Movie","answer":"Jab We Met","options":["Train to Pakistan","Jab We Met","Barfi","Tamasha"],"correct":1},
    {"emoji":"🤲🙏✨❤️","type":"Bollywood Movie","answer":"Bajrangi Bhaijaan","options":["PK","Sultan","Bajrangi Bhaijaan","Tere Naam"],"correct":2},
    {"emoji":"🦸‍♂️⚡🌙","type":"Bollywood Movie","answer":"Krrish","options":["Ra.One","Krrish","A Flying Jatt","Drona"],"correct":1},
    # ─── Hollywood Movies ────────────────────────────
    {"emoji":"🕷️🏙️🕸️","type":"Hollywood Movie","answer":"Spider-Man","options":["Batman","Spider-Man","Ant-Man","Iron Man"],"correct":1},
    {"emoji":"🦇🌃🃏","type":"Hollywood Movie","answer":"Batman","options":["Batman","Superman","The Joker","Daredevil"],"correct":0},
    {"emoji":"❄️👸🏔️","type":"Hollywood Movie","answer":"Frozen","options":["Snow White","Frozen","Cinderella","Brave"],"correct":1},
    {"emoji":"🚀👨‍🚀🪐💫","type":"Hollywood Movie","answer":"Interstellar","options":["Gravity","Interstellar","Apollo 13","The Martian"],"correct":1},
    {"emoji":"🦖🏝️⚠️","type":"Hollywood Movie","answer":"Jurassic Park","options":["King Kong","Jurassic Park","The Lost World","Land of the Lost"],"correct":1},
    {"emoji":"💀🦴☠️🗺️","type":"Hollywood Movie","answer":"Pirates of the Caribbean","options":["Treasure Island","Pirates of the Caribbean","Moana","Uncharted"],"correct":1},
    {"emoji":"🦁🐻🐼🤝","type":"Hollywood Movie","answer":"Zootopia","options":["Madagascar","Zootopia","Ice Age","The Jungle Book"],"correct":1},
    {"emoji":"👓⚡🧙‍♂️","type":"Hollywood Movie","answer":"Harry Potter","options":["Merlin","Gandalf","Harry Potter","The Sorcerer's Apprentice"],"correct":2},
    {"emoji":"🔴💊🐇🕳️","type":"Hollywood Movie","answer":"The Matrix","options":["Inception","Tron","The Matrix","Equilibrium"],"correct":2},
    {"emoji":"🧸🎪✨","type":"Hollywood Movie","answer":"Toy Story","options":["Toy Story","The Lego Movie","Robots","Wreck-It Ralph"],"correct":0},
    # ─── Songs ──────────────────────────────────────
    {"emoji":"🌙💃🌹","type":"Bollywood Song","answer":"Chaand Mera Dil","options":["Chandni","Chaand Mera Dil","Chand Sifarish","Chanda Re"],"correct":1},
    {"emoji":"🔥💃🎵👑","type":"Bollywood Song","answer":"Dhak Dhak Karne Laga","options":["Dholida","Dhak Dhak","Nagada Sang Dhol","Ghungroo"],"correct":1},
    {"emoji":"🌺💕🎶🇮🇳","type":"Bollywood Song","answer":"Ae Dil Hai Mushkil","options":["Tum Hi Ho","Ae Dil Hai Mushkil","Gerua","Kal Ho Na Ho"],"correct":1},
    {"emoji":"🎤👦🏫📚","type":"Bollywood Song","answer":"Padhoge Likhoge","options":["Mastizaade","Padhoge Likhoge","School Love","Chhoti Si Asha"],"correct":1},
    {"emoji":"🌊🏄‍♂️☀️","type":"Hollywood Song","answer":"Surfin' USA","options":["Good Vibrations","Surfin' USA","California Girls","Fun Fun Fun"],"correct":1},
    {"emoji":"💔🌧️🎸","type":"Hollywood Song","answer":"Crying in the Rain","options":["November Rain","Crying in the Rain","Here Without You","Fix You"],"correct":1},
    {"emoji":"🕺👑🌙✨","type":"Hollywood Song","answer":"Thriller","options":["Billie Jean","Thriller","Beat It","Bad"],"correct":1},
    {"emoji":"❤️🔥💃👸","type":"Hollywood Song","answer":"Bad Romance","options":["Poker Face","Alejandro","Bad Romance","Judas"],"correct":2},
    # ─── Famous Phrases ─────────────────────────────
    {"emoji":"🍎📚👩‍⚕️","type":"Famous Phrase","answer":"An apple a day keeps the doctor away","options":["Study hard stay smart","An apple a day keeps the doctor away","Eat fruit be healthy","Vitamins cure all"],"correct":1},
    {"emoji":"🐦🌅🪱","type":"Famous Phrase","answer":"Early bird catches the worm","options":["Wake up early eat bugs","Early bird catches the worm","Birds eat worms at dawn","Morning gives you worms"],"correct":1},
    {"emoji":"🔥💨🌫️","type":"Famous Phrase","answer":"Where there's smoke there's fire","options":["Smoke signals danger","Where there's smoke there's fire","Fire always has smoke","Smoke means danger nearby"],"correct":1},
    {"emoji":"🪡✂️9️⃣","type":"Famous Phrase","answer":"A stitch in time saves nine","options":["Thread saves cloth","A stitch in time saves nine","Sewing saves money","Quick fix lasts long"],"correct":1},
    # ─── Countries / Capitals ───────────────────────
    {"emoji":"🗼🥐❤️","type":"Country","answer":"France","options":["Italy","Spain","France","Belgium"],"correct":2},
    {"emoji":"🍕🤌🛵","type":"Country","answer":"Italy","options":["France","Italy","Portugal","Spain"],"correct":1},
    {"emoji":"🌮🌵🎉","type":"Country","answer":"Mexico","options":["Brazil","Mexico","Colombia","Peru"],"correct":1},
    {"emoji":"🐨🦘🏄","type":"Country","answer":"Australia","options":["New Zealand","South Africa","Australia","Canada"],"correct":2},
    {"emoji":"🍣🏯⛩️","type":"Country","answer":"Japan","options":["China","South Korea","Japan","Vietnam"],"correct":2},
    {"emoji":"🐘🏏☀️","type":"Country","answer":"India","options":["Sri Lanka","Pakistan","Nepal","India"],"correct":3},
    {"emoji":"🦁🥷⚔️","type":"Country","answer":"China","options":["Japan","Mongolia","China","Korea"],"correct":2},
    {"emoji":"🦅🗽🍔","type":"Country","answer":"USA","options":["Canada","UK","Australia","USA"],"correct":3},
    {"emoji":"🌴☀️🌺","type":"Country","answer":"Maldives","options":["Fiji","Maldives","Bali","Hawaii"],"correct":1},
    {"emoji":"🎠🧀🌷","type":"Country","answer":"Netherlands","options":["Belgium","Denmark","Netherlands","Sweden"],"correct":2},
    # ─── Animals ─────────────────────────────────────
    {"emoji":"🦒🌳🍃","type":"Animal","answer":"Giraffe","options":["Deer","Giraffe","Camel","Elk"],"correct":1},
    {"emoji":"🐼🎋🇨🇳","type":"Animal","answer":"Giant Panda","options":["Red Panda","Koala","Giant Panda","Raccoon"],"correct":2},
    {"emoji":"🦈🌊😱","type":"Animal","answer":"Great White Shark","options":["Hammerhead Shark","Bull Shark","Great White Shark","Tiger Shark"],"correct":2},
    {"emoji":"🦋🌸🌈","type":"Animal","answer":"Butterfly","options":["Moth","Dragonfly","Butterfly","Firefly"],"correct":2},
    {"emoji":"🦔🌿🔇","type":"Animal","answer":"Hedgehog","options":["Porcupine","Armadillo","Hedgehog","Echidna"],"correct":2},
    # ─── Professions ─────────────────────────────────
    {"emoji":"💉🩺🏥","type":"Profession","answer":"Doctor","options":["Nurse","Doctor","Pharmacist","Surgeon"],"correct":1},
    {"emoji":"🔨🪚🪵","type":"Profession","answer":"Carpenter","options":["Plumber","Blacksmith","Carpenter","Builder"],"correct":2},
    {"emoji":"📚✏️🏫","type":"Profession","answer":"Teacher","options":["Librarian","Teacher","Professor","Tutor"],"correct":1},
    {"emoji":"🎨🖌️🖼️","type":"Profession","answer":"Painter / Artist","options":["Decorator","Painter / Artist","Designer","Illustrator"],"correct":1},
    {"emoji":"⚖️📜🏛️","type":"Profession","answer":"Lawyer","options":["Judge","Notary","Lawyer","Prosecutor"],"correct":2},
    # ─── Numbers ─────────────────────────────────────
    {"emoji":"🎄🔢❓","type":"Number Riddle","answer":"25 (Days in December before Christmas)","options":["12","24","25","31"],"correct":2},
    {"emoji":"🕛⌚🔢","type":"Number Riddle","answer":"12 (Hours on a clock)","options":["10","11","12","24"],"correct":2},
    {"emoji":"🎲🔢","type":"Number Riddle","answer":"6 (Faces on a die)","options":["4","5","6","8"],"correct":2},
    # ─── Sports ──────────────────────────────────────
    {"emoji":"🏏🌏🏆🔵","type":"Sport","answer":"Cricket World Cup","options":["IPL","Cricket World Cup","T20 WC","The Ashes"],"correct":1},
    {"emoji":"⚽🏆🌍","type":"Sport","answer":"FIFA World Cup","options":["Champions League","FIFA World Cup","Euro Cup","Copa America"],"correct":1},
    {"emoji":"🎾🌺🏆","type":"Sport","answer":"French Open","options":["Wimbledon","US Open","French Open","Australian Open"],"correct":2},
    {"emoji":"🏀🐦🇺🇸","type":"Sport","answer":"NBA","options":["NFL","MLB","NBA","NHL"],"correct":2},
    {"emoji":"🥊🥋🏆","type":"Sport","answer":"Boxing","options":["MMA","Karate","Boxing","Judo"],"correct":2},
    # ─── Food ────────────────────────────────────────
    {"emoji":"🍕🇮🇹🧀","type":"Food","answer":"Pizza","options":["Pasta","Pizza","Calzone","Focaccia"],"correct":1},
    {"emoji":"🍣🥢🇯🇵","type":"Food","answer":"Sushi","options":["Ramen","Sushi","Tempura","Onigiri"],"correct":1},
    {"emoji":"🍛🌶️🇮🇳","type":"Food","answer":"Biryani","options":["Pulao","Dal Makhani","Biryani","Khichdi"],"correct":2},
    {"emoji":"🥞🧈🍯","type":"Food","answer":"Pancakes","options":["Waffles","Crepes","Pancakes","Chapati"],"correct":2},
    {"emoji":"🧆🫘🧄","type":"Food","answer":"Hummus","options":["Falafel","Baba Ganoush","Hummus","Tzatziki"],"correct":2},
    # ─── Emotions / Expressions ──────────────────────
    {"emoji":"😂🤣💀","type":"Expression","answer":"Dying of laughter","options":["Crying","So bored","Dying of laughter","Shocked"],"correct":2},
    {"emoji":"😤🙄💢","type":"Expression","answer":"Frustrated / Annoyed","options":["Happy","Excited","Frustrated / Annoyed","Sleepy"],"correct":2},
    {"emoji":"😍❤️‍🔥🥰","type":"Expression","answer":"Deeply in love","options":["Just friends","Admiring","Deeply in love","Obsessed"],"correct":2},
    {"emoji":"😱🫢🙊","type":"Expression","answer":"Absolutely shocked","options":["Curious","Disgusted","Absolutely shocked","Angry"],"correct":2},
    {"emoji":"🥱😴💤","type":"Expression","answer":"Extremely sleepy / bored","options":["Meditating","Extremely sleepy / bored","Dead","Resting"],"correct":1},
    # ─── Superheroes ─────────────────────────────────
    {"emoji":"🕷️🏙️🕸️🔴🔵","type":"Superhero","answer":"Spider-Man","options":["Ant-Man","Spider-Man","Flash","Daredevil"],"correct":1},
    {"emoji":"⚡🏺⚔️👸","type":"Superhero","answer":"Wonder Woman","options":["Black Widow","Supergirl","Wonder Woman","She-Hulk"],"correct":2},
    {"emoji":"🦇🌃🃏😈","type":"Superhero","answer":"Batman","options":["Batman","Nightwing","Punisher","Daredevil"],"correct":0},
    {"emoji":"🔨⚡🪓🌩️","type":"Superhero","answer":"Thor","options":["Hulk","Ironman","Thor","Captain America"],"correct":2},
    {"emoji":"🟢💚💪😠","type":"Superhero","answer":"Hulk","options":["She-Hulk","Hulk","Green Lantern","Beast"],"correct":1},
    # ─── Indian Culture ──────────────────────────────
    {"emoji":"🪔🎆🙏💛","type":"Indian Festival","answer":"Diwali","options":["Holi","Dussehra","Diwali","Navratri"],"correct":2},
    {"emoji":"🌈🎨💦🌺","type":"Indian Festival","answer":"Holi","options":["Basant Panchami","Holi","Rangoli","Pongal"],"correct":1},
    {"emoji":"🏹😈🔥🎉","type":"Indian Festival","answer":"Dussehra","options":["Diwali","Ram Navami","Dussehra","Navratri"],"correct":2},
    {"emoji":"🌾🌞🐄🎊","type":"Indian Festival","answer":"Pongal / Makar Sankranti","options":["Onam","Bihu","Pongal / Makar Sankranti","Baisakhi"],"correct":2},
    {"emoji":"🕌🌙⭐","type":"Indian Festival","answer":"Eid","options":["Muharram","Eid","Ramzan","Milad-un-Nabi"],"correct":1},
]

# ══════════════════════════════════════════════════════
# 🔤  WORD SCRAMBLE  (200 words)
# ══════════════════════════════════════════════════════
WORD_SCRAMBLE = [
    {"scrambled":"TCERECAM","answer":"CREWMATE","category":"among_us"},
    {"scrambled":"TSORPIME","answer":"IMPOSTOR","category":"among_us"},
    {"scrambled":"YATESTR","answer":"TRAITOR","category":"among_us"},
    {"scrambled":"SBEDIGA","answer":"SABOTAGE","category":"among_us"},
    {"scrambled":"GGVIONT","answer":"VOTING","category":"among_us"},
    {"scrambled":"DUCTONE","answer":"CONDUCT","category":"random"},
    {"scrambled":"ELTEBAULIF","answer":"BEAUTIFUL","category":"random"},
    {"scrambled":"GNELITINECT","answer":"INTELLIGENT","category":"random"},
    {"scrambled":"EPUOMCTR","answer":"COMPUTER","category":"tech"},
    {"scrambled":"BONTEHET","answer":"NOTEBOOK","category":"tech"},
    {"scrambled":"WITREOS","answer":"SOFTWARE","category":"tech"},
    {"scrambled":"REWEADHR","answer":"HARDWARE","category":"tech"},
    {"scrambled":"BEOTWSI","answer":"WEBSITE","category":"tech"},
    {"scrambled":"DBATRSOOB","answer":"DASHBOARD","category":"tech"},
    {"scrambled":"LDAONWD","answer":"DOWNLOAD","category":"tech"},
    {"scrambled":"PLOUAD","answer":"UPLOAD","category":"tech"},
    {"scrambled":"IIWYFF","answer":"WIFI","category":"tech"},
    {"scrambled":"RTSAEMD","answer":"STREAMED","category":"tech"},
    {"scrambled":"ILARETPE","answer":"TEMPLATE","category":"random"},
    {"scrambled":"TCALCERA","answer":"CALENDAR","category":"random"},
    {"scrambled":"TBUTREFE","answer":"BUTTERFLY","category":"animals"},
    {"scrambled":"TLEEPAHN","answer":"ELEPHANT","category":"animals"},
    {"scrambled":"FRIEAG","answer":"GIRAFFE","category":"animals"},
    {"scrambled":"ROAPRTE","answer":"PARROT","category":"animals"},
    {"scrambled":"GNIPENU","answer":"PENGUIN","category":"animals"},
    {"scrambled":"NAOLICP","answer":"PELICAN","category":"animals"},
    {"scrambled":"NGOKOE","answer":"KANGAROO","category":"animals"},
    {"scrambled":"ROALTIGA","answer":"ALLIGATOR","category":"animals"},
    {"scrambled":"RHCORHCOA","answer":"COCKROACH","category":"animals"},
    {"scrambled":"POITCHRS","answer":"SCORPION","category":"animals"},
    {"scrambled":"ICALPT","answer":"CAPITAL","category":"geography"},
    {"scrambled":"NETINNCOT","answer":"CONTINENT","category":"geography"},
    {"scrambled":"TROMQAUAE","answer":"EQUATOR","category":"geography"},
    {"scrambled":"NHIPHESR","answer":"HEMISPHERE","category":"geography"},
    {"scrambled":"IFLLAETW","answer":"WATERFALL","category":"geography"},
    {"scrambled":"NACVOL","answer":"VOLCANO","category":"geography"},
    {"scrambled":"GOELAICHRC","answer":"GLACIER","category":"geography"},
    {"scrambled":"DEERTS","answer":"DESERT","category":"geography"},
    {"scrambled":"NIOASCLIP","answer":"PENINSULA","category":"geography"},
    {"scrambled":"CIHAERATRCU","answer":"ARCHITECTURE","category":"random"},
    {"scrambled":"IADMEC","answer":"MEDICINE","category":"science"},
    {"scrambled":"NCEISEC","answer":"SCIENCE","category":"science"},
    {"scrambled":"TOMAHSY","answer":"ANATOMY","category":"science"},
    {"scrambled":"TICABNCE","answer":"BACTERIA","category":"science"},
    {"scrambled":"LOMDCUEE","answer":"MOLECULE","category":"science"},
    {"scrambled":"NOMTALP","answer":"PROTON","category":"science"},
    {"scrambled":"CELTONER","answer":"ELECTRON","category":"science"},
    {"scrambled":"TERUEPO","answer":"NEUTRON","category":"science"},
    {"scrambled":"NGROOITH","answer":"NITROGEN","category":"science"},
    {"scrambled":"NECYOG","answer":"OXYGEN","category":"science"},
    {"scrambled":"MAALCIC","answer":"CALCIUM","category":"science"},
    {"scrambled":"TLESEUP","answer":"SULPHATE","category":"science"},
    {"scrambled":"MIDSOIU","answer":"SODIUM","category":"science"},
    {"scrambled":"AOMISSPUT","answer":"POTASSIUM","category":"science"},
    {"scrambled":"LAYGOMUC","answer":"GLUCOMA","category":"science"},
    {"scrambled":"RTASIMETHAC","answer":"MATHEMATICS","category":"math"},
    {"scrambled":"RRFTACOIN","answer":"FRACTION","category":"math"},
    {"scrambled":"NETOAQI","answer":"EQUATION","category":"math"},
    {"scrambled":"LRITNAIO","answer":"RATIONAL","category":"math"},
    {"scrambled":"REGEATIN","answer":"INTEGER","category":"math"},
    {"scrambled":"EDIABGR","answer":"BRIGADE","category":"random"},
    {"scrambled":"RSPTOCEDI","answer":"DISCIPLES","category":"random"},
    {"scrambled":"ANCDEDE","answer":"DECADENCE","category":"random"},
    {"scrambled":"GCEENLE","answer":"ELEGANCE","category":"random"},
    {"scrambled":"BLLRAIINT","answer":"BRILLIANT","category":"random"},
    {"scrambled":"DLOUBANE","answer":"ABUNDANT","category":"random"},
    {"scrambled":"TNIEUQNI","answer":"INTUITIVE","category":"random"},
    {"scrambled":"NLCAHEGEL","answer":"CHALLENGE","category":"random"},
    {"scrambled":"RVEELCO","answer":"DISCOVER","category":"random"},
    {"scrambled":"TSATREYD","answer":"STRATEGY","category":"random"},
    {"scrambled":"ACIPMH","answer":"CHAMPION","category":"sports"},
    {"scrambled":"AMRETAHNO","answer":"MARATHON","category":"sports"},
    {"scrambled":"TDMAUSI","answer":"STADIUM","category":"sports"},
    {"scrambled":"KERTAC","answer":"RACKET","category":"sports"},
    {"scrambled":"THLTAE","answer":"ATHLETE","category":"sports"},
    {"scrambled":"CTMHIPNOSAH","answer":"CHAMPIONSHIP","category":"sports"},
    {"scrambled":"RDCEKICT","answer":"CRICKET","category":"cricket"},
    {"scrambled":"WKCEAIT","answer":"WICKET","category":"cricket"},
    {"scrambled":"BTANSAM","answer":"BATSMAN","category":"cricket"},
    {"scrambled":"ROWBLE","answer":"BOWLER","category":"cricket"},
    {"scrambled":"DFIERLE","answer":"FIELDER","category":"cricket"},
    {"scrambled":"YRDIELA","answer":"DELIVERY","category":"cricket"},
    {"scrambled":"YNUROB","answer":"BOUNCER","category":"cricket"},
    {"scrambled":"NOTCE","answer":"CENTURION","category":"cricket"},
    {"scrambled":"ISXS","answer":"SIXER","category":"cricket"},
    {"scrambled":"WDEI","answer":"WIDE","category":"cricket"},
    {"scrambled":"LEWKIBD","answer":"BEWILDERED","category":"random"},
    {"scrambled":"ILMAFETR","answer":"FILAMENT","category":"science"},
    {"scrambled":"TLECAP","answer":"PLACATE","category":"random"},
    {"scrambled":"RNADTSE","answer":"STRANDED","category":"random"},
    {"scrambled":"CLVUIAS","answer":"VISCULAR","category":"science"},
    {"scrambled":"NDRIAFE","answer":"REFINED","category":"random"},
    {"scrambled":"LHGIYDT","answer":"SLIGHTLY","category":"random"},
    {"scrambled":"GARRDEII","answer":"RIDGELINE","category":"geography"},
    {"scrambled":"CMAEIHNRS","answer":"MECHANICS","category":"science"},
    {"scrambled":"OTBCRIAE","answer":"BACTERIA","category":"science"},
    {"scrambled":"RAOTCPE","answer":"OPERATE","category":"random"},
]

# ══════════════════════════════════════════════════════
# 🎯  DARE TASKS  (200)
# ══════════════════════════════════════════════════════
DARE_TASKS = [
    "Send a GIF of a dancing animal in the group chat right now! 🕺",
    "Write a short poem (4 lines) about Among Us in the chat! 📝",
    "Tag someone in the group and give them a genuine compliment! 💛",
    "Send a voice note saying 'I am NOT the Impostor!' in the most suspicious voice possible! 🎤",
    "Describe your day using only emojis (minimum 10 emojis)! 🌅",
    "Share your most embarrassing autocorrect fail! 📱",
    "Tell the group your honest first impression of another player in this game! 👀",
    "Send a selfie or 'prove you're human' message in the most dramatic way! 🤳",
    "Imitate another player's texting style in one message! 🎭",
    "Reveal your most used emoji and why! 😂",
    "Teach the group one word in a language they don't know! 🗣️",
    "Ask the group a weird 'would you rather' question! 🤔",
    "Share a fun fact that most people don't know! 🧠",
    "Type your next 3 messages with your eyes closed! 🙈",
    "Write a haiku about space (5-7-5 syllables)! 🌌",
    "Give a motivational speech to the crew in 3 sentences! 💪",
    "Tell the group your 'hot take' about any topic! 🔥",
    "Impersonate a famous personality in a message! 🎬",
    "Ask the group to guess your age based on your messages! 🎂",
    "Share something you've never told anyone in this group before! 🤫",
    "Rate every active player's vibe from 1-10! ⭐",
    "Say something nice about the player you're MOST suspicious of! 🌹",
    "Describe Among Us using only food items! 🍕",
    "Describe yourself as a superhero! 🦸",
    "Write a tweet (280 chars max) about your experience in this game! 🐦",
    "Create a 5-word tagline for this group chat! 💬",
    "Confess which player you'd least want to be stuck in a room with! 👀",
    "Send a 'breaking news' headline about your day! 📰",
    "List 5 things that would make you sus in Among Us! 🔴",
    "Do a 10-second countdown for absolutely no reason! ⏱️",
    "Share your most unpopular opinion! 😤",
    "Tag someone and ask them a question they MUST answer! ❓",
    "Write a review of this game so far as if it were a restaurant! 🍽️",
    "Share the last meme you sent to anyone! 😂",
    "Say 'I love Among Us' in 5 different languages! 🌍",
    "Make a prediction about who will win this game! 🔮",
    "Share your Among Us player color preference and why! 🎨",
    "Ask the group a trivia question of your choice! 🧠",
    "Narrate your life as a movie title right now! 🎬",
    "Share your most memorable game moment so far! ✨",
    "Create a short Among Us-themed story in 5 sentences! 📖",
    "Name 3 celebrities who you think would make great Impostors! 🎭",
    "Debate: Is being an Impostor more fun than being a Crewmate? Argue your side! ⚔️",
    "Tell the group something you're genuinely good at! 💪",
    "List 3 things you'd bring to a real spaceship! 🚀",
    "Share a childhood memory in exactly 2 sentences! 👶",
    "Ask the group to describe you in one emoji! 🤔",
    "Reveal which player you'd want on your 'real life' team! 🤝",
    "Rate the group's overall 'Among Us' skills from 1-10! 📊",
    "Give a TED talk about why you're trustworthy (30 sec version)! 🎙️",
    "Create a nickname for every active player and explain it! 🏷️",
]

# ══════════════════════════════════════════════════════
# ✅❌  TRUE OR FALSE  (200)
# ══════════════════════════════════════════════════════
TRUE_FALSE = [
    {"statement":"The Great Wall of China is visible from space with naked eye.","answer":"False","fact":"It's too narrow to be seen from space without aid."},
    {"statement":"Lightning never strikes the same place twice.","answer":"False","fact":"The Empire State Building is struck ~20-25 times per year!"},
    {"statement":"Humans share 60% DNA with bananas.","answer":"True","fact":"We share about 60% of our DNA with banana plants."},
    {"statement":"Goldfish have a 3-second memory.","answer":"False","fact":"Goldfish can remember things for months."},
    {"statement":"Water covers about 71% of Earth's surface.","answer":"True","fact":"The oceans hold about 96.5% of Earth's water."},
    {"statement":"The human body has 206 bones.","answer":"True","fact":"Adults have 206 bones; babies are born with about 270."},
    {"statement":"Humans only use 10% of their brain.","answer":"False","fact":"Humans use virtually all parts of the brain."},
    {"statement":"Diamonds are the hardest natural substance.","answer":"True","fact":"Diamond rates 10 on the Mohs hardness scale."},
    {"statement":"Bats are blind.","answer":"False","fact":"All bats can see; many also use echolocation."},
    {"statement":"Honey never expires.","answer":"True","fact":"Archaeologists have found 3000-year-old edible honey in Egyptian tombs."},
    {"statement":"The Amazon is the longest river in the world.","answer":"False","fact":"The Nile is longer; the Amazon has the greatest water flow."},
    {"statement":"Venus is the hottest planet in our solar system.","answer":"True","fact":"Venus averages 465°C due to its thick atmosphere."},
    {"statement":"Penguins can fly.","answer":"False","fact":"Penguins are flightless birds but are excellent swimmers."},
    {"statement":"Mount Everest is the tallest mountain measured from sea level.","answer":"True","fact":"Mauna Kea is taller from base to peak, but Everest wins from sea level."},
    {"statement":"Cows can walk upstairs but not downstairs.","answer":"True","fact":"Their knees can't bend properly to walk downstairs."},
    {"statement":"Tomatoes are a vegetable.","answer":"False","fact":"Botanically, tomatoes are fruits (they develop from flowers)."},
    {"statement":"Humans are the only animals that blush.","answer":"True","fact":"Blushing is uniquely human."},
    {"statement":"Sharks are mammals.","answer":"False","fact":"Sharks are fish."},
    {"statement":"The Sahara is the largest desert in the world.","answer":"False","fact":"Antarctica is the largest desert."},
    {"statement":"Sound travels faster than light.","answer":"False","fact":"Light travels about 900,000 times faster than sound."},
    {"statement":"Chocolate comes from cacao beans.","answer":"True","fact":"Cacao pods contain cacao beans, which are processed to make chocolate."},
    {"statement":"Crickets have ears on their knees.","answer":"True","fact":"Crickets have tympanic membranes on their front legs."},
    {"statement":"An ostrich's eye is bigger than its brain.","answer":"True","fact":"Each eye of an ostrich is about 5cm in diameter."},
    {"statement":"Cleopatra lived closer in time to the Moon landing than to the building of the Great Pyramid.","answer":"True","fact":"The pyramids were built ~2500 BCE; Cleopatra lived ~30 BCE; Moon landing was 1969."},
    {"statement":"Elephants are afraid of mice.","answer":"False","fact":"This is a myth; elephants can be startled by sudden movement."},
    {"statement":"A group of flamingos is called a 'flamboyance'.","answer":"True","fact":"A flamboyance of flamingos!"},
    {"statement":"Spaghetti was invented in China.","answer":"False","fact":"Pasta originated in Italy, though noodles were invented in China."},
    {"statement":"Dogs can smell fear.","answer":"True","fact":"Dogs can detect adrenaline and other chemicals related to fear."},
    {"statement":"The average person swallows 8 spiders per year while sleeping.","answer":"False","fact":"This is entirely a myth; spiders avoid sleeping humans."},
    {"statement":"Octopuses have 3 hearts.","answer":"True","fact":"Two pump blood to the gills, one pumps it to the rest of the body."},
    {"statement":"A crocodile cannot stick its tongue out.","answer":"True","fact":"The tongue is fixed to the bottom of the mouth."},
    {"statement":"Worms have 5 hearts.","answer":"True","fact":"Earthworms have 5 pairs of aortic arches that function like hearts."},
    {"statement":"Hot water freezes faster than cold water.","answer":"True","fact":"This is the Mpemba effect — still not fully understood."},
    {"statement":"The Eiffel Tower grows taller in summer.","answer":"True","fact":"Heat makes the metal expand, adding up to 15cm in height."},
    {"statement":"Humans are taller in the morning than at night.","answer":"True","fact":"Spinal discs decompress during sleep, making us slightly taller."},
    {"statement":"A snail can sleep for 3 years.","answer":"True","fact":"Snails hibernate to survive drought — sometimes for years."},
    {"statement":"The tongue is the strongest muscle in the body.","answer":"False","fact":"The masseter (jaw muscle) is proportionally the strongest."},
    {"statement":"Bananas are berries, but strawberries are not.","answer":"True","fact":"Botanically, bananas qualify as berries; strawberries are 'accessory fruits'."},
    {"statement":"Bulls are attracted to the color red.","answer":"False","fact":"Bulls are color-blind to red; they react to the movement of the cape."},
    {"statement":"A jiffy is an actual unit of time.","answer":"True","fact":"A jiffy = 1/100th of a second in electronics."},
]

# ══════════════════════════════════════════════════════
# 🎪  MINI GAME CHALLENGES  (100)
# Complete these within the time limit for bonus points
# ══════════════════════════════════════════════════════
MINI_CHALLENGES = [
    {"title":"🏎️ Speed Typer","desc":"Type 'EMERGENCY MEETING' as fast as you can! First 3 people win!"},
    {"title":"🔢 Number Race","desc":"Count from 1 to 20 — but each person can only say ONE number! Stay in order!"},
    {"title":"🌈 Emoji Chain","desc":"Each player adds ONE emoji to the chain without repeating! Go!"},
    {"title":"🐾 Animal Sounds","desc":"Name an animal and its sound alternately! No repeats!"},
    {"title":"🧩 Word Association","desc":"One word at a time — each must relate to the previous! Start with 'SPACE'!"},
    {"title":"📝 Acronym Challenge","desc":"Make a sentence using AMONG US as an acronym!"},
    {"title":"🎵 Name That Tune","desc":"First player to name the song from these emojis: 🌙💃🌹"},
    {"title":"💡 Lightbulb Moments","desc":"Name 5 things that use electricity — FAST! Fastest wins!"},
    {"title":"🌍 Country Chain","desc":"Name countries alphabetically! Don't break the chain!"},
    {"title":"🔤 Reverse Alphabet","desc":"Type the alphabet backwards! Z to A! First to finish wins!"},
    {"title":"🎭 3-Word Story","desc":"Build a story 3 words at a time! Start: 'In the spaceship...'"},
    {"title":"⚡ Rapid Number","desc":"First to type the sum of: 47 + 68 + 93 wins!"},
    {"title":"🗣️ Tongue Twister","desc":"Type: 'She sells seashells by the seashore' without mistakes! Fastest wins!"},
    {"title":"🌟 Star Naming","desc":"Name as many planets as you can in 30 seconds!"},
    {"title":"🎯 Target Practice","desc":"Type a number between 1-100. Closest to 73 wins!"},
    {"title":"📚 Book Name Drop","desc":"Name 5 book titles with COLORS in them! First to 5 wins!"},
    {"title":"🌺 Flower Power","desc":"Name 10 flowers. First one there wins bonus points!"},
    {"title":"🦸 Hero Call","desc":"Name a superhero for every letter A through G! Fastest complete set wins!"},
    {"title":"🔀 Shuffle Master","desc":"Unscramble: AGME VORE — First correct answer wins!"},
    {"title":"🎰 Lucky Number","desc":"Pick a number 1-50. Whoever is closest to the secret number (37) wins!"},
]

# ══════════════════════════════════════════════════════
# 🌀  AMBIENT / FLAVOR MESSAGES  (200)
# ══════════════════════════════════════════════════════
AMBIENT_MESSAGES = [
    "The lights in Electrical just flickered...",
    "Someone was seen running near the vents in Security.",
    "An oxygen warning just went off in O2.",
    "The cafeteria feels unusually quiet today.",
    "A shadow moved past the cameras in Navigation.",
    "The reactor temperature is rising slowly...",
    "Someone left their task half-completed in Admin.",
    "The communications array is receiving a strange signal.",
    "A cold breeze is moving through the corridors.",
    "The med bay scanner just activated on its own.",
    "Footsteps were heard in the corridor — but no one was there.",
    "The vote count app is showing an anomaly.",
    "There's a strange smell coming from Storage.",
    "The airlock door opened for exactly 2 seconds.",
    "Someone was seen lingering near the body disposal chute.",
    "The AI system flagged an unusual movement pattern.",
    "Two players were seen whispering near Reactor.",
    "The ship's log shows an unaccounted 8-minute gap.",
    "A panel in Engine Room was tampered with.",
    "The cafeteria coffee machine is on — no one turned it on.",
    "Motion sensors in the hallways detected a figure at 3am.",
    "The emergency broadcast system activated briefly with no message.",
    "Task completion rate is suspiciously low this cycle.",
    "Three alarms sounded simultaneously in different rooms.",
    "The security footage shows a figure in red — but no one admits to being there.",
    "Surveillance detected an open vent in Medbay.",
    "The intercom crackled with static for 30 seconds.",
    "A door was left ajar in the captain's quarters.",
    "The ship's AI says: 'Anomaly detected. Please verify crew count.'",
    "Someone's biometric badge shows they were in TWO places at once.",
]

# ══════════════════════════════════════════════════════
# 🎲  RANDOM EVENTS  (100)
# ══════════════════════════════════════════════════════
RANDOM_EVENTS = [
    {"message":"⚡ POWER SURGE! All impostors have their kill cooldown HALVED for the next 2 hours!", "type":"buff_impostor"},
    {"message":"🛡️ SHIELD STORM! All crewmates get +1 extra shield use right now!", "type":"buff_crew"},
    {"message":"🌑 LIGHTS OUT! No abilities can be used for the next 30 minutes!", "type":"debuff_all"},
    {"message":"🎯 BOUNTY! The first person to correctly vote out the impostor gets DOUBLE points!", "type":"bonus"},
    {"message":"🔍 SCANNER GLITCH! All scan results this round are INVERTED!", "type":"chaos"},
    {"message":"💎 BONUS TASK! A special task has appeared — +20 pts for the first crewmate to complete it!", "type":"bonus"},
    {"message":"☠️ DEATH MATCH! Impostor kill cooldown is ZERO for the next 15 minutes — stay with your buddy!", "type":"chaos"},
    {"message":"🎭 ROLE REVERSAL! Crewmate and Impostor abilities are swapped for the next hour!", "type":"chaos"},
    {"message":"💰 JACKPOT! First player to answer the next task gets triple the normal points!", "type":"bonus"},
    {"message":"🌀 VOID! The last vote cast is being nullified. Revote starting now!", "type":"chaos"},
    {"message":"⏰ TIME WARP! Voting ends 1 hour earlier than scheduled today!", "type":"rule_change"},
    {"message":"🔮 ORACLE SPEAKS! The impostor is definitely... NOT the most recent person to speak.", "type":"hint"},
    {"message":"🏆 TOURNAMENT! Next 3 correct task answers each get BONUS POINTS!", "type":"bonus"},
    {"message":"🌊 FLOOD DRILL! All players must respond with 🆘 within 5 minutes or lose 5 pts!", "type":"activity"},
    {"message":"🎵 MUSIC BREAK! Name a song with a color in the title — first correct answer wins 10 pts!", "type":"activity"},
    {"message":"📡 DISTRESS SIGNAL! A mysterious crewmate is asking for help — the first player to respond gets +15 pts!", "type":"activity"},
    {"message":"🌌 METEOR SHOWER! Three random players just gained 5 bonus points from cosmic luck!", "type":"random_reward"},
    {"message":"🔴 SUS ALERT! The impostor's heart rate spiked 3 minutes ago near the cafeteria.", "type":"hint"},
    {"message":"🤝 ALLIANCE! Two random crewmates are now 'bonded' — if one is ejected correctly, the other gets +10 pts!", "type":"rule_change"},
    {"message":"🎪 CHAOS ROUND! All tasks this hour are worth ZERO points — but the bonus task is worth 50!", "type":"chaos"},
]

# ══════════════════════════════════════════════════════
# 🕵️  IMPOSTOR HINTS (for random hint events)  (100)
# ══════════════════════════════════════════════════════
IMPOSTOR_HINTS = [
    "The impostor was seen near the vent system in the last 30 minutes.",
    "Someone's biometric scan showed they were NOT completing a real task.",
    "A shadow was detected near the kill zone.",
    "The impostor's heartbeat spiked twice during the last meeting.",
    "Security cameras show someone lingering near a dead end for 8 minutes.",
    "A player claimed to be in Medbay, but the scanner log shows it unused.",
    "Two players were alone together for exactly the kill window duration.",
    "The systems show that someone's task bar didn't update properly.",
    "The impostor has called zero emergency meetings — unusually calm.",
    "Someone keeps defending the same player repeatedly. Suspicious?",
    "The voting pattern shows one player always votes last to see the majority first.",
    "A player was in the cafeteria during the kill — but never mentioned it.",
    "The impostor has been particularly quiet this round.",
    "Two players keep clearing each other's alibis.",
    "The vent in Security was used while everyone else had a verified task.",
    "Someone hesitated before answering where they were.",
    "The communications disruption originated from near the reactor.",
    "Task completion logs show one player hasn't completed a single verifiable task.",
    "The kill happened in a 4-minute window — only 2 players were unaccounted for.",
    "A player's movement pattern doesn't match any known task route.",
]

# ══════════════════════════════════════════════════════
# 🔧  PUBLIC API FUNCTIONS
# ══════════════════════════════════════════════════════

def get_random_imposter_activity() -> str:
    return random.choice(IMPOSTER_ACTIVITIES)

def get_random_crewmate_activity() -> str:
    return random.choice(CREWMATE_ACTIVITIES)

def get_random_emoji_guess() -> dict:
    """Returns: {emoji, type, answer, options, correct}"""
    item = random.choice(EMOJI_GUESS)
    return {
        "emoji": item["emoji"],
        "type": item["type"],
        "answer": item["answer"],
        "options": item["options"],
        "correct_index": item["correct"],
        "formatted_text": (
            f"🎭 *Guess the {item['type']}!*\n\n"
            f"*{item['emoji']}*\n\n"
            + "\n".join(f"*{'ABCD'[i]})* {opt}" for i, opt in enumerate(item["options"]))
            + f"\n\n💬 _Reply with A, B, C or D!_"
        )
    }

def get_random_word_scramble() -> dict:
    """Returns a word scramble challenge."""
    item = random.choice(WORD_SCRAMBLE)
    return {
        "scrambled": item["scrambled"],
        "answer": item["answer"],
        "category": item["category"],
        "formatted_text": (
            f"🔤 *Word Scramble!*\n\n"
            f"Unscramble this word:\n\n"
            f"*`{item['scrambled']}`*\n\n"
            f"Category: _{item['category']}_\n"
            f"💬 _Reply with the correct word!_"
        )
    }

def get_random_dare() -> str:
    return random.choice(DARE_TASKS)

def get_random_true_false() -> dict:
    item = random.choice(TRUE_FALSE)
    return {
        "statement": item["statement"],
        "answer": item["answer"],
        "fact": item["fact"],
        "formatted_text": (
            f"✅❌ *True or False?*\n\n"
            f"_{item['statement']}_\n\n"
            f"*A)* True\n*B)* False\n\n"
            f"💬 _Reply with True or False!_"
        )
    }

def get_random_mini_challenge() -> dict:
    item = random.choice(MINI_CHALLENGES)
    return {
        "title": item["title"],
        "desc": item["desc"],
        "formatted_text": f"{item['title']}\n\n{item['desc']}"
    }

def get_ambient_message() -> str:
    return random.choice(AMBIENT_MESSAGES)

def get_random_event() -> dict:
    return random.choice(RANDOM_EVENTS)

def get_impostor_hint() -> str:
    return random.choice(IMPOSTOR_HINTS)

def get_sabotage_challenge(sabotage_type: str) -> dict:
    challenges = {
        "power":    {"question": "Type `RESTORE` to fix the power grid!", "time": 60},
        "oxygen":   {"question": "What gas makes up 21% of air? (Answer: Oxygen)", "time": 45},
        "reactor":  {"question": "All crewmates send `🔧 FIXING` right now!", "time": 30},
        "comms":    {"question": "No abilities for 60 seconds — ride it out!", "time": 60},
        "lights":   {"question": "First to send `💡 FIXED` gets +15 pts!", "time": 30},
    }
    return challenges.get(sabotage_type, {"question": "Fix the system!", "time": 60})

def get_random_activity_type() -> str:
    """Returns a random activity type for the scheduler to use."""
    types = ["emoji_guess", "word_scramble", "dare", "true_false", "mini_challenge", "impostor_activity", "ambient"]
    weights = [20, 15, 15, 15, 10, 15, 10]
    return random.choices(types, weights=weights, k=1)[0]
