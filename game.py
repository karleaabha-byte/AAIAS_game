"""
game.py - Game state and rules engine for "Who Is the Mole?"
"""
import case
from ai_agent import MoleAI

ROOMS = ["Laboratory", "Storage", "Cafeteria"]
TOTAL_BUDGET = 9  # 3 room visits + 5 questions + 1 accusation


class GameState:
    def __init__(self, seed=None):
        self.mole_ai = MoleAI(seed)
        self.actions_used = 0
        self.suspicion = 10
        self.visited_rooms = {}      # room -> clue text shown
        self.room_decisions = {}     # room -> "sabotage" / "help" / "neutral"
        self.asked = {}              # character -> {"question": key, "answer": str, "lied": bool}
        self.log = []
        self.game_over = False
        self.result = None           # "win" / "lose" / None
        self.accused = None
        self.contradiction_flagged = False

    # ---------- helpers ----------
    @property
    def actions_remaining(self):
        return TOTAL_BUDGET - self.actions_used

    def _clamp_suspicion(self):
        self.suspicion = max(0, min(100, self.suspicion))

    def _log(self, text):
        self.log.append(text)

    def can_act(self):
        return not self.game_over and self.actions_remaining > 0

    # ---------- actions ----------
    def visit_room(self, room):
        if not self.can_act():
            return False, "No actions remaining."
        if room in self.visited_rooms:
            return False, f"You've already investigated the {room}."
        if room not in ROOMS:
            return False, "Unknown room."

        if room == "Laboratory":
            clue = case.get_lab_clue()
            decision = "neutral"
        else:
            decision = self.mole_ai.decide_room_action(self.suspicion, self.actions_remaining)
            if room == "Storage":
                clue = case.get_storage_clue(decision)
            else:
                clue = case.get_cafeteria_clue(decision)

            if decision == "sabotage":
                self.suspicion += self.mole_ai.rng.randint(8, 14)
                self._log(f"🕵️ Something feels *off* about the {room} — did someone tamper with it?")
            else:
                self.suspicion -= self.mole_ai.rng.randint(4, 8)
                self._log(f"🙂 The {room} seems undisturbed, almost helpfully so.")

        self._clamp_suspicion()
        self.room_decisions[room] = decision
        self.visited_rooms[room] = clue
        self.actions_used += 1
        self._log(f"🔎 Investigated the {room}.")
        return True, clue

    def ask_question(self, character, question_key):
        if not self.can_act():
            return False, "No actions remaining."
        if character in self.asked:
            return False, f"You've already questioned {character}."
        if character not in case.CHARACTERS:
            return False, "Unknown character."

        if character == case.MOLE:
            tell_truth = self.mole_ai.decide_truth_or_lie(self.suspicion)
            answer = case.get_answer(character, question_key, tell_truth)
            lied = not tell_truth

            if lied and question_key == "alibi":
                # Contradiction check: Raven says she was alone in the Lab all night.
                if "Raven" in self.asked and self.asked["Raven"]["question"] == "alibi":
                    self.suspicion += 25
                    self.contradiction_flagged = True
                    self._log(
                        "🚨 Wait — Raven swore she was ALONE in the Laboratory all night, but "
                        "Zephyr just claimed to have popped in to borrow a tool. That doesn't add up!"
                    )
                else:
                    self.suspicion += 6
            elif lied:
                self.suspicion += 5
            else:
                self.suspicion -= 3
        else:
            tell_truth = True
            answer = case.get_answer(character, question_key, True)
            lied = False

        self._clamp_suspicion()
        self.asked[character] = {"question": question_key, "answer": answer, "lied": lied}
        self.actions_used += 1
        self._log(f"💬 Questioned {character}.")
        return True, answer

    def make_accusation(self, character):
        if self.game_over:
            return False, "The case is already closed."
        if character not in case.CHARACTERS:
            return False, "Unknown character."

        self.accused = character
        self.actions_used = TOTAL_BUDGET  # accusation always consumes the final action
        self.game_over = True
        self.result = "win" if character == case.MOLE else "lose"
        self._log(f"⚖️ Final accusation: {character}.")
        return True, self.result

    def get_stats(self):
        stats = self.mole_ai.stats()
        stats.update(
            {
                "actions_used": self.actions_used,
                "suspicion": self.suspicion,
                "result": self.result,
                "accused": self.accused,
                "contradiction_flagged": self.contradiction_flagged,
            }
        )
        return stats
