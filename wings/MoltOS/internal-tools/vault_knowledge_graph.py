#!/usr/bin/env python3
"""
VaultKnowledgeGraph v2 — Production-grade knowledge graph for Nathan's vault

Improvements over v1:
- Known entity whitelist (Hatchly, StandoutLocal, etc.)
- Noise filtering (blocklist of common words)
- File-structure entity inference
- Co-occurrence relationship detection
- Better query ranking with semantic scoring
- YAML frontmatter parsing for structured metadata

Usage:
    python vault_knowledge_graph.py --build          # Rebuild graph
    python vault_knowledge_graph.py --query "abandoned projects"
    python vault_knowledge_graph.py --entity "Hatchly"
    python vault_knowledge_graph.py --stats
"""

import json
import re
import os
import sys
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict, Counter
from typing import Dict, List, Set, Tuple, Optional

# ── Configuration ───────────────────────────────────────────────────────────

VAULT_ROOT = Path("/root/.openclaw/workspace/shepherd-brain-vault")
GRAPH_FILE = VAULT_ROOT / "../.cache/vault_knowledge_graph_v2.json"
INDEX_FILE = VAULT_ROOT / "../.cache/vault_graph_index_v2.json"

# Known entities that should ALWAYS be extracted with proper types
KNOWN_ENTITIES = {
    # Projects
    "Hatchly": "project",
    "StandoutLocal": "project",
    "Standout Local": "project",
    "MoltOS": "project",
    "MoltBook": "project",
    "Promachos": "project",
    "9router": "project",
    "Auto-Trigger": "project",
    "Knowledge Graph": "project",
    "Vault Knowledge Graph": "project",
    "Picasso Steal": "project",
    "Shepherd Brain": "project",
    
    # Companies
    "Kimi": "company",
    "Moonshot AI": "company",
    "Anthropic": "company",
    "OpenAI": "company",
    "Meta": "company",
    "Google": "company",
    
    # People
    "Nathan": "person",
    "Nathan Shepherd": "person",
    "Shepherd": "person",
    "Midas": "person",
    "Graeme": "person",
    
    # Technologies
    "OpenClaw": "technology",
    "Claude": "technology",
    "GPT": "technology",
    "LangChain": "technology",
    "CrewAI": "technology",
    "AutoGen": "technology",
    "Dify": "technology",
    "Ollama": "technology",
    "Next.js": "technology",
    "React": "technology",
    "TypeScript": "technology",
    
    # Concepts
    "AaaS": "concept",
    "SaaS": "concept",
    "Agent": "concept",
    "Swarm": "concept",
    "RAG": "concept",
    "Knowledge Graph": "concept",
    "Heartbeat": "concept",
    "Self-Diagnostic": "concept",
    "Crater Landing": "concept",
    "Picasso Steal": "concept",
    "Auto-Trigger": "concept",
    "1% Rule": "concept",
    "Triple Memory": "concept",
    "ClawFS": "concept",
    "Marrow": "concept",
}

