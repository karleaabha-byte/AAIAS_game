"""
ai_agent.py
Adversarial Mole AI for Zom-Mole Hunter.

Every major Zephyr decision is exactly 50/50.

IMPORTANT:
The AI decision is only made when GameState explicitly asks for it.
Streamlit reruns do NOT cause another decision.
"""

import random


class MoleAI:

    def __init__(self, seed=None):
        self.rng = random.Random(seed)

        self.sabotage_count = 0
        self.help_count = 0

        self.lie_count = 0
        self.truth_count = 0

        self.security_sabotage_count = 0
        self.security_skip_count = 0

        self.decisions_log = []

    # ========================================================
    # TRUTH / LIE
    # ========================================================

    def decide_truth_or_lie(self, suspicion=None):
        """
        EXACTLY 50/50.

        Returns:
            True  -> tell truth
            False -> lie
        """

        tell_truth = self.rng.random() < 0.5

        if tell_truth:
            self.truth_count += 1
        else:
            self.lie_count += 1

        self.decisions_log.append(
            f"Zephyr chose to "
            f"{'TELL THE TRUTH' if tell_truth else 'LIE'}."
        )

        return tell_truth

    # ========================================================
    # ROOM SABOTAGE
    # ========================================================

    def decide_room_action(
        self,
        suspicion=None,
        actions_remaining=None
    ):
        """
        EXACTLY 50/50.

        Returns:
            'sabotage'
            'help'
        """

        will_sabotage = self.rng.random() < 0.5

        if will_sabotage:
            self.sabotage_count += 1
            decision = "sabotage"
        else:
            self.help_count += 1
            decision = "help"

        self.decisions_log.append(
            f"Zephyr chose to {decision.upper()} the room clue."
        )

        return decision

    # ========================================================
    # SECURITY CHALLENGE
    # ========================================================

    def decide_security_sabotage(
        self,
        suspicion=None,
        actions_remaining=None
    ):
        """
        EXACTLY 50/50.

        Returns:
            True  -> deploy timed security challenge
            False -> keep interrogation system normally accessible
        """

        deploy = self.rng.random() < 0.5

        if deploy:
            self.security_sabotage_count += 1
        else:
            self.security_skip_count += 1

        self.decisions_log.append(
            f"Zephyr chose to "
            f"{'DEPLOY' if deploy else 'SKIP'} "
            f"the security challenge."
        )

        return deploy

    # ========================================================
    # DEBUG / STATS
    # ========================================================

    def stats(self):

        return {
            "sabotage_count":
                self.sabotage_count,

            "help_count":
                self.help_count,

            "lie_count":
                self.lie_count,

            "truth_count":
                self.truth_count,

            "security_sabotage_count":
                self.security_sabotage_count,

            "security_skip_count":
                self.security_skip_count,

            "decisions_log":
                list(self.decisions_log)
        }
