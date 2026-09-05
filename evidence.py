"""
evidence.py - Tracks evidence, contradictions, and suspect guilt scores.
"""

import case


class EvidenceBoard:

    def __init__(self):
        self.contradictions = []

        # Individual suspicion for each suspect
        self.guilt_scores = {
            char: 0 for char in case.CHARACTERS
        }

        # character -> question -> answer information
        self.suspect_statements = {}

        # Clues discovered from rooms
        self.clues_found = set()

        # PIN status
        self.pin_cracked = False

    # =========================================================
    # SUSPICION
    # =========================================================

    def add_suspicion(self, character, amount):
        """Increase a suspect's suspicion score."""

        if character not in self.guilt_scores:
            return

        self.guilt_scores[character] += amount

        self.guilt_scores[character] = max(
            0,
            min(100, self.guilt_scores[character])
        )

    def reduce_suspicion(self, character, amount):
        """Decrease a suspect's suspicion score."""

        if character not in self.guilt_scores:
            return

        self.guilt_scores[character] -= amount

        self.guilt_scores[character] = max(
            0,
            min(100, self.guilt_scores[character])
        )

    def get_guilt_score(self, character):
        """Return suspicion score from 0 to 100."""

        return min(
            100,
            max(
                0,
                self.guilt_scores.get(character, 0)
            )
        )

    # =========================================================
    # INTERROGATION
    # =========================================================

    def log_answer(
        self,
        character,
        question_key,
        answer,
        lied
    ):
        """Store an interrogation answer."""

        if character not in self.suspect_statements:
            self.suspect_statements[character] = {}

        self.suspect_statements[character][question_key] = {
            "answer": answer,
            "lied": lied
        }

        # -----------------------------------------------------
        # LIE DETECTION
        # -----------------------------------------------------

        if lied:

            # Base suspicion for lying
            self.add_suspicion(
                character,
                15
            )

            # Lying about an alibi is especially suspicious
            if question_key == "alibi":
                self.add_suspicion(
                    character,
                    15
                )

        # -----------------------------------------------------
        # ZEPHYR-SPECIFIC EVIDENCE
        # -----------------------------------------------------

        if character == "Zephyr":

            # Zephyr denying vent access is extremely suspicious
            # because the background says Supply Coordinator has
            # vent authorization.
            if (
                question_key == "vent"
                and lied
            ):
                self.add_suspicion(
                    "Zephyr",
                    25
                )

            # Zephyr denying vending activity conflicts with
            # the cafeteria evidence.
            elif (
                question_key == "vending"
                and lied
            ):
                self.add_suspicion(
                    "Zephyr",
                    20
                )

            # A false timeline/alibi is suspicious.
            elif (
                question_key == "timeline"
                and lied
            ):
                self.add_suspicion(
                    "Zephyr",
                    15
                )

    # =========================================================
    # CONTRADICTIONS
    # =========================================================

    def detect_contradictions(self):
        """
        Compare statements made by suspects and identify
        contradictions.
        """

        new_contradictions = []

        # =====================================================
        # CHECK 1:
        # ZEPHYR VS RAVEN
        # =====================================================

        zephyr_alibi = (
            self.suspect_statements
            .get("Zephyr", {})
            .get("alibi")
        )

        raven_alibi = (
            self.suspect_statements
            .get("Raven", {})
            .get("alibi")
        )

        if zephyr_alibi and raven_alibi:

            zephyr_answer = (
                zephyr_alibi["answer"]
                .lower()
            )

            raven_answer = (
                raven_alibi["answer"]
                .lower()
            )

            # The false Zephyr alibi contains "lab"
            # and Raven says she was alone.
            zephyr_in_lab = (
                "lab" in zephyr_answer
                or "laboratory" in zephyr_answer
            )

            raven_alone = (
                "alone" in raven_answer
            )

            if zephyr_in_lab and raven_alone:

                contradiction = {
                    "type": "timeline_conflict",
                    "characters": [
                        "Raven",
                        "Zephyr"
                    ],
                    "detail": (
                        "Raven claims she was ALONE in the "
                        "Laboratory, but Zephyr claims he "
                        "was there. Their stories cannot "
                        "both be true."
                    )
                }

                self._add_contradiction(
                    contradiction,
                    new_contradictions,
                    suspicion=30
                )

        # =====================================================
        # CHECK 2:
        # ZEPHYR VS VENT AUTHORIZATION
        # =====================================================

        zephyr_vent = (
            self.suspect_statements
            .get("Zephyr", {})
            .get("vent")
        )

        if zephyr_vent:

            answer = (
                zephyr_vent["answer"]
                .lower()
            )

            denied_access = (
                "no" in answer
                and (
                    "vent" in answer
                    or "access" in answer
                )
            )

            if denied_access:

                contradiction = {
                    "type": "access_conflict",
                    "characters": [
                        "Zephyr"
                    ],
                    "detail": (
                        "Zephyr denied having vent access, "
                        "but the Vent Access Authorization "
                        "identifies the Supply Coordinator "
                        "as an authorized vent user."
                    )
                }

                self._add_contradiction(
                    contradiction,
                    new_contradictions,
                    suspicion=20
                )

        # =====================================================
        # CHECK 3:
        # ZEPHYR VS CAFETERIA
        # =====================================================

        zephyr_vending = (
            self.suspect_statements
            .get("Zephyr", {})
            .get("vending")
        )

        if zephyr_vending:

            answer = (
                zephyr_vending["answer"]
                .lower()
            )

            denied_vending = (
                "wasn't near" in answer
                or "was not near" in answer
                or "not near" in answer
            )

            if (
                denied_vending
                and "cafeteria_pin" in self.clues_found
            ):

                contradiction = {
                    "type": "vending_conflict",
                    "characters": [
                        "Zephyr"
                    ],
                    "detail": (
                        "Zephyr denied being near the "
                        "vending machine, but the cafeteria "
                        "restocking evidence identifies the "
                        "Supply Coordinator's involvement."
                    )
                }

                self._add_contradiction(
                    contradiction,
                    new_contradictions,
                    suspicion=20
                )

        return new_contradictions

    # =========================================================
    # CONTRADICTION HELPER
    # =========================================================

    def _add_contradiction(
        self,
        contradiction,
        new_contradictions,
        suspicion=0
    ):
        """
        Add a contradiction only once.
        """

        existing = any(
            item["type"] == contradiction["type"]
            and item["characters"]
            == contradiction["characters"]
            for item in self.contradictions
        )

        if existing:
            return

        # IMPORTANT:
        # Actually save the contradiction.
        self.contradictions.append(
            contradiction
        )

        new_contradictions.append(
            contradiction
        )

        if suspicion > 0:

            for character in contradiction["characters"]:

                self.add_suspicion(
                    character,
                    suspicion
                )

    # =========================================================
    # ROOM CLUES
    # =========================================================

    def add_clue(self, clue_name):

        if clue_name in self.clues_found:
            return

        self.clues_found.add(
            clue_name
        )

        # -----------------------------------------------------
        # LABORATORY
        # -----------------------------------------------------

        if clue_name == "lab_acrostic":

            # The clue spells FOUR.
            # This is primarily useful for the PIN puzzle.
            # It does not directly accuse anyone.
            pass

        # -----------------------------------------------------
        # STORAGE
        # -----------------------------------------------------

        elif clue_name == "storage_riddle":

            # Riddle answer = BREEZE.
            # BREEZE has 6 letters.
            # This contributes to solving the PIN.
            pass

        # -----------------------------------------------------
        # CAFETERIA
        # -----------------------------------------------------

        elif clue_name == "cafeteria_pin":

            # The restocking record is associated with
            # the Supply Coordinator.
            self.add_suspicion(
                "Zephyr",
                10
            )

    # =========================================================
    # PIN
    # =========================================================

    def set_pin_cracked(self):

        if self.pin_cracked:
            return

        self.pin_cracked = True

        # Cracking the PIN confirms the employee credentials
        # associated with the Supply Coordinator.
        self.add_suspicion(
            "Zephyr",
            20
        )

    # =========================================================
    # SUMMARY
    # =========================================================

    def get_summary(self):

        return {
            "contradictions":
                self.contradictions,

            "guilt_scores":
                self.guilt_scores,

            "clues_found":
                self.clues_found,

            "pin_cracked":
                self.pin_cracked,

            "suspect_statements":
                self.suspect_statements,
        }