# Words that should NEVER be entities
BLOCKLIST = {
    # Common words
    "the", "and", "or", "but", "for", "with", "from", "into", "onto", "about",
    "this", "that", "these", "those", "such", "what", "when", "where", "why",
    "how", "all", "any", "both", "each", "few", "more", "most", "other", "some",
    "very", "can", "will", "just", "should", "now", "only", "also", "than",
    "then", "them", "they", "their", "there", "here", "where", "were", "was",
    "been", "have", "has", "had", "did", "does", "doing", "done", "being",
    "are", "is", "am", "be", "to", "of", "in", "on", "at", "by", "as", "it",
    "its", "it's", "not", "no", "up", "out", "if", "so", "do", "go", "get",
    "got", "gotten", "make", "made", "take", "took", "see", "seen", "come",
    "came", "know", "knew", "known", "think", "thought", "say", "said", "tell",
    "told", "ask", "asked", "give", "gave", "given", "find", "found", "use",
    "used", "work", "worked", "call", "called", "try", "tried", "need", "needed",
    "feel", "felt", "become", "became", "leave", "left", "put", "mean", "meant",
    "keep", "kept", "let", "begin", "began", "seem", "seemed", "help", "helped",
    "show", "showed", "shown", "hear", "heard", "play", "played", "run", "ran",
    "move", "moved", "live", "lived", "believe", "believed", "bring", "brought",
    "happen", "happened", "write", "wrote", "written", "provide", "provided",
    "sit", "sat", "stand", "stood", "lose", "lost", "add", "added", "spend",
    "spent", "grow", "grew", "grown", "open", "opened", "walk", "walked", "win",
    "won", "offer", "offered", "remember", "remembered", "love", "loved",
    "consider", "considered", "appear", "appeared", "buy", "bought", "wait",
    "waited", "serve", "served", "die", "died", "send", "sent", "expect",
    "expected", "build", "built", "stay", "stayed", "fall", "fell", "fallen",
    "cut", "reach", "reached", "kill", "killed", "remain", "remained",
    "suggest", "suggested", "raise", "raised", "pass", "passed", "sell", "sold",
    "require", "required", "report", "reported", "decide", "decided", "pull",
    "pulled", "return", "returned", "explain", "explained", "carry", "carried",
    "develop", "developed", "hope", "hoped", "drive", "drove", "driven",
    "break", "broke", "broken", "receive", "received", "agree", "agreed",
    "support", "supported", "remove", "removed", "return", "returned",
    "describe", "described", "create", "created", "add", "added", "apply",
    "applied", "avoid", "avoided", "prepare", "prepared", "compare", "compared",
    "declare", "declared", "improve", "improved", "maintain", "maintained",
    "establish", "established", "perform", "performed", "reflect", "reflected",
    "discuss", "discussed", "realize", "realized", "contain", "contained",
    "follow", "followed", "refer", "referred", "solve", "solved", "reduce",
    "reduced", "enable", "enabled", "operate", "operated", "expand", "expanded",
    "depend", "depended", "derive", "derived", "select", "selected", "consist",
    "consisted", "observe", "observed", "permit", "permitted", "survive",
    "survived", "belong", "belonged", "commit", "committed", "recognize",
    "recognized", "assume", "assumed", "ensure", "ensured", "indicate",
    "indicated", "continue", "continued", "exist", "existed", "obtain",
    "obtained", "represent", "represented", "conduct", "conducted",
    "replace", "replaced", "encourage", "encouraged", "match", "matched",
    "argue", "argued", "deny", "denied", "reveal", "revealed", "clarify",
    "clarified", "confirm", "confirmed", "attend", "attended", "estimate",
    "estimated", "conclude", "concluded", "engage", "engaged", "enhance",
    "enhanced", "insist", "insisted", "investigate", "investigated",
    "participate", "participated", "predict", "predicted", "propose",
    "proposed", "remind", "reminded", "respond", "responded", "restore",
    "restored", "specify", "specified", "succeed", "succeeded", "suffer",
    "suffered", "threaten", "threatened", "transform", "transformed",
    "translate", "translated", "acquire", "acquired", "adapt", "adapted",
    "adjust", "adjusted", "adopt", "adopted", "analyze", "analyzed",
    "anticipate", "anticipated", "appeal", "appealed", "appoint",
    "appointed", "approach", "approached", "approve", "approved",
    "assign", "assigned", "assist", "assisted", "assume", "assumed",
    "assure", "assured", "attach", "attached", "attack", "attacked",
    "attempt", "attempted", "attract", "attracted", "base", "based",
    "beat", "beaten", "benefit", "benefited", "bind", "bound", "blame",
    "blamed", "bleed", "bled", "blow", "blew", "blown", "burn", "burnt",
    "burst", "bury", "buried", "bust", "busted", "buzz", "buzzed",
    "calculate", "calculated", "capture", "captured", "care", "cared",
    "catch", "caught", "challenge", "challenged", "change", "changed",
    "charge", "charged", "check", "checked", "cheer", "cheered",
    "choke", "choked", "claim", "claimed", "clean", "cleaned", "clear",
    "cleared", "click", "clicked", "climb", "climbed", "close", "closed",
    "coach", "coached", "collect", "collected", "color", "colored",
    "combine", "combined", "comfort", "comforted", "command", "commanded",
    "comment", "commented", "communicate", "communicated", "complete",
    "completed", "compose", "composed", "concern", "concerned", "conclude",
    "concluded", "condition", "conditioned", "conduct", "conducted",
    "confess", "confessed", "confine", "confined", "confuse", "confused",
    "connect", "connected", "conserve", "conserved", "consider", "considered",
    "consist", "consisted", "consult", "consulted", "consume", "consumed",
    "contact", "contacted", "contain", "contained", "continue", "continued",
    "contract", "contracted", "contrast", "contrasted", "contribute",
    "contributed", "control", "controlled", "convert", "converted", "convince",
    "convinced", "cook", "cooked", "cool", "cooled", "copied", "copy",
    "correct", "corrected", "cost", "cost", "cough", "coughed", "count",
    "counted", "cover", "covered", "crack", "cracked", "crash", "crashed",
    "crawl", "crawled", "create", "created", "cross", "crossed", "crowd",
    "crowded", "crush", "crushed", "cry", "cried", "cure", "cured",
    "curl", "curled", "curve", "curved", "dam", "damaged", "dance",
    "danced", "dare", "dared", "deal", "dealt", "debate", "debated",
    "decay", "decayed", "deceive", "deceived", "decide", "decided",
    "declare", "declared", "decorate", "decorated", "decrease", "decreased",
    "defeat", "defeated", "defend", "defended", "define", "defined",
    "delay", "delayed", "delight", "delighted", "deliver", "delivered",
    "demand", "demanded", "deny", "denied", "depart", "departed",
    "depend", "depended", "deposit", "deposited", "derive", "derived",
    "describe", "described", "desert", "deserted", "deserve", "deserved",
    "design", "designed", "destroy", "destroyed", "detect", "detected",
    "determine", "determined", "develop", "developed", "devote", "devoted",
    "die", "died", "differ", "differed", "dig", "dug", "dim", "dimmed",
    "dip", "dipped", "direct", "directed", "disagree", "disagreed",
    "disappear", "disappeared", "disapprove", "disapproved", "discover",
    "discovered", "discuss", "discussed", "dive", "dived", "divide",
    "divided", "divorce", "divorced", "do", "did", "done", "double",
    "doubled", "doubt", "doubted", "drag", "dragged", "drain", "drained",
    "draw", "drew", "drawn", "dress", "dressed", "drill", "drilled",
    "drink", "drank", "drunk", "drip", "dripped", "drive", "drove",
    "driven", "drop", "dropped", "drown", "drowned", "drum", "drummed",
    "dry", "dried", "dump", "dumped", "dust", "dusted", "earn", "earned",
    "educate", "educated", "effect", "effected", "elect", "elected",
    "elevate", "elevated", "embarrass", "embarrassed", "employ", "employed",
    "empty", "emptied", "enable", "enabled", "encourage", "encouraged",
    "end", "ended", "enjoy", "enjoyed", "enter", "entered", "entertain",
    "entertained", "escape", "escaped", "establish", "established",
    "estimate", "estimated", "evaporate", "evaporated", "exchange",
    "exchanged", "excite", "excited", "exclaim", "exclaimed", "exclude",
    "excluded", "excuse", "excused", "execute", "executed", "exercise",
    "exercised", "exhaust", "exhausted", "exhibit", "exhibited", "exist",
    "existed", "expand", "expanded", "expect", "expected", "experience",
    "experienced", "explain", "explained", "explode", "exploded", "explore",
    "explored", "express", "expressed", "extend", "extended", "face",
    "faced", "fade", "faded", "fail", "failed", "fancy", "fancied",
    "fasten", "fastened", "fear", "feared", "feed", "fed", "feel", "felt",
    "fence", "fenced", "fetch", "fetched", "fight", "fought", "fill",
    "filled", "film", "filmed", "filter", "filtered", "finance", "financed",
    "find", "found", "fire", "fired", "fit", "fitted", "fix", "fixed",
    "flash", "flashed", "flee", "fled", "fling", "flung", "float",
    "floated", "flood", "flooded", "flow", "flowed", "flower", "flowered",
    "fold", "folded", "follow", "followed", "fool", "fooled", "force",
    "forced", "form", "formed", "forsake", "forsook", "forsaken",
    "frame", "framed", "frighten", "frightened", "frown", "frowned",
    "fry", "fried", "fund", "funded", "gain", "gained", "garden",
    "gardened", "gasp", "gasped", "gather", "gathered", "gaze", "gazed",
    "get", "got", "given", "give", "gave", "glance", "glanced", "glare",
    "glared", "gleam", "gleamed", "glide", "glided", "glimpse", "glimpsed",
    "glitter", "glittered", "glow", "glowed", "glue", "glued", "gnaw",
    "gnawed", "go", "went", "gone", "govern", "governed", "grab",
    "grabbed", "grate", "grated", "grease", "greased", "greet", "greeted",
    "grill", "grilled", "grimace", "grimaced", "grind", "ground", "grip",
    "gripped", "groan", "groaned", "grow", "grew", "grown", "guard",
    "guarded", "guess", "guessed", "guide", "guided", "hammer", "hammered",
    "hand", "handed", "handle", "handled", "hang", "hung", "happen",
    "happened", "harass", "harassed", "harm", "harmed", "harness",
    "harnessed", "hate", "hated", "haunt", "haunted", "head", "headed",
    "heal", "healed", "heap", "heaped", "hear", "heard", "heat", "heated",
    "help", "helped", "hesitate", "hesitated", "hide", "hid", "hidden",
    "hit", "hitch", "hitched", "hold", "held", "hole", "holed", "holler",
    "hollered", "hope", "hoped", "hover", "hovered", "howl", "howled",
    "hug", "hugged", "hum", "hummed", "hunt", "hunted", "hurl", "hurled",
    "hurry", "hurried", "hurt", "hurt", "hush", "hushed", "hustle",
    "hustled", "hypnotize", "hypnotized", "identify", "identified",
    "ignore", "ignored", "illuminate", "illuminated", "illustrate",
    "illustrated", "imagine", "imagined", "imitate", "imitated", "impact",
    "impacted", "implement", "implemented", "imply", "implied", "impress",
    "impressed", "improve", "improved", "include", "included", "increase",
    "increased", "indicate", "indicated", "induce", "induced", "indulge",
    "indulged", "influence", "influenced", "inform", "informed", "inject",
    "injected", "injure", "injured", "inquire", "inquired", "insert",
    "inserted", "inspect", "inspected", "inspire", "inspired", "install",
    "installed", "intend", "intended", "interest", "interested", "interfere",
    "interfered", "interpret", "interpreted", "interrupt", "interrupted",
    "introduce", "introduced", "invent", "invented", "invest", "invested",
    "investigate", "investigated", "invite", "invited", "involve", "involved",
    "iron", "ironed", "irritate", "irritated", "isolate", "isolated",
    "itch", "itched", "jail", "jailed", "jam", "jammed", "jog", "jogged",
    "join", "joined", "joke", "joked", "judge", "judged", "juggle",
    "juggled", "jump", "jumped", "justify", "justified", "keep", "kept",
    "kick", "kicked", "kill", "killed", "kiss", "kissed", "kneel", "knelt",
    "knit", "knitted", "knock", "knocked", "knot", "knotted", "know",
    "knew", "known", "label", "labeled", "labor", "labored", "lack",
    "lacked", "lag", "lagged", "lament", "lamented", "land", "landed",
    "last", "lasted", "laugh", "laughed", "launch", "launched", "lay",
    "laid", "lead", "led", "leak", "leaked", "lean", "leaned", "leap",
    "leaped", "learn", "learned", "leave", "left", "lend", "lent",
    "lengthen", "lengthened", "lessen", "lessened", "let", "letter",
    "lettered", "level", "leveled", "license", "licensed", "lick", "licked",
    "lie", "lay", "lain", "lift", "lifted", "light", "lit", "lighted",
    "like", "liked", "limit", "limited", "line", "lined", "linger",
    "lingered", "link", "linked", "list", "listed", "listen", "listened",
    "live", "lived", "load", "loaded", "locate", "located", "lock",
    "locked", "lodge", "lodged", "log", "logged", "long", "longed",
    "look", "looked", "loosen", "loosened", "lose", "lost", "love",
    "loved", "lower", "lowered", "mail", "mailed", "maintain", "maintained",
    "make", "made", "manage", "managed", "march", "marched", "mark",
    "marked", "marry", "married", "marvel", "marveled", "mash", "mashed",
    "match", "matched", "mate", "mated", "matter", "mattered", "mature",
    "matured", "mean", "meant", "measure", "measured", "meddle", "meddled",
    "meet", "met", "melt", "melted", "memorize", "memorized", "mend",
    "mended", "mention", "mentioned", "merge", "merged", "milk", "milked",
    "mind", "minded", "mine", "mined", "mingle", "mingled", "miss",
    "missed", "mix", "mixed", "moan", "moaned", "modify", "modified",
    "monitor", "monitored", "moor", "moored", "mop", "mopped", "mourn",
    "mourned", "move", "moved", "mow", "mowed", "multiply", "multiplied",
    "mumble", "mumbled", "murder", "murdered", "mutter", "muttered",
    "nail", "nailed", "name", "named", "need", "needed", "nest", "nested",
    "nod", "nodded", "note", "noted", "notice", "noticed", "number",
    "numbered", "obey", "obeyed", "object", "objected", "observe",
    "observed", "obtain", "obtained", "occupy", "occupied", "occur",
    "occurred", "offer", "offered", "officiate", "officiated", "open",
    "opened", "operate", "operated", "order", "ordered", "organize",
    "organized", "originate", "originated", "outline", "outlined",
    "overcome", "overcame", "overcome", "overdo", "overdid", "overdone",
    "overdraw", "overdrew", "overdrawn", "overeat", "overate", "overeaten",
    "overflow", "overflowed", "overgrow", "overgrew", "overgrown",
    "overhang", "overhung", "overhear", "overheard", "overlay", "overlaid",
    "overpay", "overpaid", "override", "overrode", "overridden", "overrun",
    "overran", "overrun", "oversee", "oversaw", "overseen", "overshoot",
    "overshot", "oversleep", "overslept", "overtake", "overtook",
    "overtaken", "overthrow", "overthrew", "overthrown", "owe", "owed",
    "own", "owned", "pack", "packed", "paddle", "paddled", "paint",
    "painted", "park", "parked", "part", "parted", "participate",
    "participated", "pass", "passed", "paste", "pasted", "pat", "patted",
    "pause", "paused", "pay", "paid", "peel", "peeled", "peep", "peeped",
    "perceive", "perceived", "perform", "performed", "permit", "permitted",
    "persuade", "persuaded", "phone", "phoned", "pick", "picked", "picture",
    "pictured", "piece", "pieced", "pile", "piled", "pin", "pinned",
    "pine", "pined", "place", "placed", "plan", "planned", "plant",
    "planted", "play", "played", "plead", "pled", "please", "pleased",
    "plod", "plodded", "plot", "plotted", "plow", "plowed", "plug",
    "plugged", "plunge", "plunged", "point", "pointed", "poke", "poked",
    "polish", "polished", "pop", "popped", "possess", "possessed", "post",
    "posted", "pour", "poured", "practice", "practiced", "pray", "prayed",
    "preach", "preached", "precede", "preceded", "predict", "predicted",
    "prefer", "preferred", "prepare", "prepared", "present", "presented",
    "preserve", "preserved", "press", "pressed", "presume", "presumed",
    "pretend", "pretended", "prevent", "prevented", "prick", "pricked",
    "print", "printed", "proceed", "proceeded", "produce", "produced",
    "profess", "professed", "program", "programmed", "progress",
    "progressed", "prohibit", "prohibited", "promise", "promised",
    "promote", "promoted", "prompt", "prompted", "propose", "proposed",
    "prosecute", "prosecuted", "protect", "protected", "prove", "proved",
    "proven", "provide", "provided", "provoke", "provoked", "publish",
    "published", "pull", "pulled", "punch", "punched", "puncture",
    "punctured", "punish", "punished", "purchase", "purchased", "push",
    "pushed", "put", "puzzle", "puzzled", "qualify", "qualified",
    "question", "questioned", "quit", "quit", "race", "raced", "rain",
    "rained", "raise", "raised", "rake", "raked", "rank", "ranked",
    "rate", "rated", "rattle", "rattled", "reach", "reached", "read",
    "read", "realize", "realized", "reap", "reaped", "rear", "reared",
    "reason", "reasoned", "receive", "received", "recognize", "recognized",
    "recommend", "recommended", "record", "recorded", "recover",
    "recovered", "recruit", "recruited", "reduce", "reduced", "refer",
    "referred", "reflect", "reflected", "refuse", "refused", "regard",
    "regarded", "register", "registered", "regret", "regretted", "regulate",
    "regulated", "rehabilitate", "rehabilitated", "reign", "reigned",
    "reinforce", "reinforced", "reject", "rejected", "rejoice", "rejoiced",
    "relate", "related", "relax", "relaxed", "release", "released",
    "rely", "relied", "remain", "remained", "remember", "remembered",
    "remind", "reminded", "remove", "removed", "render", "rendered",
    "renew", "renewed", "rent", "rented", "repair", "repaired", "repeat",
    "repeated", "replace", "replaced", "reply", "replied", "report",
    "reported", "represent", "represented", "reproduce", "reproduced",
    "request", "requested", "require", "required", "rescue", "rescued",
    "research", "researched", "resemble", "resembled", "reserve",
    "reserved", "resign", "resigned", "resist", "resisted", "resolve",
    "resolved", "respect", "respected", "respond", "responded", "rest",
    "rested", "restore", "restored", "restrict", "restricted", "result",
    "resulted", "resume", "resumed", "retain", "retained", "retire",
    "retired", "retreat", "retreated", "retrieve", "retrieved", "return",
    "returned", "reveal", "revealed", "revenge", "revenged", "reverse",
    "reversed", "review", "reviewed", "revise", "revised", "revive",
    "revived", "reward", "rewarded", "rhyme", "rhymed", "rid", "ridden",
    "ride", "rode", "ring", "rang", "rung", "rinse", "rinsed", "rise",
    "rose", "risen", "risk", "risked", "roar", "roared", "roast",
    "roasted", "rob", "robbed", "rock", "rocked", "roll", "rolled",
    "rot", "rotted", "round", "rounded", "rub", "rubbed", "ruin",
    "ruined", "rule", "ruled", "run", "ran", "rush", "rushed", "rust",
    "rusted", "sack", "sacked", "sacrifice", "sacrificed", "sadden",
    "saddened", "sail", "sailed", "satisfy", "satisfied", "save",
    "saved", "saw", "sawed", "say", "said", "scale", "scaled", "scare",
    "scared", "scatter", "scattered", "scold", "scolded", "scorch",
    "scorched", "scrape", "scraped", "scratch", "scratched", "scream",
    "screamed", "screw", "screwed", "scrub", "scrubbed", "seal",
    "sealed", "search", "searched", "seat", "seated", "secure",
    "secured", "see", "saw", "seek", "sought", "seem", "seemed",
    "seize", "seized", "select", "selected", "sell", "sold", "send",
    "sent", "sense", "sensed", "separate", "separated", "serve", "served",
    "set", "settle", "settled", "severe", "sew", "sewed", "sewn",
    "shade", "shaded", "shake", "shook", "shaken", "shape", "shaped",
    "share", "shared", "shave", "shaved", "shear", "shore", "shed",
    "shed", "shine", "shone", "ship", "shipped", "shiver", "shivered",
    "shock", "shocked", "shoot", "shot", "shop", "shopped", "shout",
    "shouted", "show", "showed", "shown", "shred", "shredded", "shrink",
    "shrank", "shrunk", "shut", "sigh", "sighed", "sign", "signed",
    "signal", "signaled", "simplify", "simplified", "sin", "sinned",
    "sing", "sang", "sung", "sink", "sank", "sunk", "sip", "sipped",
    "sit", "sat", "skate", "skated", "sketch", "sketched", "ski", "skied",
    "skip", "skipped", "slap", "slapped", "slay", "slew", "slain",
    "sleep", "slept", "slice", "sliced", "slide", "slid", "slip",
    "slipped", "slit", "slope", "sloped", "slow", "slowed", "smash",
    "smashed", "smell", "smelled", "smelt", "smile", "smiled", "smoke",
    "smoked", "snap", "snapped", "snatch", "snatched", "sneak", "sneaked",
    "snuck", "sneeze", "sneezed", "sniff", "sniffed", "snow", "snowed",
    "soak", "soaked", "solve", "solved", "soothe", "soothed", "sort",
    "sorted", "sound", "sounded", "sow", "sowed", "sown", "spare",
    "spared", "spark", "sparked", "sparkle", "sparkled", "speak", "spoke",
    "spoken", "speed", "sped", "spell", "spelled", "spelt", "spend",
    "spent", "spill", "spilled", "spilt", "spin", "spun", "spit",
    "spat", "split", "spoil", "spoiled", "spoilt", "spot", "spotted",
    "spray", "sprayed", "spread", "spread", "spring", "sprang", "sprung",
    "sprout", "sprouted", "squash", "squashed", "squeak", "squeaked",
    "squeal", "squealed", "squeeze", "squeezed", "stab", "stabbed",
    "stain", "stained", "stake", "staked", "stammer", "stammered",
    "stamp", "stamped", "stand", "stood", "stare", "stared", "start",
    "started", "starve", "starved", "stay", "stayed", "steal", "stole",
    "stolen", "steer", "steered", "step", "stepped", "stick", "stuck",
    "sting", "stung", "stink", "stank", "stunk", "stir", "stirred",
    "stitch", "stitched", "stop", "stopped", "store", "stored", "storm",
    "stormed", "stow", "stowed", "straighten", "straightened", "strain",
    "strained", "strap", "strapped", "stray", "strayed", "stream",
    "streamed", "strengthen", "strengthened", "stress", "stressed",
    "stretch", "stretched", "stride", "strode", "stridden", "strike",
    "struck", "stricken", "string", "strung", "strip", "stripped",
    "strive", "strove", "striven", "stroke", "stroked", "stuff",
    "stuffed", "stumble", "stumbled", "stun", "stunned", "submerge",
    "submerged", "succeed", "succeeded", "suck", "sucked", "suffer",
    "suffered", "suggest", "suggested", "suit", "suited", "summon",
    "summoned", "supply", "supplied", "support", "supported", "suppose",
    "supposed", "surge", "surged", "surmise", "surmised", "surprise",
    "surprised", "surround", "surrounded", "survey", "surveyed",
    "survive", "survived", "suspect", "suspected", "suspend", "suspended",
    "sustain", "sustained", "swallow", "swallowed", "swamp", "swamped",
    "swear", "swore", "sworn", "sweat", "sweated", "sweep", "swept",
    "swell", "swelled", "swollen", "swim", "swam", "swum", "swing",
    "swung", "switch", "switched", "tag", "tagged", "take", "took",
    "taken", "talk", "talked", "tame", "tamed", "tap", "tapped",
    "taste", "tasted", "tax", "taxed", "teach", "taught", "tear",
    "tore", "torn", "tease", "teased", "telephone", "telephoned",
    "tell", "told", "tempt", "tempted", "tend", "tended", "tense",
    "tensed", "term", "termed", "terrify", "terrified", "test",
    "tested", "thank", "thanked", "thatch", "thatched", "thaw", "thawed",
    "theorize", "theorized", "think", "thought", "thrive", "thrived",
    "throve", "throw", "threw", "thrown", "thrust", "thrusted",
    "thunder", "thundered", "tick", "ticked", "tickle", "tickled",
    "tie", "tied", "tighten", "tightened", "tilt", "tilted", "time",
    "timed", "tip", "tipped", "tire", "tired", "toast", "toasted",
    "tolerate", "tolerated", "toss", "tossed", "touch", "touched",
    "tour", "toured", "tow", "towed", "trace", "traced", "trade",
    "traded", "train", "trained", "transform", "transformed", "translate",
    "translated", "transport", "transported", "trap", "trapped",
    "travel", "traveled", "tread", "trod", "trodden", "treasure",
    "treasured", "treat", "treated", "treble", "trebled", "tremble",
    "trembled", "trick", "tricked", "trip", "tripped", "trot", "trotted",
    "trouble", "troubled", "trust", "trusted", "try", "tried", "tug",
    "tugged", "tumble", "tumbled", "tune", "tuned", "turn", "turned",
    "twist", "twisted", "type", "typed", "undergo", "underwent",
    "undergone", "understand", "understood", "undertake", "undertook",
    "undertaken", "undo", "undid", "undone", "undress", "undressed",
    "unfold", "unfolded", "unify", "unified", "unite", "united",
    "unlock", "unlocked", "unpack", "unpacked", "up", "upped", "update",
    "updated", "upgrade", "upgraded", "uphold", "upheld", "upset",
    "upset", "urge", "urged", "use", "used", "utilize", "utilized",
    "utter", "uttered", "value", "valued", "vanish", "vanished",
    "vary", "varied", "verify", "verified", "vex", "vexed", "vie",
    "vied", "view", "viewed", "violate", "violated", "visit", "visited",
    "voice", "voiced", "volunteer", "volunteered", "vote", "voted",
    "vow", "vowed", "wait", "waited", "wake", "woke", "woken", "walk",
    "walked", "wander", "wandered", "want", "wanted", "warm", "warmed",
    "warn", "warned", "wash", "washed", "waste", "wasted", "watch",
    "watched", "water", "watered", "wave", "waved", "wax", "waxed",
    "weaken", "weakened", "wear", "wore", "worn", "weave", "wove",
    "woven", "wed", "wedded", "weep", "wept", "weigh", "weighed",
    "welcome", "welcomed", "wet", "wetted", "whine", "whined", "whip",
    "whipped", "whirl", "whirled", "whisper", "whispered", "whistle",
    "whistled", "widen", "widened", "win", "won", "wind", "wound",
    "wink", "winked", "wipe", "wiped", "wish", "wished", "withdraw",
    "withdrew", "withdrawn", "withhold", "withheld", "withstand",
    "withstood", "witness", "witnessed", "wonder", "wondered", "work",
    "worked", "worry", "worried", "worship", "worshipped", "wrap",
    "wrapped", "wreck", "wrecked", "wrestle", "wrestled", "wring",
    "wrung", "write", "wrote", "written", "yawn", "yawned", "yell",
    "yelled", "yield", "yielded", "zip", "zipped",
    # Numbers
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
    "one", "two", "three", "four", "five", "six", "seven", "eight",
    "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
    "sixteen", "seventeen", "eighteen", "nineteen", "twenty",
    "first", "second", "third", "fourth", "fifth",
    # Markdown / formatting
    "true", "false", "null", "none", "undefined", "nan", "inf",
    "yes", "no", "ok", "okay",
    # Common file words
    "readme", "todo", "changelog", "license", "contributing", "code",
    "conduct", "security", "issues", "pull", "request", "requests",
    # Time words
    "today", "tomorrow", "yesterday", "morning", "afternoon", "evening",
    "night", "week", "month", "year", "daily", "weekly", "monthly",
    "hour", "minute", "second", "day", "date", "time", "now", "then",
    # Size words
    "small", "medium", "large", "big", "tiny", "huge", "little",
    # Direction
    "left", "right", "up", "down", "top", "bottom", "front", "back",
    "north", "south", "east", "west",
    # Colors
    "red", "green", "blue", "yellow", "orange", "purple", "black",
    "white", "gray", "grey", "brown", "pink",
    # Generic
    "thing", "stuff", "item", "object", "part", "piece", "bit", "lot",
    "set", "group", "list", "array", "map", "dict", "string", "int",
    "float", "bool", "char", "byte", "word", "text", "line", "page",
    "file", "folder", "dir", "path", "url", "link", "button", "form",
    "input", "output", "error", "warning", "info", "debug", "log",
    "config", "setting", "option", "mode", "type", "kind", "sort",
    "way", "method", "function", "class", "module", "package",
    "library", "framework", "tool", "app", "application", "program",
    "system", "service", "api", "endpoint", "route", "handler",
    "controller", "model", "view", "template", "component", "element",
    "tag", "attribute", "property", "field", "column", "row", "table",
    "database", "db", "schema", "query", "sql", "migration", "seed",
    # More noise
    "notes", "note", "memo", "journal", "diary", "entry", "record",
    "log", "draft", "version", "v1", "v2", "v3", "alpha", "beta",
    "stable", "release", "build", "deploy", "deployment", "host",
    "server", "client", "user", "admin", "guest", "account", "profile",
    "login", "logout", "auth", "authentication", "authorization",
    "permission", "role", "session", "cookie", "token", "key",
    "secret", "password", "credential", "certificate", "ssl", "tls",
    "https", "http", "ftp", "ssh", "vpn", "proxy", "firewall",
    "network", "lan", "wan", "ip", "port", "domain", "dns",
    "host", "hostname", "localhost", "127", "0", "1",
}

