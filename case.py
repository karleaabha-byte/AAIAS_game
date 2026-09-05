"""
case.py - Static case data for "Who Is the Mole?"

Clue chain:
- Laboratory (always full, not sabotage-able): acrostic spells "FOUR" -> digit 4.
- Storage (sabotage-able): riddle answer "BREEZE" (6 letters) -> digit 6.
- Cafeteria (sabotage-able): PIN's first two digits are ALWAYS hidden (the
  player must derive them from Lab + Storage). Only "19" is ever visible.
  Sabotage/help instead affect how clearly the job title reads — a second,
  redundant clue channel that never fully disappears.
"""

CHARACTERS = ["Raven", "Zephyr", "Luca", "Marinette", "Adrien"]
MOLE = "Zephyr"

LAB_NUMBER = 4
STORAGE_ANSWER = "BREEZE"
STORAGE_NUMBER = len(STORAGE_ANSWER)  # 6
CORRECT_PIN = f"{LAB_NUMBER}{STORAGE_NUMBER}19"  # "4619"

CASE_INTRO = """
### 🧟 Research Facility — Night Shift Incident Report

Half the supply cabinets have been raided, a couple of pieces of equipment
sabotaged, and morale is through the floor. Five staff members were on shift
last night: **Raven, Zephyr, Luca, Marinette, and Adrien.**

Rumor has it there's a mole among them — someone quietly working against the
facility from the inside.

You have **9 actions** to crack the case:
- Investigate all **3 rooms** (1 visit each)
- Question all **5 staff members** (1 question each)
- Make **1 final accusation**

*Old trivia pinned by the door, from back when this wing was a weather
station: staff used to get informal nicknames based on wind and weather
terms. Nobody's sure why that tradition stuck around.*
"""

PROFILES = {
    "Raven": {
        "job": "Head Chemist",
        "true_alibi": (
            "I spent the whole night alone in the Laboratory, recalibrating the "
            "incubators. Nobody else came in — the door was locked the entire time."
        ),
    },
    "Zephyr": {
        "job": "Supply Coordinator",
        "true_alibi": "I was doing a full inventory count in Storage, all by myself.",
        "false_alibi": "I stepped into the Laboratory for a few minutes to borrow a tool from Raven.",
    },
    "Luca": {
        "job": "Security Officer",
        "true_alibi": "I was patrolling the corridor right outside the Cafeteria most of the night.",
    },
    "Marinette": {
        "job": "Medic",
        "true_alibi": "I was in the medical bay all night, tending to a worker who'd come down with a fever.",
    },
    "Adrien": {
        "job": "Engineer",
        "true_alibi": "I was down in the generator room, fixing a fuel line that had started leaking.",
    },
}

QUESTION_BANK = [
    ("alibi", "Where were you last night, during the incident?"),
    ("suspicion", "Did you notice anything strange going on?"),
    ("vending", "Do you know anything about the vending machine acting up?"),
    ("riddle", "Any idea who scratched that riddle onto the storage wall?"),
    ("trust", "Who around here would you trust the least, and why?"),
]

_INNOCENT_ANSWERS = {
    "Raven": {
        "suspicion": "The vents have been rattling more than usual. Might be nothing.",
        "vending": "Not really my department, I barely leave the lab.",
        "riddle": "No idea. I don't even go into Storage much.",
        "trust": "I'd rather not point fingers without proof.",
    },
    "Luca": {
        "suspicion": "The cafeteria's vending machine has been glitching for days.",
        "vending": "Funny you ask — I saw the Supply Coordinator hanging around it pretty late last night.",
        "riddle": "Didn't see anyone near Storage, but I wasn't posted there.",
        "trust": "Everyone's got secrets on a night shift like this.",
    },
    "Marinette": {
        "suspicion": "One of the patients kept muttering about a 'draft' from the vents.",
        "vending": "I heard it ate someone's snack money, that's all I know.",
        "riddle": "No clue, sorry — I was stuck in the medical bay all night.",
        "trust": "I try to think the best of everyone here.",
    },
    "Adrien": {
        "suspicion": "The generator's been fine, but I did hear something rattling in the vent system.",
        "vending": "It's been eating coins all week, not just last night.",
        "riddle": "I wouldn't know — I never got further than the generator room.",
        "trust": "Hard to say. Maybe ask Luca, he sees everyone come and go.",
    },
}

