"""
game.py - Game state and rules engine for "Zom-Mole Hunter"
"""

import case

from ai_agent import MoleAI
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

        self.mole_ai = MoleAI(seed)

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

        return (
            TOTAL_BUDGET
            - self.actions_used
        )


    def _clamp_suspicion(self):

        self.suspicion = max(
            0,
            min(
                100,
                self.suspicion
            )
        )


    def _log(self, text):

        self.log.append(text)


    def can_act(self):

        return (
            not self.game_over
            and self.actions_remaining > 0
        )


    # ========================================================
    # ROOM INVESTIGATION
    # ========================================================

    def visit_room(self, room):

        if not self.can_act():

            return (
                False,
                "No actions remaining."
            )


        if room in self.visited_rooms:

            return (
                False,
                f"You've already investigated the {room}."
            )


        if room not in ROOMS:

            return (
                False,
                "Unknown room."
            )


        # ====================================================
        # LABORATORY
        # ====================================================

        if room == "Laboratory":

            clue = case.get_lab_clue()

            decision = "neutral"

            self.evidence.add_clue(
                "lab_acrostic"
            )


        # ====================================================
        # STORAGE / CAFETERIA
        # ====================================================

        else:

            decision = (
                self.mole_ai.decide_room_action(
                    self.suspicion,
                    self.actions_remaining
                )
            )


            if room == "Storage":

                clue = case.get_storage_clue(
                    decision
                )

                self.evidence.add_clue(
                    "storage_riddle"
                )


            else:

                clue = case.get_cafeteria_clue(
                    decision
                )

                self.evidence.add_clue(
                    "cafeteria_pin"
                )


            # =================================================
            # AI ROOM BEHAVIOUR
            # =================================================

            if decision == "sabotage":

                self.suspicion += (
                    self.mole_ai.rng.randint(
                        8,
                        14
                    )
                )

                self._log(
                    f"🕵️ Something feels *off* "
                    f"about the {room} — "
                    f"did someone tamper with it?"
                )

            else:

                self.suspicion -= (
                    self.mole_ai.rng.randint(
                        4,
                        8
                    )
                )

                self._log(
                    f"🙂 The {room} seems "
                    f"undisturbed."
                )


        self._clamp_suspicion()


        self.room_decisions[room] = decision

        self.visited_rooms[room] = clue

        self.actions_used += 1


        self._log(
            f"🔎 Investigated the {room}."
        )


        return (
            True,
            clue
        )


    # ========================================================
    # PIN ATTEMPT
    # ========================================================

    def attempt_pin(self, guess):

        # Every attempt consumes one action.
        if not self.can_act():

            return False


        # ====================================================
        # CONSUME ACTION FIRST
        # ====================================================

        self.actions_used += 1

        self.pin_attempts += 1


        # ====================================================
        # CLEAN USER INPUT
        # ====================================================

        digits = "".join(
            ch
            for ch in str(guess)
            if ch.isdigit()
        )


        # ====================================================
        # CHECK PIN
        # ====================================================

        correct = (
            digits == case.CORRECT_PIN
        )


        # ====================================================
        # CORRECT
        # ====================================================

        if correct:

            if not self.pin_cracked:

                self.pin_cracked = True

                self.evidence.set_pin_cracked()

                self._log(
                    "🔓 PIN CRACKED. "
                    "Restricted employee access unlocked."
                )

            return True


        # ====================================================
        # INCORRECT
        # ====================================================

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

        # ====================================================
        # PIN LOCK
        # ====================================================

        if not self.pin_cracked:

            return (
                False,
                "🔒 The interrogation system is locked. "
                "Crack the Cafeteria PIN first."
            )


        # ====================================================
        # NORMAL ACTION CHECK
        # ====================================================

        if not self.can_act():

            return (
                False,
                "No actions remaining."
            )


        if character in self.asked:

            return (
                False,
                f"You've already questioned {character}."
            )


        if character not in case.CHARACTERS:

            return (
                False,
                "Unknown character."
            )


        # ====================================================
        # MOLE
        # ====================================================

        if character == case.MOLE:

            tell_truth = (
                self.mole_ai.decide_truth_or_lie(
                    self.suspicion
                )
            )

            answer = case.get_answer(
                character,
                question_key,
                tell_truth
            )

            lied = not tell_truth


            # =================================================
            # ALIBI CONTRADICTION
            # =================================================

            if (
                lied
                and question_key == "alibi"
            ):

                if (
                    "Raven" in self.asked
                    and self.asked["Raven"]["question"]
                    == "alibi"
                ):

                    self.suspicion += 25

                    self.contradiction_flagged = True

                    self.last_contradiction = (
                        "Raven claimed to be alone "
                        "in the Laboratory, but Zephyr "
                        "claims to have visited."
                    )

                    self._log(
                        "🚨 CONTRADICTION: "
                        "Raven swore she was ALONE "
                        "in the Laboratory all night, "
                        "but Zephyr just claimed to "
                        "have popped in."
                    )

                else:

                    self.suspicion += 6


            elif lied:

                self.suspicion += 5


            else:

                self.suspicion -= 3


        # ====================================================
        # OTHER CHARACTERS
        # ====================================================

        else:

            tell_truth = True

            answer = case.get_answer(
                character,
                question_key,
                True
            )

            lied = False


        # ====================================================
        # SAVE
        # ====================================================

        self._clamp_suspicion()


        self.asked[character] = {

            "question": question_key,

            "answer": answer,

            "lied": lied
        }


        self.evidence.log_answer(
            character,
            question_key,
            answer,
            lied
        )


        self.actions_used += 1


        self._log(
            f"💬 Questioned {character}."
        )


        # ====================================================
        # DETECT CONTRADICTIONS
        # ====================================================

        new_contradictions = (
            self.evidence.detect_contradictions()
        )


        for contradiction in new_contradictions:

            self._log(
                f"🚨 {contradiction['detail']}"
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

        stats = self.mole_ai.stats()


        stats.update(
            {
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
                    self.pin_attempts,
            }
        )


        return stats
