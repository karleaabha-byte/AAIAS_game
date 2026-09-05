"""
evidence.py

Detective notebook.

This does NOT decide who is guilty.
It stores clues and statements so the player can make
their own deductions.
"""

import case


class EvidenceBoard:

    def __init__(self):

        # Physical clues the player discovered
        self.clues_found = set()

        # Answers the player has collected
        self.suspect_statements = {}

        # Notes written by the player
        self.notes = []

        # Pin progress
        self.pin_cracked = False

    # ========================================================
    # CLUES
    # ========================================================

    def add_clue(self, clue_name):

        if clue_name in self.clues_found:
            return False

        self.clues_found.add(clue_name)
        return True

    def has_clue(self, clue_name):
        return clue_name in self.clues_found

    # ========================================================
    # SUSPECT STATEMENTS
    # ========================================================

    def log_answer(
        self,
        character,
        question_key,
        answer,
        truth
    ):

        if character not in self.suspect_statements:
            self.suspect_statements[character] = {}

        self.suspect_statements[character][question_key] = {
            "answer": answer,
            "truth": truth
        }

    def get_statement(self, character, question_key):

        return (
            self.suspect_statements
            .get(character, {})
            .get(question_key)
        )

    # ========================================================
    # PLAYER NOTES
    # ========================================================

    def add_note(self, note):

        note = note.strip()

        if not note:
            return False

        self.notes.append(note)
        return True

    # ========================================================
    # PIN
    # ========================================================

    def set_pin_cracked(self):
        self.pin_cracked = True

    # ========================================================
    # SUMMARY
    # ========================================================

    def get_summary(self):

        return {
            "clues_found": list(self.clues_found),
            "suspect_statements": self.suspect_statements,
            "notes": self.notes,
            "pin_cracked": self.pin_cracked
        }
