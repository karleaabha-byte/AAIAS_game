"""
case.py - Enhanced case data with interconnected alibis and background context.
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
facility from the inside. You have **12 actions** to crack the case (3 extra for
investigation breadth).

- Investigate all **3 rooms** (1 visit each)
- Question all **5 staff members** (1 question each)
- Make **1 final accusation**
- That leaves **3 actions** for additional investigation.
"""

# --- BACKGROUND CONTEXT: Facts established independently ---
BACKGROUND = {
    "security_log": {
        "title": "Security Access Log (11:30 PM - 12:30 AM)",
        "entries": [
            "11:47 PM — Lab Door: Unlocked by Raven's badge",
            "11:50 PM — Vent Access Panel (Storage): Opened using maintenance override",
            "11:52 PM — Vending Machine (Cafeteria): Restocking in progress",
            "12:03 AM — Vent Access Panel (Storage): Closed",
            "12:15 AM — Lab Door: Locked by Raven's badge",
        ]
    },
    "timeline": {
        "title": "Incident Timeline",
        "notes": [
            "11:45 PM — Facilities report first equipment malfunction",
            "11:50 PM — Vending machine restocking noted by corridor patrol",
            "12:00 AM — Supply cabinet discovered open and partially emptied",
            "12:10 AM — Vent system alarm triggered (maintenance override detected)",
        ]
    },
    "maintenance": {
        "title": "Vent Access Authorization",
        "notes": [
            "Only 2 staff members have vent access: Supply Coordinator, Maintenance Chief",
            "Maintenance Chief: Off-shift (not present last night)",
            "Supply Coordinator: On-shift all night",
        ]
    },
}

PROFILES = {
    "Raven": {
        "job": "Head Chemist",
        "location": "Laboratory",
        "true_alibi": (
            "I was alone in the Laboratory all night, recalibrating the incubators. "
            "I came in around 11:45, locked the door, and didn't leave until after midnight."
        ),
    },
    "Zephyr": {
        "job": "Supply Coordinator",
        "location": "Storage",
        "true_alibi": "I was in Storage doing inventory count all night. Didn't leave once.",
        "false_alibi": "I was mostly in Storage, but I did pop into the Lab briefly to help Raven with something around 11:50.",
    },
    "Luca": {
        "job": "Security Officer",
        "location": "Corridor Patrol",
        "true_alibi": "I was patrolling the corridors and monitoring the security feed all night. Nothing unusual on camera until the alarm.",
    },
    "Marinette": {
        "job": "Medic",
        "location": "Medical Bay",
        "true_alibi": "I was treating a worker in the medical bay all night. They had a high fever, so I stayed with them the whole time.",
    },
    "Adrien": {
        "job": "Engineer",
        "location": "Generator Room",
        "true_alibi": "I was in the generator room fixing a fuel leak. Started around 11:30, finished around 12:15 AM.",
    },
}

QUESTION_BANK = [
    ("alibi", "Walk me through your movements last night between 11:30 PM and 12:30 AM."),
    ("vent", "Do you have authorization to access the ventilation system?"),
    ("vending", "Did you go near the vending machine or the supply areas?"),
    ("observation", "Did you see anyone acting unusually or in places they shouldn't be?"),
    ("timeline", "When exactly did you arrive and leave your assigned area?"),
]

_INNOCENT_ANSWERS = {
    "Raven": {
        "alibi": (
            "I unlocked the lab around 11:45 and spent the whole night there alone, "
            "working on the incubators. Locked up and left after midnight."
        ),
        "vent": "No, I don't have vent access. That's restricted to Supply and Maintenance.",
        "vending": "Not at all. I was in the lab the entire time.",
        "observation": "I heard some unusual sounds near the vents around 11:50, but I assumed it was just the system.",
        "timeline": "Arrived 11:45, left around 12:20. No breaks.",
    },
    "Luca": {
        "alibi": (
            "I was on corridor patrol the entire shift, monitoring the security cameras. "
            "I saw the restocking happen in the cafeteria around 11:50."
        ),
        "vent": "No, I don't have access. Only the Supply Coordinator and Maintenance can touch those.",
        "vending": "I saw someone restocking the vending machine around 11:50 PM. Looked routine.",
        "observation": "The supply coordinator seemed to be moving around more than usual, but nothing overtly suspicious.",
        "timeline": "Patrol from 11:30 until end of shift. Stationary in security office monitoring feeds.",
    },
    "Marinette": {
        "alibi": (
            "I was in the medical bay all night treating a worker who came in sick. "
            "Never left their side."
        ),
        "vent": "No, I wouldn't have access to that. That's a Supply Coordinator thing.",
        "vending": "I wasn't near the vending machine. I was in the medical bay.",
        "observation": "My patient mentioned hearing something rattling in the vents around midnight, but I didn't investigate.",
        "timeline": "Medical bay from 11:00 PM onward. The patient arrived around 11:20.",
    },
    "Adrien": {
        "alibi": (
            "I was in the generator room fixing a fuel leak. Arrived around 11:30, "
            "took me about 45 minutes. Left around 12:15."
        ),
        "vent": "No, I don't have vent access. That's restricted to Supply and Maintenance.",
        "vending": "I didn't go near the vending machine.",
        "observation": "I heard something in the vent system around 11:50 or so. Sounded like movement.",
        "timeline": "Generator room 11:30 to 12:15 AM. No breaks.",
    },
}

