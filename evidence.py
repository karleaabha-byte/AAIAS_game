"""
evidence.py

Evidence board for Zom-Mole Hunter.

This does NOT decide who is guilty.
It stores clues and statements and identifies
possible contradictions between collected statements.
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

        # Contradictions already reported
        self.reported_contradictions = set()


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


    def get_statement(
        self,
        character,
        question_key
    ):

        return (
            self.suspect_statements
            .get(character, {})
            .get(question_key)
        )


    # ========================================================
    # CONTRADICTION DETECTION
    # ========================================================

    def detect_contradictions(self):

        contradictions = []

        statements = self.suspect_statements


        # ====================================================
        # RAVEN / ZEPHYR ALIBI
        # ====================================================

        raven_alibi = (
            statements
            .get("Raven", {})
            .get("alibi")
        )

        zephyr_alibi = (
            statements
            .get("Zephyr", {})
            .get("alibi")
        )


        if raven_alibi and zephyr_alibi:

            raven_text = raven_alibi.get(
                "answer",
                ""
            ).lower()

            zephyr_text = zephyr_alibi.get(
                "answer",
                ""
            ).lower()


            # Raven says she was alone.
            # Zephyr says he was in Storage all night.
            #
            # This is deliberately NOT treated as proof
            # of guilt. It simply records the statements
            # for the detective to interpret.

            if (
                "alone" in raven_text
                and (
                    "storage" in zephyr_text
                    or "didn't leave" in zephyr_text
                    or "did not leave" in zephyr_text
                )
            ):

                contradiction_id = (
                    "raven_zephyr_alibi"
                )


                if (
                    contradiction_id
                    not in self.reported_contradictions
                ):

                    contradictions.append(
                        {
                            "id": contradiction_id,

                            "detail":
                                "Raven says she was alone "
                                "in the Laboratory, while "
                                "Zephyr says he remained in "
                                "Storage throughout the shift."
                        }
                    )

                    self.reported_contradictions.add(
                        contradiction_id
                    )


        # ====================================================
        # RAVEN / LUCA TIMELINE
        # ====================================================

        raven_timeline = (
            statements
            .get("Raven", {})
            .get("timeline")
        )

        luca_timeline = (
            statements
            .get("Luca", {})
            .get("timeline")
        )


        if raven_timeline and luca_timeline:

            raven_text = raven_timeline.get(
                "answer",
                ""
            ).lower()

            luca_text = luca_timeline.get(
                "answer",
                ""
            ).lower()


            if (
                "11:50" in raven_text
                and "11:49" in luca_text
            ):

                contradiction_id = (
                    "raven_luca_timeline"
                )


                if (
                    contradiction_id
                    not in self.reported_contradictions
                ):

                    contradictions.append(
                        {
                            "id": contradiction_id,

                            "detail":
                                "Raven places herself in the "
                                "Laboratory around 11:50 PM, "
                                "while Luca reports responding "
                                "to the camera outage at 11:49 PM."
                        }
                    )

                    self.reported_contradictions.add(
                        contradiction_id
                    )


        # ====================================================
        # ZEPHYR / STORAGE
        # ====================================================

        zephyr_inventory = (
            statements
            .get("Zephyr", {})
            .get("inventory")
        )

        if zephyr_inventory:

            inventory_text = zephyr_inventory.get(
                "answer",
                ""
            ).lower()


            if (
                "counted everything" in inventory_text
                or "counted" in inventory_text
            ):

                contradiction_id = (
                    "zephyr_inventory"
                )


                if (
                    contradiction_id
                    not in self.reported_contradictions
                ):

                    contradictions.append(
                        {
                            "id": contradiction_id,

                            "detail":
                                "Zephyr says he counted the "
                                "Storage inventory before midnight, "
                                "but the case record shows six "
                                "filter cartridges missing."
                        }
                    )

                    self.reported_contradictions.add(
                        contradiction_id
                    )


        return contradictions


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

            "clues_found":
                list(self.clues_found),

            "suspect_statements":
                self.suspect_statements,

            "notes":
                self.notes,

            "pin_cracked":
                self.pin_cracked,

            "contradictions":
                list(
                    self.reported_contradictions
                )
        }