_ZEPHYR_ANSWERS = {
    "suspicion": {
        "truth": "Now that you mention it... I felt a strange draft near the vents last night. Probably nothing.",
        "lie": "Nope, nothing seemed off to me at all.",
    },
    "vending": {
        "truth": "Oh, I actually restocked it myself last night — comes with the job.",
        "lie": "No idea, I don't really deal with the cafeteria side of things.",
    },
    "riddle": {
        "truth": "Storage riddles? I might've scratched a line or two on that wall out of boredom, honestly.",
        "lie": "Haven't touched that wall. No clue who did.",
    },
    "trust": {
        "truth": "Honestly? I don't suspect anyone. We all get along fine.",
        "lie": "Beats me. Everyone seems trustworthy enough.",
    },
}

ROOM_INFO = {
    "Laboratory": {
        "emoji": "🧪",
        "flavor": "Rows of cracked beakers under a flickering light. A note is pinned to the corkboard.",
    },
    "Storage": {
        "emoji": "📦",
        "flavor": "Shelves half-emptied, boxes overturned. Someone's scratched a riddle into the wall in grease pencil.",
    },
    "Cafeteria": {
        "emoji": "🍽️",
        "flavor": "The vending machine hums quietly. A restocking log is clipped to its side.",
    },
}

# ---------- Laboratory: acrostic note (never sabotage-able) ----------
# First letters read top to bottom spell "FOUR". No hint text — the
# highlighted letters are the only nudge given.
_LAB_LINES = [
    ("F", "our vents line the ceiling, and every one of them shows fresh scuff marks."),
    ("O", "nly staff badges can open the vent hatch — the maintenance chart confirms it."),
    ("U", "nderneath the middle vent, damp footprints trail off toward the hallway."),
    ("R", "ecords show someone accessed the vent controls well after midnight."),
]


def get_lab_clue():
    return _LAB_LINES


# ---------- Storage: riddle (answer: BREEZE, 6 letters) ----------
_RIDDLE_LINES = [
    "I cannot be seen, but I shake every leaf.",
    "I fill the sails of ships, yet I weigh nothing at all.",
    "I caress your skin on a warm afternoon, gentle and soft.",
    "Sailors bless me on a calm day, and curse me when I turn into a storm.",
    "What am I?",

]
_RIDDLE_DECOY = "I can also 'travel' through a crowd as a rumor."
_RIDDLE_HELPER = "Scrawled beneath, in different handwriting: something you'd feel standing on a beach."


def get_storage_clue(decision):
    """Returns a list of dicts: {'text', 'struck', 'decoy', 'helper'}"""
    if decision == "sabotage":
        return [
            {"text": _RIDDLE_LINES[0], "struck": True, "decoy": False, "helper": False},
            {"text": _RIDDLE_LINES[1], "struck": False, "decoy": False, "helper": False},
            {"text": _RIDDLE_DECOY, "struck": False, "decoy": True, "helper": False},
            {"text": _RIDDLE_LINES[2], "struck": False, "decoy": False, "helper": False},
            {"text": _RIDDLE_LINES[3], "struck": False, "decoy": False, "helper": False},
        ]
    lines = [{"text": l, "struck": False, "decoy": False, "helper": False} for l in _RIDDLE_LINES]
    if decision == "help":
        lines.append({"text": _RIDDLE_HELPER, "struck": False, "decoy": False, "helper": True})
    return lines


# ---------- Cafeteria: restocking log / PIN ----------
# The first two PIN digits (the derived ones) are ALWAYS hidden — the player
# must work them out from Lab + Storage. Only "1" and "9" are ever visible.
# Sabotage/help instead affect the job-title fragment, a corroborating clue
# that's never fully destroyed.
def get_cafeteria_clue(decision):
    if decision == "sabotage":
        job = "Supply Coor" + "▓" * 6  # smudged but still a legible fragment
    elif decision == "help":
        job = "Supply Coordinator"
    else:
        job = "Supply Coord▓nator"  # lightly worn, still readable
    pin_digits = list(CORRECT_PIN)          # e.g. ["4","6","1","9"]
    redacted = [True, True, False, False]   # digits 1-2 always hidden, 3-4 always shown
    return {"job": job, "pin_digits": pin_digits, "redacted": redacted}


def get_answer(character, question_key, tell_truth=True):
    if character == MOLE:
        if question_key == "alibi":
            return PROFILES[MOLE]["true_alibi"] if tell_truth else PROFILES[MOLE]["false_alibi"]
        variants = _ZEPHYR_ANSWERS.get(question_key)
        if variants:
            return variants["truth"] if tell_truth else variants["lie"]
        return "..."
    if question_key == "alibi":
        return PROFILES[character]["true_alibi"]
    return _INNOCENT_ANSWERS.get(character, {}).get(question_key, "Not much to say about that.")
