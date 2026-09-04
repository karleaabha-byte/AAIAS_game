"""
ai_agent.py - The adversarial mole AI (Zephyr).

The mole has two decision points:
  1. decide_truth_or_lie   -> when questioned by the researcher
  2. decide_room_action    -> when the researcher enters Storage or Cafeteria
                              (Laboratory is not mole-controllable)

Both decisions adapt to the current suspicion level and remaining action
budget, so the mole plays cautiously when it's under scrutiny and takes more
risks when it's running out of time to act.
"""
import random


class MoleAI:
    def __init__(self, seed=None):
        self.rng = random.Random(seed)
        self.sabotage_count = 0
        self.help_count = 0
        self.lie_count = 0
        self.truth_count = 0
        self.decisions_log = []

    def decide_truth_or_lie(self, suspicion):
        """Higher suspicion -> the mole plays it safer and tells the truth more often."""
        lie_probability = max(0.15, 0.75 - suspicion / 100)
        will_lie = self.rng.random() < lie_probability
        if will_lie:
            self.lie_count += 1
        else:
            self.truth_count += 1
        self.decisions_log.append(
            f"Mole chose to {'LIE' if will_lie else 'tell the TRUTH'} (suspicion={suspicion})."
        )
        return not will_lie  # returns tell_truth: bool

    def decide_room_action(self, suspicion, actions_remaining):
        """Returns 'sabotage' or 'help' for a mole-controllable room."""
        caution = suspicion / 100
        # the fewer actions left, the less time there is for a risky move to
        # come back and bite the mole -> slightly more willing to gamble
        urgency = 0.0 if actions_remaining > 4 else (5 - actions_remaining) * 0.1
        sabotage_probability = max(0.1, min(0.9, 0.65 - caution + urgency))

        will_sabotage = self.rng.random() < sabotage_probability
        decision = "sabotage" if will_sabotage else "help"

        if decision == "sabotage":
            self.sabotage_count += 1
        else:
            self.help_count += 1

        self.decisions_log.append(
            f"Mole chose to {decision.upper()} "
            f"(suspicion={suspicion}, actions_remaining={actions_remaining})."
        )
        return decision

    def stats(self):
        return {
            "sabotage_count": self.sabotage_count,
            "help_count": self.help_count,
            "lie_count": self.lie_count,
            "truth_count": self.truth_count,
        }
