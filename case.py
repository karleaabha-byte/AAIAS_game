"""
case.py - Enhanced case data with interconnected alibis and specific details.

The alibis now form a timeline that either validates or contradicts each other.
Innocent characters' stories reinforce each other. Zephyr's story has gaps and
contradicts with Raven's.
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
"""

PROFILES = {
    "Raven": {
        "job": "Head Chemist",
        "location": "Laboratory",
        "true_alibi": (
            "I spent the whole night alone in the Laboratory, recalibrating the incubators. "
            "The door was locked from the inside — nobody could have gotten in."
        ),
    },
    "Zephyr": {
        "job": "Supply Coordinator",
        "location": "Storage",
        "true_alibi": "I was doing a full inventory count in Storage, all by myself.",
        "false_alibi": "I stepped into the Laboratory around 11:45 PM to borrow a tool from Raven.",
    },
    "Luca": {
        "job": "Security Officer",
        "location": "Cafeteria Corridor",
        "true_alibi": "I was patrolling the corridor outside the Cafeteria most of the night. I even saw the Supply Coordinator restocking the vending machine around 11:50 PM.",
    },
    "Marinette": {
        "job": "Medic",
        "location": "Medical Bay",
        "true_alibi": "I was in the medical bay all night, tending to a worker who'd come down with a fever. Didn't leave for a second.",
    },
    "Adrien": {
        "job": "Engineer",
        "location": "Generator Room",
        "true_alibi": "I was down in the generator room, fixing a fuel line that had started leaking. Took me about 3 hours, finished around midnight.",
    },
}

QUESTION_BANK = [
    ("alibi", "Where were you last night, and do you have anyone who can corroborate it?"),
    ("suspicion", "Did you notice anything strange going on?"),
    ("vending", "Did you see anyone near the vending machine or the restocking log?"),
    ("access", "Do you have access to the ventilation system?"),
    ("trust", "Who around here would you trust the least, and why?"),
]

_INNOCENT_ANSWERS = {
    "Raven": {
        "suspicion": "The vents have been rattling more than usual. And I heard footsteps in the hallway around 11:45.",
        "vending": "Not really my department, I barely leave the lab.",
        "access": "Only the Supply Coordinator has full vent access on night shift. It's in the maintenance chart.",
        "trust": "I'd rather not point fingers without proof.",
    },
    "Luca": {
        "suspicion": "The cafeteria's vending machine has been glitching. Also, I saw the Supply Coordinator restocking it around 11:50.",
        "vending": "I literally watched Zephyr restocking it late last night. They seemed to be lingering longer than usual.",
        "access": "The vent hatch is only accessible from the Supply Storage. That's restricted to Zephyr and maintenance.",
        "trust": "Everyone's got secrets on a night shift like this.",
    },
    "Marinette": {
        "suspicion": "One of the patients kept muttering about a 'draft' from the vents. Odd timing.",
        "vending": "I heard it ate someone's snack money, but I wasn't near the cafeteria.",
        "access": "I have no reason to know who has vent access. That's not my area.",
        "trust": "I try to think the best of everyone here.",
    },
    "Adrien": {
        "suspicion": "The generator's been fine, but I did hear something rattling in the vent system around 11:30.",
        "vending": "It's been eating coins all week. I didn't see anyone near it though.",
        "access": "Only people with maintenance clearance can touch the vents. That's like... Zephyr and maybe one or two others.",
        "trust": "Hard to say. Luca probably knows more — he's everywhere at night.",
    },
}

_ZEPHYR_ANSWERS = {
    "suspicion": {
        "truth": "Now that you mention it... I felt a strange draft near the vents last night. Probably nothing.",
        "lie": "Nope, nothing seemed off to me at all.",
    },
    "vending": {
        "truth": "Oh, I actually restocked it myself last night around 11:50 — comes with the job.",
        "lie": "No idea, I don't really deal with the cafeteria side of things.",
    },
    "access": {
        "truth": "Yeah, I have full vent access. Part of the Supply Coordinator role — gotta check air filters.",
        "lie": "No, I don't have vent access. That's a maintenance thing.",
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
    if question_key == "alibi":
        return PROFILES[character]["true_alibi"]
    return _INNOCENT_ANSWERS.get(character, {}).get(question_key, "Not much to say about that.")
