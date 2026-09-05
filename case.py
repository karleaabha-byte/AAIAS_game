"""
case.py
Case data for "Who Is The Mole?"
"""

# ============================================================
# CASE BASICS
# ============================================================

CHARACTERS = [
    "Raven",
    "Zephyr",
    "Luca",
    "Marinette",
    "Adrien"
]

MOLE = "Zephyr"

ROOMS = [
    "Laboratory",
    "Storage",
    "Cafeteria"
]

LAB_NUMBER = 4
STORAGE_ANSWER = "BREEZE"
STORAGE_NUMBER = len(STORAGE_ANSWER)

# Final PIN = 4619
CORRECT_PIN = f"{LAB_NUMBER}{STORAGE_NUMBER}19"


# ============================================================
# CASE INTRO
# ============================================================

CASE_INTRO = """
## THE NIGHT SHIFT INCIDENT

**12:18 AM.**

The research facility should have been asleep.

Instead, the emergency lights are flashing, the laboratory alarm is screaming,
and someone has managed to make an entire cabinet of experimental materials
disappear without setting off a single ordinary security alarm.

At first, it looked like an equipment failure.

Then security found the broken vial.

Then they found the ventilation panel.

Then someone noticed that three minutes of camera footage had vanished.

And finally, they discovered something much worse:

**someone inside the facility knew exactly where the blind spots were.**

Five people were still inside the building that night.

One of them is lying.

Possibly more than one.

Your job is not simply to find someone who lied.

Your job is to figure out **which lie matters.**
"""


# ============================================================
# BACKGROUND
# ============================================================

BACKGROUND = {
    "THE INCIDENT": {
        "entries": [
            (
                "00:10",
                "The emergency alarm screamed through the facility. "
                "A centrifuge in the Laboratory had stopped mid-cycle."
            ),
            (
                "00:12",
                "Security found Raven inside the Laboratory. "
                "A shattered glass vial was lying beside her workstation."
            ),
            (
                "00:14",
                "Six experimental filter cartridges were missing "
                "from the Storage inventory."
            ),
            (
                "00:17",
                "The Storage ventilation panel was discovered closed, "
                "despite the system reporting that it had been opened earlier."
            ),
            (
                "00:18",
                "Three minutes of corridor camera footage were missing."
            ),
        ]
    },

    "THE STRANGE PART": {
        "entries": [
            (
                "11:45",
                "Raven says she began working alone in the Laboratory."
            ),
            (
                "11:49",
                "The corridor camera stopped recording."
            ),
            (
                "11:50",
                "The Storage ventilation panel registered a "
                "maintenance override."
            ),
            (
                "11:50",
                "The cafeteria vending machine began an unscheduled "
                "restocking cycle."
            ),
            (
                "11:52",
                "The laboratory centrifuge registered an unexpected "
                "manual interruption."
            ),
            (
                "12:03",
                "The ventilation panel was closed again."
            ),
        ]
    },

    "WHO COULD OPEN THE VENT?": {
        "entries": [
            (
                "AUTHORIZED",
                "Only the Supply Coordinator and Maintenance Chief "
                "are authorized to use the Storage ventilation override."
            ),
            (
                "MAINTENANCE",
                "The Maintenance Chief was off-site that night."
            ),
            (
                "SUPPLY",
                "The Supply Coordinator was scheduled for the entire "
                "night shift."
            ),
            (
                "IMPORTANT",
                "The system does not identify which authorized employee "
                "actually used the override."
            ),
        ]
    },

    "THE PEOPLE": {
        "entries": [
            (
                "RAVEN",
                "Head Chemist. She was responsible for the Laboratory "
                "and was apparently the last person seen near the broken vial."
            ),
            (
                "ZEPHYR",
                "Supply Coordinator. Responsible for Storage inventory, "
                "deliveries and equipment supplies."
            ),
            (
                "LUCA",
                "Security Officer. Responsible for corridor patrols "
                "and camera monitoring."
            ),
            (
                "MARINETTE",
                "Medic. Responsible for the Medical Bay and night-shift "
                "first aid."
            ),
            (
                "ADRIEN",
                "Engineer. Responsible for the Generator Room "
                "and facility power systems."
            ),
        ]
    },

    "THINGS WORTH REMEMBERING": {
        "entries": [
            (
                "1",
                "The camera outage happened at almost exactly the same "
                "time as the ventilation override."
            ),
            (
                "2",
                "The person who used the ventilation override did not "
                "need to physically enter the Laboratory."
            ),
            (
                "3",
                "The missing cartridges came from Storage."
            ),
            (
                "4",
                "The vending machine restocking happened during the "
                "three-minute camera blackout."
            ),
            (
                "5",
                "Not every suspicious statement is necessarily evidence "
                "of sabotage."
            ),
        ]
    }
}


