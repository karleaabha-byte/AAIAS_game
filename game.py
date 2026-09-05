"""
game.py
Game state and rules engine for Zom-Mole Hunter
"""

import case

from evidence import EvidenceBoard


# ============================================================
# GAME CONSTANTS
# ============================================================

ROOMS = [
    "Laboratory",
    "Storage",
    "Cafeteria"
]

TOTAL_BUDGET = 12


# ============================================================
# GAME STATE
# ============================================================

class GameState:

    def __init__(self, seed=None):

        self.evidence = EvidenceBoard()

        self.actions_used = 0

        self.suspicion = 10

        self.visited_rooms = {}

        self.room_decisions = {}

        self.asked = {}

        self.log = []

        self.game_over = False

        self.result = None

        self.accused = None

        self.contradiction_flagged = False

        self.pin_cracked = False

        self.pin_attempts = 0

        self.last_contradiction = None


    # ========================================================
    # ACTIONS
    # ========================================================

    @property
    def actions_remaining(self):

        return TOTAL_BUDGET - self.actions_used


    def can_act(self):

        return (
            not self.game_over
            and self.actions_remaining > 0
        )


    def _log(self, text):

        self.log.append(text)


    # ========================================================
    # ROOM INVESTIGATION
    # ========================================================

    def visit_room(self, room):

        if not self.can_act():
            return False, "No actions remaining."

        if room in self.visited_rooms:
            return False, f"You've already investigated the {room}."

        if room not in ROOMS:
            return False, "Unknown room."

        # ----------------------------------------------------
        # LABORATORY
        # ----------------------------------------------------

        if room == "Laboratory":

            clue = case.get_lab_clue()

            self.evidence.add_clue(
                "lab_acrostic"
            )

            self.room_decisions[room] = "neutral"


        # ----------------------------------------------------
        # STORAGE
        # ----------------------------------------------------

        elif room == "Storage":

            clue = case.get_storage_clue()

            self.evidence.add_clue(
                "storage_riddle"
            )

            self.room_decisions[room] = "neutral"


        # ----------------------------------------------------
        # CAFETERIA
        # ----------------------------------------------------

        else:

            clue = case.get_cafeteria_clue()

            self.evidence.add_clue(
                "cafeteria_pin"
            )

            self.room_decisions[room] = "neutral"


        # ----------------------------------------------------
        # SAVE INVESTIGATION
        # ----------------------------------------------------

        self.visited_rooms[room] = clue

        self.actions_used += 1

        self._log(
            f"🔎 Investigated the {room}."
        )

        return True, clue


    # ========================================================
    # PIN
    # ========================================================

    def attempt_pin(self, guess):

        if not self.can_act():
            return False

        # Every attempt costs one action
        self.actions_used += 1

        self.pin_attempts += 1

        digits = "".join(
            character
            for character in str(guess)
            if character.isdigit()
        )

        correct = (
            digits == case.CORRECT_PIN
        )

        # ----------------------------------------------------
        # CORRECT
        # ----------------------------------------------------

        if correct:

            self.pin_cracked = True

            self.evidence.set_pin_cracked()

            self._log(
                "🔓 PIN CRACKED. "
                "Restricted employee access unlocked."
            )

            return True


        # ----------------------------------------------------
        # INCORRECT
        # ----------------------------------------------------

        self._log(
            f"🔐 Incorrect PIN attempt "
            f"#{self.pin_attempts}."
        )

        return False


    # ========================================================
    # INTERROGATION
    # ========================================================

    def ask_question(
        self,
        character,
        question_key
    ):

        # ----------------------------------------------------
        # PIN LOCK
        # ----------------------------------------------------

        if not self.pin_cracked:

            return (
                False,
                "🔒 The interrogation system is locked. "
                "Crack the Cafeteria PIN first."
            )


        # ----------------------------------------------------
        # ACTION CHECK
        # ----------------------------------------------------

        if not self.can_act():

            return (
                False,
                "No actions remaining."
            )


        # ----------------------------------------------------
        # ONE QUESTION PER SUSPECT
        # ----------------------------------------------------

        if character in self.asked:

            return (
                False,
                f"You've already questioned {character}."
            )


        # ----------------------------------------------------
        # VALID CHARACTER
        # ----------------------------------------------------

        if character not in case.CHARACTERS:

            return (
                False,
                "Unknown character."
            )


        # ----------------------------------------------------
        # VALID QUESTION
        # ----------------------------------------------------

        if question_key not in case.QUESTION_BANK:

            return (
                False,
                "Unknown question."
            )


        # ----------------------------------------------------
        # GET ANSWER
        # ----------------------------------------------------

        answer_data = case.get_question(
            character,
            question_key
        )

        answer = answer_data["answer"]

        actual_truth = answer_data.get(
            "truth",
            True
        )

        lied = not actual_truth


        # ----------------------------------------------------
        # SAVE STATEMENT
        # ----------------------------------------------------

        self.asked[character] = {

            "question": question_key,

            "answer": answer,

            "lied": lied
        }


        self.evidence.log_answer(
            character,
            question_key,
            answer,

            # EvidenceBoard expects whether
            # the statement was actually true.
            actual_truth
        )


        # ----------------------------------------------------
        # SMALL SUSPICION EFFECT
        # ----------------------------------------------------

        if character == case.MOLE:

            if lied:
                self.suspicion += 8
            else:
                self.suspicion -= 2

        else:

            self.suspicion -= 1


        self.suspicion = max(
            0,
            min(
                100,
                self.suspicion
            )
        )


        # ----------------------------------------------------
        # CONSUME ACTION
        # ----------------------------------------------------

        self.actions_used += 1


        self._log(
            f"💬 Questioned {character}."
        )


        return (
            True,
            answer
        )


    # ========================================================
    # FINAL ACCUSATION
    # ========================================================

    def make_accusation(
        self,
        character
    ):

        if self.game_over:

            return (
                False,
                "The case is already closed."
            )


        if character not in case.CHARACTERS:

            return (
                False,
                "Unknown character."
            )


        self.accused = character

        self.actions_used = TOTAL_BUDGET

        self.game_over = True


        if character == case.MOLE:

            self.result = "win"

        else:

            self.result = "lose"


        self._log(
            f"⚖️ Final accusation: "
            f"{character}."
        )


        return (
            True,
            self.result
        )


    # ========================================================
    # STATS
    # ========================================================

    def get_stats(self):

        return {

            "actions_used":
                self.actions_used,

            "suspicion":
                self.suspicion,

            "result":
                self.result,

            "accused":
                self.accused,

            "contradiction_flagged":
                self.contradiction_flagged,

            "guilt_scores":
                self.evidence.guilt_scores,

            "last_contradiction":
                self.last_contradiction,

            "pin_cracked":
                self.pin_cracked,

            "pin_attempts":
                self.pin_attempts
        }