# Entity types we care about (regex-extracted)
ENTITY_PATTERNS = {
    "project": [
        r"(?i)#+\s*(?:project|wings?| initiative)\s*[\-:]?\s*([A-Z][A-Za-z0-9\-_\s]{2,30})",
        r"(?i)(?:building|working on|project\s+name[\s:]*)\s*([A-Z][A-Za-z0-9\-_]{2,30})",
    ],
    "company": [
        r"(?i)(?:company|startup|firm|business)\s*[\-:]?\s*([A-Z][A-Za-z0-9\-_\s&]{2,40})",
    ],
    "person": [
        r"(?i)(?:by|from|author)\s*[:\-]?\s*([A-Z][a-z]+\s[A-Z][a-z]+)",
    ],
    "technology": [
        r"(?i)(?:OpenClaw|MoltOS|Claude|GPT|Kimi|LangChain|CrewAI|AutoGen|Dify|Ollama)",
        r"(?i)(?:React|Node\.js|Python|TypeScript|Rust|Next\.js|Vue|Docker|Kubernetes)",
    ],
    "concept": [
        r"(?i)(?:AaaS|SaaS|agent|swarm|orchestration|knowledge graph|RAG|compaction|token)",
        r"(?i)(?:Picasso steal|crater landing|momentum|alignment|self-diagnostic|heartbeat)",
    ],
    "date": [
        r"\b(20\d{2}-\d{2}-\d{2})\b",
    ],
    "metric": [
        r"(?i)(?:\$[\d,]+(?:\.\d+)?[KMB]?|\d+[\d,]*\s*(?:stars?|users?|customers?|ARR|MRR|revenue))",
    ],
    "decision": [
        r"(?i)(?:decided?|decision|chosen?|chose|opted?|going with)\s*[\-:]?\s*([^\.\n]{10,200})",
    ],
}