# ============================================================
# SUSPECT PROFILES
# ============================================================

PROFILES = {
    "Raven": {
        "role": "Head Chemist",
        "location": "Laboratory",
        "description": (
            "Brilliant, impatient and visibly annoyed that anyone "
            "would question her work."
        ),
        "personality": "Defensive but confident."
    },

    "Zephyr": {
        "role": "Supply Coordinator",
        "location": "Storage",
        "description": (
            "Quiet, organized and almost painfully calm. "
            "He knows where everything in the facility is kept."
        ),
        "personality": "Helpful, controlled and evasive."
    },

    "Luca": {
        "role": "Security Officer",
        "location": "Corridor Patrol",
        "description": (
            "Takes security seriously, but seems embarrassed "
            "that three minutes of camera footage disappeared."
        ),
        "personality": "Professional with something to hide."
    },

    "Marinette": {
        "role": "Medic",
        "location": "Medical Bay",
        "description": (
            "Friendly and observant. She notices more than "
            "she initially admits."
        ),
        "personality": "Kind but secretive."
    },

    "Adrien": {
        "role": "Engineer",
        "location": "Generator Room",
        "description": (
            "Usually relaxed, but became unusually nervous "
            "when the power briefly dipped."
        ),
        "personality": "Casual and slightly nervous."
    }
}


# ============================================================
# QUESTIONS
# ============================================================

QUESTION_BANK = {
    "alibi": "Where were you between 11:45 PM and 12:10 AM?",

    "observation": "Did you see or hear anything unusual?",

    "timeline": "Walk me through what you were doing around 11:50 PM.",

    "vent": "Did you know anything about the Storage ventilation panel?",

    "vending": "Were you anywhere near the cafeteria vending machine?",

    "camera": "What do you know about the three-minute camera outage?",

    "inventory": "What do you know about the missing filter cartridges?",

    "lab": "Did you enter or approach the Laboratory that night?"
}


# ============================================================
# INTERROGATION ANSWERS
# ============================================================

