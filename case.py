"""
case.py - Static case data for "Who Is the Mole?"

Clue chain design:
- Laboratory (always full, not sabotage-able): an acrostic spells "FOUR" -> a digit.
- Storage (sabotage-able): a riddle whose answer is "BREEZE" (6 letters) -> a digit.
- Cafeteria (sabotage-able): the vending PIN's first two digits are exactly the
  digits from Lab (4) and Storage (6). The job title never gets redacted, so
  there's always a fallback clue even if the PIN math isn't cracked.
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
        "flavor": "Rows of cracked beakers under a flickering light. A note is pinned to the corkboard, its wording oddly deliberate.",
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

_LAB_NOTE = (
    "**F**our vents line the ceiling, and every one of them shows fresh scuff marks.\n\n"
    "**O**nly staff badges can open the vent hatch — the maintenance chart confirms it.\n\n"
    "**U**nderneath the middle vent, damp footprints trail off toward the hallway.\n\n"
    "**R**ecords show someone accessed the vent controls well after midnight.\n\n"
    "*(Someone's circled the first letter of each line. Read top to bottom... could it be a number?)*"
)

_RIDDLE_BASE = (
    "*I cannot be seen, but I shake every leaf.*\n\n"
    "*I fill the sails of ships, yet I weigh nothing at all.*\n\n"
    "*Sailors bless me on a calm day, and curse me when I turn into a storm.*\n\n"
    "*What six-letter word am I?*\n\n"
    "*(Hint scratched at the bottom: count the letters in your answer — you'll need that number.)*"
)

_RIDDLE_SABOTAGE = (
    "Someone's scratched extra lines over the original riddle, half-covering it:\n\n"
    "*I cannot be seen, but I shake every leaf... (the next line is scratched out)*\n\n"
    "*I fill the sails of ships, yet I weigh nothing at all.*\n\n"
    "*I can also 'travel' through a crowd as a rumor — so maybe I'm just noise?*\n\n"
    "*Sailors bless me on a calm day, and curse me when I turn into a storm.*\n\n"
    "*What six-letter word am I?*\n\n"
    "*(Hint scratched at the bottom, partly smudged: cou_t the lett___ in your answer.)*"
)

_RIDDLE_HELP = (
    _RIDDLE_BASE
    + "\n\n*Scrawled underneath, in different handwriting:* \"Hint: it's something you'd feel standing on a beach.\""
)

_CAFE_BASE = (
    "**Restocking Log — Vending Machine #3**\n\n"
    "Restocked by: *Supply Coordinator*\n\n"
    "Employee PIN: **_ _ 1 9**\n\n"
    "*(First two digits smudged by a spilled drink — last two are legible.)*"
)

_CAFE_SABOTAGE = (
    "**Restocking Log — Vending Machine #3** *(coffee-stained)*\n\n"
    "Restocked by: *Supply Coordinator*\n\n"
    "Employee PIN: **_ _ _ 9**\n\n"
    "*(Only the very last digit survived the spill.)*"
)

_CAFE_HELP = (
    "**Restocking Log — Vending Machine #3**\n\n"
    "Restocked by: *Supply Coordinator*\n\n"
    "Employee PIN: **4 6 1 9**\n\n"
    "*(Someone left the full log untouched, oddly considerate.)*"
)


def get_lab_clue():
    return _LAB_NOTE


def get_storage_clue(decision):
    if decision == "sabotage":
        return _RIDDLE_SABOTAGE
    if decision == "help":
        return _RIDDLE_HELP
    return _RIDDLE_BASE


def get_cafeteria_clue(decision):
    if decision == "sabotage":
        return _CAFE_SABOTAGE
    if decision == "help":
        return _CAFE_HELP
    return _CAFE_BASE


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
