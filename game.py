"""
game.py
Game state and rules engine for Zom-Mole Hunter
"""

import time
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

WORDLE_ANSWER = "VENTS"
WORDLE_MAX_ATTEMPTS = 6
WORDLE_TIME_LIMIT = 45


# ============================================================
# GAME STATE
# ============================================================

class GameState:

    def __init__(self, seed=None):

        # ----------------------------------------------------
        # AI
        # ----------------------------------------------------

        self.mole_ai = MoleAI(seed)

        # ----------------------------------------------------
        # EVIDENCE
        # ----------------------------------------------------

        self.evidence = EvidenceBoard()

        # ----------------------------------------------------
        # ACTION / GAME STATE
        # ----------------------------------------------------

        self.actions_used = 0

        self.suspicion = 10

        self.visited_rooms = {}

        self.room_decisions = {}

        self.asked = {}

        self.log = []

        self.game_over = False

        self.result = None

        self.accused = None

        # ----------------------------------------------------
        # CONTRADICTIONS
        # ----------------------------------------------------

        self.contradiction_flagged = False

        self.last_contradiction = None

        # ----------------------------------------------------
        # CAFETERIA PIN
        # ----------------------------------------------------

        self.pin_cracked = False

        self.pin_attempts = 0

        # ----------------------------------------------------
        # SECURITY CHALLENGE
        # ----------------------------------------------------

        self.security_challenge_active = False

        self.security_challenge_complete = False

        self.wordle_answer = WORDLE_ANSWER

        self.wordle_attempts = []

        self.wordle_max_attempts = WORDLE_MAX_ATTEMPTS

        self.wordle_time_limit = WORDLE_TIME_LIMIT

        self.wordle_started_at = None

        self.wordle_failed = False


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


    def _clamp_suspicion(self):

        self.suspicion = max(
            0,
            min(
                100,
                self.suspicion
            )
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

            self.evidence.add_clue(
                "lab_acrostic"
            )

            self.room_decisions[room] = "neutral"


        # ====================================================
        # STORAGE
        # ====================================================

        elif room == "Storage":

            # ------------------------------------------------
            # Zephyr decides whether to sabotage the riddle.
            # ------------------------------------------------

            sabotage = self.mole_ai.decide_riddle_sabotage(
                self.suspicion
            )

            if sabotage:

                clue = case.get_storage_clue(
                    "sabotage"
                )

                self.room_decisions[room] = "riddle_sabotage"

                self._log(
                    "⚠️ The Storage terminal appears "
                    "to have been tampered with."
                )

                self.suspicion += 3

            else:

                clue = case.get_storage_clue(
                    "help"
                )

                self.room_decisions[room] = "help"

                self._log(
                    "📦 The Storage terminal appears "
                    "undisturbed."
                )

            self.evidence.add_clue(
                "storage_riddle"
            )


        # ====================================================
        # CAFETERIA
        # ====================================================

        else:

            clue = case.get_cafeteria_clue()

            self.evidence.add_clue(
                "cafeteria_pin"
            )

            self.room_decisions[room] = "neutral"


        # ----------------------------------------------------
        # CLAMP SUSPICION
        # ----------------------------------------------------

        self._clamp_suspicion()


        # ----------------------------------------------------
        # SAVE INVESTIGATION
        # ----------------------------------------------------

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
    # PIN
    # ========================================================

    def attempt_pin(self, guess):

        if self.pin_cracked:

            return True

        if not self.can_act():

            return False

        # ----------------------------------------------------
        # EVERY ATTEMPT COSTS ONE ACTION
        # ----------------------------------------------------

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


        # ====================================================
        # CORRECT PIN
        # ====================================================

        if correct:

            self.pin_cracked = True

            self.evidence.set_pin_cracked()

            self._log(
                "🔓 PIN CRACKED. "
                "Restricted employee access unlocked."
            )


            # ------------------------------------------------
            # ZEPHYR GETS A CHANCE TO SABOTAGE INTERROGATION
            # ------------------------------------------------

            activate_challenge = (
                self.mole_ai.decide_extra_challenge(
                    self.suspicion,
                    self.actions_remaining
                )
            )


            if activate_challenge:

                self.security_challenge_active = True

                self.security_challenge_complete = False

                self.wordle_started_at = time.time()

                self._log(
                    "🚨 SECONDARY SECURITY LOCK ACTIVATED."
                )

            else:

                self.security_challenge_active = False

                self.security_challenge_complete = True

                self._log(
                    "🔓 INTERROGATION SYSTEM UNLOCKED."
                )

            return True


        # ====================================================
        # INCORRECT PIN
        # ====================================================

        self._log(
            f"🔐 Incorrect PIN attempt "
            f"#{self.pin_attempts}."
        )

        return False


    # ========================================================
    # WORDLE / SECURITY CHALLENGE
    # ========================================================

    def submit_wordle(self, guess):

        # ----------------------------------------------------
        # CHALLENGE ACTIVE?
        # ----------------------------------------------------

        if not self.security_challenge_active:

            if self.security_challenge_complete:

                return (
                    True,
                    "ALREADY_COMPLETE"
                )

            return (
                False,
                "No security challenge is active."
            )


        # ----------------------------------------------------
        # TIME CHECK
        # ----------------------------------------------------

        elapsed = (
            time.time()
            - self.wordle_started_at
        )

        if elapsed >= self.wordle_time_limit:

            self.security_challenge_active = False

            self.wordle_failed = True

            self._log(
                "⏰ SECURITY CHALLENGE FAILED: "
                "Time expired."
            )

            return (
                False,
                "TIME_EXPIRED"
            )


        # ----------------------------------------------------
        # NORMALIZE GUESS
        # ----------------------------------------------------

        guess = str(guess).strip().upper()


        # ----------------------------------------------------
        # LENGTH CHECK
        # ----------------------------------------------------

        if len(guess) != 5:

            return (
                False,
                "Enter a 5-letter word."
            )


        # ----------------------------------------------------
        # LETTER CHECK
        # ----------------------------------------------------

        if not guess.isalpha():

            return (
                False,
                "Letters only."
            )


        # ----------------------------------------------------
        # ATTEMPT LIMIT
        # ----------------------------------------------------

        if (
            len(self.wordle_attempts)
            >= self.wordle_max_attempts
        ):

            self.security_challenge_active = False

            self.wordle_failed = True

            self._log(
                "🔐 SECURITY CHALLENGE FAILED: "
                "Maximum attempts reached."
            )

            return (
                False,
                "ATTEMPTS_EXHAUSTED"
            )


        # ----------------------------------------------------
        # SAVE ATTEMPT
        # ----------------------------------------------------

        self.wordle_attempts.append(
            guess
        )


        answer = self.wordle_answer

        result = []


        # ----------------------------------------------------
        # WORDLE RESULT
        # ----------------------------------------------------

        for index, letter in enumerate(guess):

            if letter == answer[index]:

                result.append("🟩")

            elif letter in answer:

                result.append("🟨")

            else:

                result.append("⬛")


        # ====================================================
        # CORRECT
        # ====================================================

        if guess == answer:

            self.security_challenge_complete = True

            self.security_challenge_active = False

            self._log(
                "🔓 SECONDARY SECURITY LOCK DEFEATED."
            )

            return (
                True,
                {
                    "status": "CORRECT",
                    "result": result,
                    "attempts_remaining": (
                        self.wordle_max_attempts
                        - len(self.wordle_attempts)
                    )
                }
            )


        # ====================================================
        # OUT OF ATTEMPTS
        # ====================================================

        if (
            len(self.wordle_attempts)
            >= self.wordle_max_attempts
        ):

            self.security_challenge_active = False

            self.wordle_failed = True

            self._log(
                "🔐 SECURITY CHALLENGE FAILED."
            )

            return (
                False,
                {
                    "status": "FAILED",
                    "result": result,
                    "attempts_remaining": 0
                }
            )


        # ====================================================
        # INCORRECT BUT CONTINUE
        # ====================================================

        return (
            True,
            {
                "status": "CONTINUE",
                "result": result,
                "attempts_remaining": (
                    self.wordle_max_attempts
                    - len(self.wordle_attempts)
                )
            }
        )


    # ========================================================
    # TIME REMAINING FOR WORDLE
    # ========================================================

    def get_wordle_time_remaining(self):

        if not self.security_challenge_active:

            return 0

        if self.wordle_started_at is None:

            return self.wordle_time_limit

        elapsed = (
            time.time()
            - self.wordle_started_at
        )

        remaining = (
            self.wordle_time_limit
            - elapsed
        )

        return max(
            0,
            int(remaining)
        )


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
        # SECURITY CHALLENGE LOCK
        # ----------------------------------------------------

        if self.security_challenge_active:

            return (
                False,
                "🔐 Interrogation is locked. "
                "Complete the secondary security challenge."
            )


        # ----------------------------------------------------
        # FAILED SECURITY CHALLENGE
        # ----------------------------------------------------

        if self.wordle_failed:

            return (
                False,
                "🔐 Interrogation access was blocked "
                "by the security system."
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


        # ====================================================
        # MOLE AI DECIDES TRUTH / LIE
        # ====================================================

        if character == case.MOLE:

            tell_truth = (
                self.mole_ai.decide_truth_or_lie(
                    self.suspicion
                )
            )

            answer_data = case.get_question(
                character,
                question_key
            )

            answer = answer_data["answer"]

            # The AI's decision determines how the statement
            # is treated internally.

            lied = not tell_truth

        else:

            answer_data = case.get_question(
                character,
                question_key
            )

            answer = answer_data["answer"]

            lied = False


        # ----------------------------------------------------
        # SAVE STATEMENT
        # ----------------------------------------------------

        self.asked[character] = {

            "question": question_key,

            "answer": answer,

            "lied": lied
        }


        # ----------------------------------------------------
        # SAVE TO EVIDENCE BOARD
        # ----------------------------------------------------

        self.evidence.log_answer(
            character,
            question_key,
            answer,

            # EvidenceBoard stores whether statement
            # is true.
            not lied
        )


        # ====================================================
        # SUSPICION
        # ====================================================

        if character == case.MOLE:

            if lied:

                self.suspicion += 8

                self._log(
                    "⚠️ Zephyr's answer feels rehearsed."
                )

            else:

                self.suspicion -= 2

                self._log(
                    "🔎 Zephyr gave a surprisingly "
                    "straightforward answer."
                )

        else:

            self.suspicion -= 1


        self._clamp_suspicion()


        # ----------------------------------------------------
        # CONSUME ACTION
        # ----------------------------------------------------

        self.actions_used += 1


        # ----------------------------------------------------
        # LOG
        # ----------------------------------------------------

        self._log(
            f"💬 Questioned {character}."
        )


        # ====================================================
        # CONTRADICTION DETECTION
        # ====================================================

        try:

            new_contradictions = (
                self.evidence.detect_contradictions()
            )

        except AttributeError:

            new_contradictions = []


        for contradiction in new_contradictions:

            self.contradiction_flagged = True

            self.last_contradiction = (
                contradiction["detail"]
            )

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

        return {

            "actions_used":
                self.actions_used,

            "actions_remaining":
                self.actions_remaining,

            "suspicion":
                self.suspicion,

            "result":
                self.result,

            "accused":
                self.accused,

            "contradiction_flagged":
                self.contradiction_flagged,

            "guilt_scores":
                getattr(
                    self.evidence,
                    "guilt_scores",
                    {}
                ),

            "last_contradiction":
                self.last_contradiction,

            "pin_cracked":
                self.pin_cracked,

            "pin_attempts":
                self.pin_attempts,

            "security_challenge_active":
                self.security_challenge_active,

            "security_challenge_complete":
                self.security_challenge_complete,

            "wordle_attempts":
                self.wordle_attempts,

            "wordle_time_remaining":
                self.get_wordle_time_remaining(),

            "wordle_failed":
                self.wordle_failed,

            "mole_ai":
                self.mole_ai.stats()
        }