ANSWERS = {

    # ========================================================
    # RAVEN
    # ========================================================

    "Raven": {

        "alibi": {
            "answer": (
                "I was in the Laboratory. I started around 11:45 "
                "and stayed there. I wasn't exactly socializing."
            ),
            "truth": True
        },

        "observation": {
            "answer": (
                "I heard the vending cart outside around 11:50. "
                "Then everything went strangely quiet for a few minutes."
            ),
            "truth": True
        },

        "timeline": {
            "answer": (
                "Around 11:50 I was running the centrifuge. "
                "At 11:52 it suddenly stopped."
            ),
            "truth": True
        },

        "lab": {
            "answer": (
                "Obviously I was in the Laboratory. "
                "That's where I work."
            ),
            "truth": True
        },

        "vent": {
            "answer": (
                "No. I don't touch the ventilation system. "
                "That's not my department."
            ),
            "truth": True
        },

        "camera": {
            "answer": (
                "I noticed the lights flicker, but I didn't know "
                "the cameras had gone down."
            ),
            "truth": True
        },

        "inventory": {
            "answer": (
                "I don't handle Storage inventory. "
                "Ask Zephyr."
            ),
            "truth": True
        },

        "vending": {
            "answer": (
                "I did leave my desk for maybe thirty seconds "
                "to grab coffee earlier. But that was before the alarm."
            ),
            "truth": False
        }
    },


    # ========================================================
    # ZEPHYR
    # ========================================================

    "Zephyr": {

        "alibi": {
            "answer": (
                "Storage. Inventory count. I was there all night. "
                "Didn't leave once."
            ),
            "truth": False
        },

        "observation": {
            "answer": (
                "Nothing unusual. Storage was boring, as usual. "
                "Boxes, shelves, inventory sheets."
            ),
            "truth": False
        },

        "timeline": {
            "answer": (
                "Around 11:50? I was checking the filter cartridges "
                "in Storage. I remember because the vending machine "
                "restocking was happening at the same time."
            ),
            "truth": False
        },

        "vent": {
            "answer": (
                "No. I don't have access to the ventilation override. "
                "That's Maintenance."
            ),
            "truth": False
        },

        "vending": {
            "answer": (
                "I wasn't near the vending machine. "
                "I was in Storage doing inventory."
            ),
            "truth": False
        },

        "camera": {
            "answer": (
                "I didn't even know the cameras went out."
            ),
            "truth": True
        },

        "inventory": {
            "answer": (
                "Six cartridges? That doesn't sound right. "
                "I counted everything before midnight."
            ),
            "truth": False
        },

        "lab": {
            "answer": (
                "I never entered the Laboratory."
            ),
            "truth": False
        }
    },


    # ========================================================
    # LUCA
    # ========================================================

    "Luca": {

        "alibi": {
            "answer": (
                "Corridor patrol. Mostly near the west entrance. "
                "I checked the cameras every few minutes."
            ),
            "truth": True
        },

        "observation": {
            "answer": (
                "I saw someone pushing a small cart toward the "
                "cafeteria around 11:50. Couldn't see the face."
            ),
            "truth": True
        },

        "timeline": {
            "answer": (
                "At 11:49 the corridor camera went dark. "
                "I went to check the system."
            ),
            "truth": True
        },

        "camera": {
            "answer": (
                "The outage looked like a routine diagnostic at first. "
                "Then I realized someone had manually overridden the system."
            ),
            "truth": True
        },

        "vent": {
            "answer": (
                "I didn't touch the ventilation controls."
            ),
            "truth": True
        },

        "vending": {
            "answer": (
                "I didn't use the vending machine. "
                "I was on patrol."
            ),
            "truth": True
        },

        "inventory": {
            "answer": (
                "I know six cartridges disappeared. "
                "Security was notified after the alarm."
            ),
            "truth": True
        },

        "lab": {
            "answer": (
                "I didn't enter the Laboratory."
            ),
            "truth": True
        }
    },


    # ========================================================
    # MARINETTE
    # ========================================================

    "Marinette": {

        "alibi": {
            "answer": (
                "Medical Bay. I was there most of the night."
            ),
            "truth": True
        },

        "observation": {
            "answer": (
                "Someone came into the Medical Bay shortly before "
                "midnight with a tiny cut on their hand."
            ),
            "truth": True
        },

        "timeline": {
            "answer": (
                "Around 11:50 I was preparing the emergency kit."
            ),
            "truth": True
        },

        "vent": {
            "answer": (
                "No idea. I don't have clearance for that system."
            ),
            "truth": True
        },

        "vending": {
            "answer": (
                "I heard the vending machine being restocked, "
                "but I didn't go there."
            ),
            "truth": True
        },

        "camera": {
            "answer": (
                "I only noticed the hallway looked darker than usual."
            ),
            "truth": True
        },

        "inventory": {
            "answer": (
                "I heard that something was missing, "
                "but I don't know how much."
            ),
            "truth": True
        },

        "lab": {
            "answer": (
                "I never went into the Laboratory."
            ),
            "truth": True
        }
    },


    # ========================================================
    # ADRIEN
    # ========================================================

    "Adrien": {

        "alibi": {
            "answer": (
                "Generator Room. The power dipped around 11:49, "
                "so I stayed there fixing it."
            ),
            "truth": True
        },

        "observation": {
            "answer": (
                "The power dipped for a few seconds. "
                "Nothing major."
            ),
            "truth": True
        },

        "timeline": {
            "answer": (
                "11:49 power dip. I checked the generator. "
                "By about 11:53 everything was stable."
            ),
            "truth": True
        },

        "vent": {
            "answer": (
                "I know the vent system exists, but I don't "
                "have authorization to override it."
            ),
            "truth": True
        },

        "vending": {
            "answer": (
                "I grabbed a drink earlier, but not during "
                "the restocking cycle."
            ),
            "truth": True
        },

        "camera": {
            "answer": (
                "The camera outage happened during the power dip, "
                "but I don't think the generator caused it."
            ),
            "truth": True
        },

        "inventory": {
            "answer": (
                "Six filter cartridges went missing. "
                "That's what I heard."
            ),
            "truth": True
        },

        "lab": {
            "answer": (
                "I passed the Laboratory earlier, but I didn't go inside."
            ),
            "truth": True
        }
    }
}