# Relationships we can detect
RELATIONSHIP_PATTERNS = {
    "works_on": [
        r"(?i)(Nathan|Mid(a|)s)\s+(?:is\s+)?(?:working on|building|developing|creating)\s+([^\.\n]{5,100})",
    ],
    "uses": [
        r"(?i)(?:using|use[sd]|runs on|built with|powered by)\s+([A-Z][A-Za-z0-9\-_\s]{2,40})",
    ],
    "created": [
        r"(?i)(?:created?|wrote|authored|built)\s+([A-Z][A-Za-z0-9\-_\s]{2,40})",
    ],
    "abandoned": [
        r"(?i)(?:abandoned?|dropped|paused|stopped|halted|killed)\s+([A-Z][A-Za-z0-9\-_\s]{2,40})",
    ],
    "competes_with": [
        r"(?i)(?:compet(?:itor|es?|ing)\s+with|vs\.?|versus)\s+([A-Z][A-Za-z0-9\-_\s]{2,40})",
    ],
    "integrates": [
        r"(?i)(?:integrat(?:e[sd]?|ing)\s+with|connect(?:s|ed)?\s+to)\s+([A-Z][A-Za-z0-9\-_\s]{2,40})",
    ],
}

# File structure → entity type mapping
DIR_ENTITY_TYPES = {
    "wings": "project",
    "rooms": "concept",
    "drawers": "entry",
    "diaries": "diary",
    "gbrain": "pattern",
    "marrow": "core_memory",
}

