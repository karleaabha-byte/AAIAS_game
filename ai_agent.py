"""
ai_agent.py - Adversarial Mole AI

Zephyr can:
1. Lie or tell the truth during interrogation.
2. Sabotage Storage/Cafeteria investigations.
3. Make the Storage riddle harder.
4. Add an optional timed security challenge before interrogation.
"""

import random


class MoleAI:

    def __init__(self, seed=None):

        self.rng = random.Random(seed)

        self.sabotage_count = 0
        self.help_count = 0

        self.lie_count = 0
        self.truth_count = 0

        self.riddle_sabotage_count = 0
        self.challenge_sabotage_count = 0

        self.decisions_log = []

    # ============================================================
    # INTERROGATION
    # ============================================================

    def decide_truth_or_lie(self, suspicion):
        """
        Zephyr becomes more cautious as suspicion increases.

        Low suspicion:
            More likely to lie.

        High suspicion:
            More likely to tell the truth.
        """

        lie_probability = max(
            0.15,
            0.75 - suspicion / 100
        )

        will_lie = self.rng.random() < lie_probability

        if will_lie:
            self.lie_count += 1
        else:
            self.truth_count += 1

        self.decisions_log.append(
            f"Mole chose to "
            f"{'LIE' if will_lie else 'TELL THE TRUTH'} "
            f"(suspicion={suspicion})."
        )

        return not will_lie

    # ============================================================
    # ROOM SABOTAGE
    # ============================================================

    def decide_room_action(self, suspicion, actions_remaining):
        """
        Decide whether Zephyr sabotages a room investigation.

        Returns:
            'sabotage'
            'help'
        """

        caution = suspicion / 100

        urgency = (
            0.0
            if actions_remaining > 4
            else (5 - actions_remaining) * 0.1
        )

        sabotage_probability = max(
            0.10,
            min(
                0.90,
                0.65 - caution + urgency
            )
        )

        will_sabotage = (
            self.rng.random() < sabotage_probability
        )

        decision = (
            "sabotage"
            if will_sabotage
            else "help"
        )

        if decision == "sabotage":
            self.sabotage_count += 1
        else:
            self.help_count += 1

        self.decisions_log.append(
            f"Mole chose to {decision.upper()} "
            f"(suspicion={suspicion}, "
            f"actions_remaining={actions_remaining})."
        )

        return decision

    # ============================================================
    # RIDDLE SABOTAGE
    # ============================================================

    def decide_riddle_sabotage(self, suspicion):
        """
        Zephyr may interfere with the Storage riddle.

        Higher suspicion means Zephyr is more likely
        to sabotage the puzzle.
        """

        probability = min(
            0.80,
            0.30 + suspicion / 200
        )

        sabotaged = self.rng.random() < probability

        if sabotaged:
            self.riddle_sabotage_count += 1

        self.decisions_log.append(
            f"Riddle sabotage: "
            f"{'YES' if sabotaged else 'NO'} "
            f"(suspicion={suspicion})."
        )

        return sabotaged

    # ============================================================
    # TIMED SECURITY CHALLENGE
    # ============================================================

    def decide_extra_challenge(
        self,
        suspicion,
        actions_remaining
    ):
        """
        Zephyr decides whether to activate an additional
        security challenge before interrogation.

        The challenge is more likely when:
        - suspicion is high
        - Zephyr has fewer actions remaining to protect himself
        """

        pressure = suspicion / 100

        urgency = (
            0.0
            if actions_remaining > 5
            else 0.15
        )

        probability = min(
            0.75,
            0.20 + pressure * 0.50 + urgency
        )

        activate = self.rng.random() < probability

        if activate:
            self.challenge_sabotage_count += 1

        self.decisions_log.append(
            f"Security challenge: "
            f"{'ACTIVATED' if activate else 'NOT ACTIVATED'} "
            f"(suspicion={suspicion}, "
            f"actions_remaining={actions_remaining})."
        )

        return activate

    # ============================================================
    # STATS
    # ============================================================

    def stats(self):

        return {
            "sabotage_count": self.sabotage_count,
            "help_count": self.help_count,

            "lie_count": self.lie_count,
            "truth_count": self.truth_count,

            "riddle_sabotage_count":
                self.riddle_sabotage_count,

            "challenge_sabotage_count":
                self.challenge_sabotage_count,
        }