# ============================================================
# ROOM CLUES
# ============================================================

# ------------------------------------------------------------
# LABORATORY
# ------------------------------------------------------------
# IMPORTANT:
# The first letters spell FOUR, but they are deliberately
# NOT highlighted in the UI.
#
# Player has to notice the acrostic themselves.
# ------------------------------------------------------------

LAB_CLUE = {
    "title": "THE LABORATORY NOTE",
    "lines": [
        "Filter pressure was stable before midnight.",
        "One centrifuge cycle was interrupted manually.",
        "Unused cartridges were stored elsewhere.",
        "Raven's workstation was still active."
    ]
}

# ============================================================
# STORAGE
# ============================================================

STORAGE_CLUE = {
    "title": "THE SCRATCHED INVENTORY BOARD",

    "lines": [
        {"text": "Boxes counted: 18", "struck": False},
        {"text": "Filter cartridges: 24", "struck": True},
        {"text": "Filter cartridges: 18", "struck": False},
        {"text": "Ventilation override — 11:50 PM", "struck": False},
        {"text": "Maintenance Chief — OFF SHIFT", "struck": False},
        {"text": "Supply Coordinator — ON SHIFT", "struck": False},
    ],

    "riddle": [
        "I cannot be seen, but I shake every leaf.",
        "I fill the sails of ships, yet I weigh nothing at all.",
        "I can carry a whisper farther than the person who spoke it.",
        "Sailors welcome me when I am gentle, but fear what I become when I grow wild.",
        "What am I?"
    ]
}


# ============================================================
# CAFETERIA
# ============================================================

CAFETERIA_CLUE = {
    "title": "RESTOCKING LOG — MACHINE #3",

    "job": "SUPPLY RESTOCK",

    "pin_digits": [
        "?",
        "?",
        "1",
        "9"
    ],

    "redacted": [
        True,
        True,
        False,
        False
    ],

    "note": (
        "Restocking began at 11:50 PM — exactly when the "
        "corridor cameras went dark."
    )
}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_lab_clue():
    """
    Return the Laboratory clue.
    """
    return LAB_CLUE


def get_storage_clue(decision=None):
    """
    Return the Storage clue.

    The decision parameter is accepted because game.py passes
    the Mole's room decision to this function.

    The clue itself does not change based on that decision.
    """
    return STORAGE_CLUE


def get_cafeteria_clue(decision=None):
    """
    Return the Cafeteria clue.

    The decision parameter is accepted because game.py passes
    the Mole's room decision to this function.

    The clue itself does not change based on that decision.
    """
    return CAFETERIA_CLUE


def get_question(character, question_key):
    """
    Return the stored answer information for a character.
    """
    return ANSWERS[character][question_key]


def get_profile(character):
    """
    Return the profile for a character.
    """
    return PROFILES[character]

def get_answer(character, question_key, tell_truth=True):
    """
    Return the interrogation answer for a character.

    The tell_truth parameter is accepted because game.py
    uses it when handling the Mole's responses.
    """
    return ANSWERS[character][question_key]["answer"]