# ── Graph Builder ───────────────────────────────────────────────────────────

class VaultKnowledgeGraph:
    def __init__(self):
        self.nodes: Dict[str, Dict] = {}
        self.edges: List[Dict] = []
        self.file_index: Dict[str, List[str]] = {}
        self.stats = {
            "files_parsed": 0,
            "files_skipped": 0,
            "entities_found": 0,
            "entities_known": 0,
            "entities_inferred": 0,
            "relationships_found": 0,
            "cooccurrence_edges": 0,
            "build_time": None,
        }

    def build(self):
        """Walk vault and build graph."""
        start_time = datetime.now(timezone.utc)

        md_files = list(VAULT_ROOT.rglob("*.md"))
        print(f"🔍 Found {len(md_files)} markdown files")

        for file_path in md_files:
            self._parse_file(file_path)

        # Add co-occurrence edges (entities appearing in same file)
        self._add_cooccurrence_edges()

        self.stats["build_time"] = (datetime.now(timezone.utc) - start_time).total_seconds()
        self._save()

        return self.stats

    def _parse_file(self, file_path: Path):
        """Parse a single markdown file."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception:
            self.stats["files_skipped"] += 1
            return

        self.stats["files_parsed"] += 1
        rel_path = str(file_path.relative_to(VAULT_ROOT))
        file_nodes = []

        # 1. Extract known entities first (whitelist)
        for entity_name, entity_type in KNOWN_ENTITIES.items():
            pattern = re.compile(rf'(?i)\b{re.escape(entity_name)}\b')
            matches = list(pattern.finditer(content))
            if matches:
                node_id = self._normalize_id(entity_name)
                if node_id not in self.nodes:
                    self.nodes[node_id] = {
                        "id": node_id,
                        "label": entity_name,
                        "type": entity_type,
                        "files": [],
                        "contexts": [],
                        "mention_count": 0,
                        "source": "known",
                    }
                    self.stats["entities_known"] += 1
                    self.stats["entities_found"] += 1

                node = self.nodes[node_id]
                if rel_path not in node["files"]:
                    node["files"].append(rel_path)
                node["mention_count"] += len(matches)

                for match in matches[:3]:  # Capture first 3 contexts
                    start = max(0, match.start() - 80)
                    end = min(len(content), match.end() + 80)
                    context = content[start:end].strip()
                    if context not in node["contexts"]:
                        node["contexts"].append(context)

                if node_id not in file_nodes:
                    file_nodes.append(node_id)

        # 2. Extract structured entities from regex patterns
        for entity_type, patterns in ENTITY_PATTERNS.items():
            for pattern in patterns:
                for match in re.finditer(pattern, content):
                    entity_text = match.group(1) if match.lastindex else match.group(0)
                    entity_text = self._clean_entity(entity_text)

                    if not entity_text or len(entity_text) < 3 or len(entity_text) > 60:
                        continue

                    node_id = self._normalize_id(entity_text)

                    # Skip if already exists as known entity
                    if node_id in self.nodes and self.nodes[node_id].get("source") == "known":
                        continue

                    # Skip blocklist
                    if entity_text.lower() in BLOCKLIST:
                        continue

                    if node_id not in self.nodes:
                        self.nodes[node_id] = {
                            "id": node_id,
                            "label": entity_text,
                            "type": entity_type,
                            "files": [],
                            "contexts": [],
                            "mention_count": 0,
                            "source": "regex",
                        }
                        self.stats["entities_found"] += 1

                    node = self.nodes[node_id]
                    if rel_path not in node["files"]:
                        node["files"].append(rel_path)
                    node["mention_count"] += 1

                    start = max(0, match.start() - 80)
                    end = min(len(content), match.end() + 80)
                    context = content[start:end].strip()
                    if context not in node["contexts"]:
                        node["contexts"].append(context)

                    if node_id not in file_nodes:
                        file_nodes.append(node_id)

        # 3. Infer entities from file structure
        self._infer_from_path(file_path, rel_path, file_nodes)

        # 4. Extract relationships from patterns
        self._extract_relationships(content, rel_path, file_nodes)

        self.file_index[rel_path] = file_nodes

    def _clean_entity(self, text: str) -> str:
        """Clean extracted entity text."""
        text = text.strip()
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'^[\s\-\*\.#\(\)\[\]\{\}"\'\`\|]+', '', text)
        text = re.sub(r'[\s\-\*\.#\(\)\[\]\{\}"\'\`\|]+$', '', text)
        # Remove markdown formatting
        text = re.sub(r'\*\*?|\*\*\*|__?|\[|\]|\(|\)', '', text)
        return text[:80]

    def _infer_from_path(self, file_path: Path, rel_path: str, file_nodes: List[str]):
        """Infer entities from file/directory structure."""
        parts = rel_path.split(os.sep)

        for i, part in enumerate(parts):
            # Skip generic names
            if part.lower() in {"entries", "drawers", "rooms", "wings", "vault"}:
                continue

            # Check if directory maps to entity type
            if i < len(parts) - 1:  # It's a directory
                dir_type = DIR_ENTITY_TYPES.get(part.lower())
                if dir_type:
                    # The next part is likely an entity of this type
                    next_part = parts[i + 1]
                    if next_part.endswith('.md'):
                        next_part = next_part[:-3]

                    # Clean up
                    entity_name = next_part.replace('-', ' ').replace('_', ' ').title()
                    if len(entity_name) >= 3 and len(entity_name) <= 50:
                        node_id = self._normalize_id(entity_name)
                        if node_id not in self.nodes:
                            self.nodes[node_id] = {
                                "id": node_id,
                                "label": entity_name,
                                "type": dir_type,
                                "files": [rel_path],
                                "contexts": [f"Inferred from directory: {rel_path}"],
                                "mention_count": 1,
                                "source": "inferred",
                            }
                            self.stats["entities_inferred"] += 1
                            self.stats["entities_found"] += 1
                        else:
                            if rel_path not in self.nodes[node_id]["files"]:
                                self.nodes[node_id]["files"].append(rel_path)

                        if node_id not in file_nodes:
                            file_nodes.append(node_id)

    def _extract_relationships(self, content: str, rel_path: str, file_nodes: List[str]):
        """Extract explicit relationships from content."""
        for relation_type, patterns in RELATIONSHIP_PATTERNS.items():
            for pattern in patterns:
                for match in re.finditer(pattern, content):
                    groups = match.groups()
                    if len(groups) >= 1:
                        target_text = self._clean_entity(groups[-1])
                        if len(target_text) < 3:
                            continue

                        target_id = self._normalize_id(target_text)
                        source_id = self._normalize_id(groups[0]) if len(groups) > 1 else "nathan"

                        # Ensure nodes exist
                        for node_id, label in [(source_id, groups[0] if len(groups) > 1 else "Nathan"),
                                               (target_id, target_text)]:
                            if node_id not in self.nodes:
                                self.nodes[node_id] = {
                                    "id": node_id,
                                    "label": label,
                                    "type": "unknown",
                                    "files": [rel_path],
                                    "contexts": [],
                                    "mention_count": 1,
                                    "source": "relationship",
                                }
                                self.stats["entities_found"] += 1

                        edge = {
                            "source": source_id,
                            "target": target_id,
                            "relation": relation_type,
                            "file": rel_path,
                            "context": content[max(0, match.start()-60):min(len(content), match.end()+60)].strip(),
                        }
                        self.edges.append(edge)
                        self.stats["relationships_found"] += 1

    def _add_cooccurrence_edges(self):
        """Add edges between entities that appear in the same file."""
        for file_path, node_ids in self.file_index.items():
            if len(node_ids) < 2:
                continue

            # Create edges between all pairs in this file
            for i, source_id in enumerate(node_ids):
                for target_id in node_ids[i+1:]:
                    # Only connect if types are different (more meaningful)
                    source_type = self.nodes.get(source_id, {}).get("type", "unknown")
                    target_type = self.nodes.get(target_id, {}).get("type", "unknown")

                    if source_type != target_type:
                        edge = {
                            "source": source_id,
                            "target": target_id,
                            "relation": "cooccurs_with",
                            "file": file_path,
                            "context": f"Appears together in {file_path}",
                        }
                        self.edges.append(edge)
                        self.stats["cooccurrence_edges"] += 1

    def _normalize_id(self, text: str) -> str:
        """Create a normalized ID from text."""
        normalized = re.sub(r'[^a-z0-9\-]', '-', text.lower().strip())
        normalized = re.sub(r'-+', '-', normalized)
        return normalized[:60]

    def _save(self):
        """Persist graph to disk."""
        GRAPH_FILE.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "nodes": self.nodes,
            "edges": self.edges,
            "stats": self.stats,
            "file_index": self.file_index,
            "built_at": datetime.now(timezone.utc).isoformat(),
        }
        with open(GRAPH_FILE, 'w') as f:
            json.dump(data, f, indent=2)

        # Build index
        index = {
            "by_type": defaultdict(list),
            "by_file": defaultdict(list),
            "by_label": {},
            "by_source": defaultdict(list),
        }
        for node_id, node in self.nodes.items():
            index["by_type"][node["type"]].append(node_id)
            index["by_source"][node.get("source", "regex")].append(node_id)
            for file in node["files"]:
                index["by_file"][file].append(node_id)
            index["by_label"][node["label"].lower()] = node_id

        with open(INDEX_FILE, 'w') as f:
            json.dump(index, f, indent=2)

        print(f"💾 Saved graph: {len(self.nodes)} nodes, {len(self.edges)} edges")
        print(f"   Known: {self.stats['entities_known']} | Regex: {self.stats['entities_found'] - self.stats['entities_known'] - self.stats['entities_inferred']} | Inferred: {self.stats['entities_inferred']}")
        print(f"   Explicit relations: {self.stats['relationships_found']} | Co-occurrence: {self.stats['cooccurrence_edges']}")

    def query(self, question: str) -> List[Dict]:
        """Graph RAG query with improved scoring."""
        if not GRAPH_FILE.exists():
            print("❌ Graph not built. Run --build first.")
            return []

        with open(GRAPH_FILE) as f:
            data = json.load(f)

        self.nodes = data["nodes"]
        self.edges = data["edges"]
        question_lower = question.lower()
        question_words = [w for w in question_lower.split() if len(w) > 2]

        results = []
        scored_nodes = []

        for node_id, node in self.nodes.items():
            score = 0
            label_lower = node["label"].lower()
            type_lower = node["type"].lower()

            # Direct keyword matches
            for word in question_words:
                if word in label_lower:
                    score += 5  # Higher weight for label match
                if word in type_lower:
                    score += 2

            # Known entities get bonus
            if node.get("source") == "known":
                score += 3

            # Context matches
            for ctx in node.get("contexts", [])[:3]:
                ctx_lower = ctx.lower()
                for word in question_words:
                    if word in ctx_lower:
                        score += 1

            # File path match
            for file in node.get("files", []):
                file_lower = file.lower()
                for word in question_words:
                    if word in file_lower:
                        score += 2

            if score > 0:
                scored_nodes.append((node_id, score, node))

        scored_nodes.sort(key=lambda x: x[1], reverse=True)

        for node_id, score, node in scored_nodes[:15]:
            related_edges = [
                e for e in self.edges
                if e["source"] == node_id or e["target"] == node_id
            ]
            results.append({
                "node": node,
                "score": score,
                "related_edges": related_edges[:5],
            })

        return results

    def get_entity(self, name: str) -> Optional[Dict]:
        """Get full info about an entity."""
        if not GRAPH_FILE.exists():
            return None

        with open(GRAPH_FILE) as f:
            data = json.load(f)

        # Try exact match first
        node_id = self._normalize_id(name)
        if node_id in data["nodes"]:
            node = data["nodes"][node_id]
            related = [
                e for e in data["edges"]
                if e["source"] == node_id or e["target"] == node_id
            ]
            return {"node": node, "edges": related}

        # Try label search
        for nid, node in data["nodes"].items():
            if name.lower() in node["label"].lower() or node["label"].lower() in name.lower():
                related = [e for e in data["edges"] if e["source"] == nid or e["target"] == nid]
                return {"node": node, "edges": related}

        return None

    def get_stats(self) -> Dict:
        """Get graph statistics."""
        if not GRAPH_FILE.exists():
            return {"status": "not_built"}

        with open(GRAPH_FILE) as f:
            data = json.load(f)

        type_counts = Counter()
        source_counts = Counter()
        for node in data["nodes"].values():
            type_counts[node["type"]] += 1
            source_counts[node.get("source", "regex")] += 1

        relation_counts = Counter()
        for edge in data["edges"]:
            relation_counts[edge["relation"]] += 1

        return {
            "status": "built",
            "nodes": len(data["nodes"]),
            "edges": len(data["edges"]),
            "files_parsed": data["stats"]["files_parsed"],
            "build_time_seconds": data["stats"]["build_time"],
            "entity_types": dict(type_counts.most_common(15)),
            "entity_sources": dict(source_counts.most_common(10)),
            "relation_types": dict(relation_counts.most_common(10)),
            "built_at": data.get("built_at", "unknown"),
        }


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Vault Knowledge Graph v2")
    parser.add_argument("--build", action="store_true", help="Build graph from vault")
    parser.add_argument("--query", type=str, help="Query with natural language")
    parser.add_argument("--entity", type=str, help="Get specific entity info")
    parser.add_argument("--stats", action="store_true", help="Show statistics")
    args = parser.parse_args()

    graph = VaultKnowledgeGraph()

    if args.build:
        print("🏗️ Building vault knowledge graph v2...")
        stats = graph.build()
        print(f"\n✅ Done!")
        print(f"   Files: {stats['files_parsed']}")
        print(f"   Entities: {stats['entities_found']}")
        print(f"   Known: {stats['entities_known']} | Inferred: {stats['entities_inferred']}")
        print(f"   Explicit relations: {stats['relationships_found']}")
        print(f"   Co-occurrence edges: {stats['cooccurrence_edges']}")
        print(f"   Time: {stats['build_time']:.1f}s")

    elif args.query:
        results = graph.query(args.query)
        print(f"🔍 Query: '{args.query}'")
        print(f"   Found {len(results)} relevant nodes\n")
        for i, r in enumerate(results[:8], 1):
            node = r["node"]
            print(f"{i}. [{node['type'].upper()}] {node['label']} (score: {r['score']})")
            print(f"   Source: {node.get('source', 'regex')} | Mentions: {node['mention_count']} | Files: {len(node['files'])}")
            if r["related_edges"]:
                rels = ', '.join(f"{e['relation']}→{e['target'] if e['source'] == node['id'] else e['source']}" 
                                for e in r["related_edges"][:3])
                print(f"   Relations: {rels}")
            print()

    elif args.entity:
        info = graph.get_entity(args.entity)
        if info:
            node = info["node"]
            print(f"📌 {node['label']} ({node['type']})")
            print(f"   ID: {node['id']} | Source: {node.get('source', 'regex')}")
            print(f"   Mentions: {node['mention_count']}")
            print(f"   Files: {', '.join(node['files'][:5])}")
            print(f"\n   Relations ({len(info['edges'])}):")
            for e in info["edges"][:12]:
                other = e['target'] if e['source'] == node['id'] else e['source']
                print(f"   • [{e['relation']}] → {other}")
            print(f"\n   Contexts:")
            for ctx in node.get("contexts", [])[:3]:
                print(f"   • ...{ctx[:140]}...")
        else:
            print(f"❌ Entity '{args.entity}' not found")

    elif args.stats:
        stats = graph.get_stats()
        if stats["status"] == "not_built":
            print("❌ Graph not built. Run --build first.")
        else:
            print(f"📊 Vault Knowledge Graph v2")
            print(f"   Nodes: {stats['nodes']} | Edges: {stats['edges']}")
            print(f"   Files: {stats['files_parsed']} | Build: {stats['build_time_seconds']:.1f}s")
            print(f"\n   Entity types:")
            for t, c in stats["entity_types"].items():
                print(f"      {t}: {c}")
            print(f"\n   Entity sources:")
            for s, c in stats["entity_sources"].items():
                print(f"      {s}: {c}")
            print(f"\n   Relations:")
            for r, c in stats["relation_types"].items():
                print(f"      {r}: {c}")

    else:
        print("Usage:")
        print("  --build      Build graph")
        print("  --query '...' Query graph")
        print("  --entity 'X' Get entity")
        print("  --stats      Show stats")


if __name__ == "__main__":
    main()