_ZEPHYR_ANSWERS = {
    "alibi": {
        "truth": (
            "I was in Storage doing the nightly inventory. Started around 11:30, "
            "kept at it the whole time."
        ),
        "lie": (
            "I was in Storage, but I did step into the lab around 11:50 to help Raven "
            "with something real quick. Only took a few minutes."
        ),
    },
    "vent": {
        "truth": "Yeah, I have full vent access as Supply Coordinator. Part of the job.",
        "lie": "No, I don't have vent access. Why would I?",
    },
    "vending": {
        "truth": "I restocked the vending machine around 11:50. That's a regular task for me.",
        "lie": "I wasn't near the vending machine. I was focused on inventory.",
    },
    "observation": {
        "truth": "Nothing unusual that I noticed. Just a normal night.",
        "lie": "I heard some people moving around, but couldn't tell who.",
    },
    "timeline": {
        "truth": "Storage from 11:30 onward. Left around 12:25.",
        "lie": "I was in Storage the whole time, didn't leave once.",
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

_LAB_LINES = [
    ("F", "our vents line the ceiling, and every one of them shows fresh scuff marks."),
    ("O", "nly staff badges can open the vent hatch — the maintenance chart confirms it."),
    ("U", "nderneath the middle vent, damp footprints trail off toward the hallway."),
    ("R", "ecords show someone accessed the vent controls well after midnight."),
]

_RIDDLE_LINES = [
    "I cannot be seen, but I shake every leaf.",
    "I fill the sails of ships, yet I weigh nothing at all.",
    "I can also 'travel' through a crowd as a rumor.",
    "Sailors bless me on a calm day, and curse me when I turn into a storm.",
    "What am I?",
]
_RIDDLE_DECOY = "I am wild and fierce, not soft or gentle."
_RIDDLE_HELPER = "Scrawled beneath, in different handwriting: something you'd feel standing on a beach."


def get_lab_clue():
    return _LAB_LINES


def get_storage_clue(decision):
    if decision == "sabotage":
        return [
            {"text": _RIDDLE_LINES[0], "struck": True, "decoy": False, "helper": False},
            {"text": _RIDDLE_LINES[1], "struck": False, "decoy": False, "helper": False},
            {"text": _RIDDLE_DECOY, "struck": False, "decoy": True, "helper": False},
            {"text": _RIDDLE_LINES[2], "struck": False, "decoy": False, "helper": False},
            {"text": _RIDDLE_LINES[3], "struck": False, "decoy": False, "helper": False},
            {"text": _RIDDLE_LINES[4], "struck": False, "decoy": False, "helper": False},
        ]
    lines = [{"text": l, "struck": False, "decoy": False, "helper": False} for l in _RIDDLE_LINES]
    if decision == "help":
        lines.append({"text": _RIDDLE_HELPER, "struck": False, "decoy": False, "helper": True})
    return lines


def get_cafeteria_clue(decision):
    if decision == "sabotage":
        job = "Supply Coor" + "▓" * 6
    elif decision == "help":
        job = "Supply Coordinator"
    else:
        job = "Supply Coord▓nator"
    pin_digits = list(CORRECT_PIN)
    redacted = [True, True, False, False]
    return {"job": job, "pin_digits": pin_digits, "redacted": redacted}


def get_answer(character, question_key, tell_truth=True):
    if character == MOLE:
        if question_key == "alibi":
            return PROFILES[MOLE]["true_alibi"] if tell_truth else PROFILES[MOLE]["false_alibi"]
        variants = _ZEPHYR_ANSWERS.get(question_key)
        if variants:
            return variants["truth"] if tell_truth else variants["lie"]
        return "..."
    return _INNOCENT_ANSWERS.get(character, {}).get(question_key, "I don't have much to say about that.")
