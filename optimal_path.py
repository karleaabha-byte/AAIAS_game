"""
optimal_path.py - Reference solution, hint system, and performance scoring.

Also doubles as a lightweight design-time proof that the case stays solvable
even under worst-case sabotage (see verify_solvability()).
"""
import case

# A minimal sequence of actions that solves the case regardless of how the
# mole plays Storage/Cafeteria, since every clue leaves a usable fragment
# behind even when sabotaged.
OPTIMAL_SEQUENCE = [
    ("visit", "Laboratory", None,
     "Reveals the acrostic hint WINDY — this room isn't mole-controllable, so it always shows in full."),
    ("visit", "Cafeteria", None,
     "Even if sabotaged, the job title 'Supply Coordinator' survives."),
    ("visit", "Storage", None,
     "Even if sabotaged, the riddle still points to 'wind'."),
    ("ask", "Raven", "alibi",
     "Establishes that Raven was ALONE in the Laboratory all night."),
    ("ask", "Zephyr", "alibi",
     "Compare this against Raven's answer for a possible contradiction."),
    ("accuse", "Zephyr", None,
     "All three room clues (a wind-themed hint, a wind riddle, and the Supply Coordinator "
     "job title) plus a possible alibi contradiction all point at Zephyr."),
]

MIN_ACTIONS_TO_SOLVE = 6  # length of OPTIMAL_SEQUENCE


def get_hint(game_state):
    """Return the next recommended action given what's already happened."""
    for kind, target, extra, reason in OPTIMAL_SEQUENCE:
        if kind == "visit":
            if target not in game_state.visited_rooms:
                return f"🔎 Try investigating the **{target}**. {reason}"
        elif kind == "ask":
            if target not in game_state.asked:
                return f"💬 Try questioning **{target}**. {reason}"
        elif kind == "accuse":
            return f"⚖️ You likely have enough to accuse **{target}**. {reason}"
    return "You've covered the optimal path already — trust your instincts!"


def evaluate_performance(stats):
    """Grade the player's run once the game is over."""
    if stats["result"] != "win":
        return {
            "grade": "F",
            "message": (
                "The mole slipped away undetected. Every clue still had a thread pointing at "
                "Zephyr — the wind-themed acrostic, the 'Supply Coordinator' job title, and the "
                "riddle's answer. Next time, follow every thread!"
            ),
        }

    used = stats["actions_used"]
    if used <= MIN_ACTIONS_TO_SOLVE:
        grade, message = "S", "Flawless deduction — you solved it in the minimum number of actions!"
    elif used <= MIN_ACTIONS_TO_SOLVE + 1:
        grade, message = "A", "Excellent work — you caught the mole with actions to spare."
    elif used <= MIN_ACTIONS_TO_SOLVE + 2:
        grade, message = "B", "Solid detective work — a bit of extra legwork, but you got there."
    else:
        grade, message = "C", "You caught the mole right at the wire — cutting it close!"

    return {"grade": grade, "message": message}


def verify_solvability():
    """
    Dev-time sanity check: confirm that even the sabotaged versions of the
    Storage and Cafeteria clues still contain a recognizable fragment of the
    giveaway information. Run directly: `python optimal_path.py`.
    """
    lab = case.get_lab_clue()
    storage_sabotaged = case.get_storage_clue("sabotage")
    cafe_sabotaged = case.get_cafeteria_clue("sabotage")

    assert all(letter in lab for letter in "WINDY"), \
        "Laboratory acrostic hint got broken."
    assert "leaf" in storage_sabotaged and "sails" in storage_sabotaged, \
        "Storage riddle sabotage removed too much information."
    assert "Supply Coor" in cafe_sabotaged, \
        "Cafeteria sabotage removed the job-title fragment."

    print("✅ Case remains solvable under worst-case sabotage.")


if __name__ == "__main__":
    verify_solvability()
