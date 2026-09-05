"""
evidence.py - Tracks evidence, contradictions, and suspect guilt scores.
"""
import case


class EvidenceBoard:
    def __init__(self):
        self.contradictions = []
        self.guilt_scores = {char: 0 for char in case.CHARACTERS}
        self.suspect_statements = {}  # character -> {question_key -> {answer, lied}}
        self.clues_found = set()
        self.pin_cracked = False

    def log_answer(self, character, question_key, answer, lied):
        if character not in self.suspect_statements:
            self.suspect_statements[character] = {}
        self.suspect_statements[character][question_key] = {"answer": answer, "lied": lied}

        # Immediate guilt bump for lying
        if lied:
            self.guilt_scores[character] += 15
            if question_key == "alibi":
                self.guilt_scores[character] += 25

    def detect_contradictions(self):
        """Scan all statements for timeline/access conflicts."""
        new_contradictions = []

        # Check 1: Zephyr claims to be in Lab, but Raven claims she was alone
        zephyr_in_lab = (
            "alibi" in self.suspect_statements.get("Zephyr", {})
            and "Laboratory" in self.suspect_statements["Zephyr"]["alibi"].get("answer", "")
        )
        raven_alone = (
            "alibi" in self.suspect_statements.get("Raven", {})
            and "alone" in self.suspect_statements["Raven"]["alibi"].get("answer", "").lower()
        )
        if zephyr_in_lab and raven_alone:
            contradiction = {
                "type": "timeline_conflict",
                "characters": ["Raven", "Zephyr"],
                "detail": "Raven claims she was ALONE in the Laboratory, but Zephyr claims to have been there.",
            }
            if contradiction not in self.contradictions and contradiction not in new_contradictions:
                new_contradictions.append(contradiction)
                self.guilt_scores["Zephyr"] += 30

        # Check 2: Luca saw Zephyr at the vending machine late
        luca_saw_zephyr = (
            "vending" in self.suspect_statements.get("Luca", {})
            and ("Zephyr" in self.suspect_statements["Luca"]["vending"].get("answer", "")
                 or "Supply Coordinator" in self.suspect_statements["Luca"]["vending"].get("answer", ""))
        )
        if luca_saw_zephyr:
            self.guilt_scores["Zephyr"] += 10

        # Check 3: Zephyr denied being near vending but admits restocking when questioned
        zephyr_denied = (
            "vending" in self.suspect_statements.get("Zephyr", {})
            and "no idea" in self.suspect_statements["Zephyr"]["vending"].get("answer", "").lower()
        )
        zephyr_admitted = (
            "vending" in self.suspect_statements.get("Zephyr", {})
            and "restocked" in self.suspect_statements["Zephyr"]["vending"].get("answer", "").lower()
        )
        # (This is caught in game.py's lying detection, but worth flagging here too)

        # Check 4: Zephyr has vent access
        zephyr_has_access = (
            "access" in self.suspect_statements.get("Zephyr", {})
            and ("yes" in self.suspect_statements["Zephyr"]["access"].get("answer", "").lower()
                 or "full vent access" in self.suspect_statements["Zephyr"]["access"].get("answer", "").lower())
        )
        if zephyr_has_access:
            self.guilt_scores["Zephyr"] += 20

        return new_contradictions

    def add_clue(self, clue_name):
        self.clues_found.add(clue_name)
        if clue_name == "lab_acrostic":
            self.guilt_scores["Zephyr"] += 5
        elif clue_name == "storage_riddle":
            self.guilt_scores["Zephyr"] += 5
        elif clue_name == "cafeteria_pin":
            self.guilt_scores["Zephyr"] += 5

    def set_pin_cracked(self):
        self.pin_cracked = True
        self.guilt_scores["Zephyr"] += 15

    def get_guilt_score(self, character):
        return min(100, self.guilt_scores.get(character, 0))

    def get_summary(self):
        return {
            "contradictions": self.contradictions,
            "guilt_scores": self.guilt_scores,
            "clues_found": self.clues_found,
            "pin_cracked": self.pin_cracked,
        }
