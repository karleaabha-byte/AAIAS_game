"""
app.py - Streamlit front-end for "Who Is The Mole?" — NOIR EDITION

Run:
    streamlit run app.py
"""

import html
import streamlit as st
import case

from game import GameState, TOTAL_BUDGET, ROOMS


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Who Is The Mole?",
    page_icon="🧟",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# NOIR AESTHETIC
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
            linear-gradient(
                135deg,
                #1a0f2e 0%,
                #2d1b4e 50%,
                #1f1135 100%
            );
        color: #e0d5d5;
    }

    body {
        font-family: Georgia, serif;
    }

    h1 {
        color: #d4af37;
        font-family: monospace;
        font-size: 2.5rem;
        text-shadow: 0 0 10px rgba(212, 175, 55, 0.5);
        letter-spacing: 3px;
    }

    h2,
    h3 {
        color: #f39c12;
        font-family: monospace;
        text-shadow: 0 0 8px rgba(243, 156, 18, 0.4);
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: #3d2860;
        border-radius: 8px 8px 0 0;
        padding: 10px 18px;
        color: #c9a961;
        font-family: monospace;
        border: 1px solid #5a3d8a;
    }

    .stTabs [aria-selected="true"] {
        background-color: #5a3d8a !important;
        color: #d4af37 !important;
        border: 1px solid #d4af37;
    }

    div[data-testid="stExpander"] {
        border: 1px solid #5a3d8a;
        border-radius: 10px;
        background-color: #2d1f42;
    }

    div[data-testid="stMetricValue"] {
        color: #f39c12;
        font-size: 1.8rem;
        font-family: monospace;
    }

    .stButton > button {
        background-color: #5a3d8a;
        color: #d4af37;
        border-radius: 8px;
        border: 1.5px solid #d4af37;
        font-family: monospace;
        font-weight: bold;
        box-shadow: 0 0 8px rgba(212, 175, 55, 0.3);
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        background-color: #d4af37;
        color: #1a0f2e;
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.8);
    }

    .case-file {
        background: rgba(45, 31, 66, 0.85);
        border: 1px solid #5a3d8a;
        border-left: 4px solid #d4af37;
        border-radius: 8px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 5px 25px rgba(0, 0, 0, 0.35);
    }

    .background-section {
        background: #2d1f42;
        border: 1px solid #5a3d8a;
        border-radius: 8px;
        padding: 16px;
        margin: 12px 0;
        font-family: monospace;
    }

    .background-title {
        color: #d4af37;
        font-weight: bold;
        margin-bottom: 12px;
        font-size: 1rem;
        letter-spacing: 1px;
    }

    .background-entry {
        color: #c9a961;
        padding: 8px 0;
        border-bottom: 1px dotted #5a3d8a;
        line-height: 1.5;
    }

    /* ========================================================
       LAB NOTE
       ======================================================== */

    .note-card {
        background: #f4ecd8;
        color: #3a3226;
        font-family: Georgia, serif;
        padding: 25px;
        border-radius: 2px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.7);
        transform: rotate(-1deg);
        margin: 14px 4px;
        line-height: 1.9;
        font-size: 1.05rem;
    }

    .note-line {
        margin: 7px 0;
    }

    /* ========================================================
       STORAGE
       ======================================================== */

    .riddle-board {
        background-color: #10151f;

        background-image:
            linear-gradient(
                #1c2434 1px,
                transparent 1px
            ),
            linear-gradient(
                90deg,
                #1c2434 1px,
                transparent 1px
            );

        background-size: 22px 22px;

        color: #e5e7eb;
        font-family: Georgia, serif;
        font-size: 1.1rem;
        padding: 24px;
        border-radius: 8px;
        border: 2px solid #334155;
        line-height: 1.8;
        margin: 14px 4px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.7);
    }

    .riddle-line {
        margin: 5px 0;
    }

    .scratched {
        text-decoration: line-through;
        text-decoration-thickness: 3px;
        text-decoration-color: #ef4444;
        color: #94a3b8;
    }

    .decoy-line {
        color: #fbbf24;
        font-style: italic;
    }

    .helper-line {
        color: #94a3b8;
        font-style: italic;
    }

    .riddle-question {
        color: #f1f5f9;
        font-style: italic;
        margin-top: 14px;
    }

    /* ========================================================
       RECEIPT
       ======================================================== */

    .receipt {
        background: #fdfdfd;
        color: #111;
        font-family: "Courier New", monospace;
        padding: 20px;
        border: 1px dashed #777;
        max-width: 340px;
        margin: 14px auto;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.7);
    }

    .receipt-title {
        text-align: center;
        font-weight: bold;
        margin-bottom: 12px;
        border-bottom: 1px dashed #777;
        padding-bottom: 8px;
    }

    .pin-display {
        margin-top: 12px;
        font-size: 1.2rem;
        font-weight: bold;
    }

    .pin-digit {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 30px;
        height: 34px;
        margin: 0 3px;
        border-bottom: 2px solid #333;
        font-weight: bold;
        font-size: 1.2rem;
    }

    .pin-redacted {
        color: #999;
    }

    /* ========================================================
       NOTEBOOK
       ======================================================== */

    .notebook {
        background:
            repeating-linear-gradient(
                #21182b,
                #21182b 31px,
                #392b42 32px
            );
        border: 1px solid #705d7d;
        border-radius: 6px;
        padding: 22px;
        margin: 10px 0;
        min-height: 100px;
    }

    /* ========================================================
       STATEMENTS
       ======================================================== */

    .statement-card {
        background: #241936;
        border-left: 4px solid #d4af37;
        border-radius: 6px;
        padding: 16px;
        margin: 12px 0;
    }

    .statement-character {
        color: #d4af37;
        font-family: monospace;
        font-weight: bold;
        font-size: 1rem;
    }

    .statement-question {
        color: #9d8ca8;
        font-size: 0.85rem;
        margin-top: 8px;
    }

    .statement-answer {
        color: #f0e7d8;
        font-family: Georgia, serif;
        font-size: 1.15rem;
        line-height: 1.5;
        margin-top: 8px;
    }

    /* ========================================================
       SUSPECT
       ======================================================== */

    .suspect-card {
        background: #3d2860;
        border-left: 4px solid #f39c12;
        padding: 15px;
        margin: 8px 0;
        border-radius: 4px;
    }

    /* ========================================================
       QUOTE
       ======================================================== */

    .quote-box {
        background: #1a1024;
        border-left: 3px solid #d4af37;
        padding: 18px;
        margin: 12px 0;
        font-family: Georgia, serif;
        font-size: 1.2rem;
        line-height: 1.5;
        color: #f0e7d8;
    }

    /* ========================================================
       LOG
       ======================================================== */

    .log-entry {
        font-family: monospace;
        font-size: 0.85rem;
        color: #c9a961;
        padding: 5px 0;
        border-bottom: 1px dotted #5a3d8a;
    }

    /* ========================================================
       CLUE CHIP
       ======================================================== */

    .clue-chip {
        display: inline-block;
        padding: 7px 12px;
        margin: 4px;
        border: 1px solid #725b7b;
        color: #d8c9dc;
        background: #201825;
        font-size: 0.75rem;
        border-radius: 4px;
    }

    /* ========================================================
       FINAL REPORT
       ======================================================== */

    .verdict-box {
        background: #21152d;
        border: 2px solid #d4af37;
        border-radius: 8px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 0 25px rgba(212, 175, 55, 0.2);
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "game" not in st.session_state:
    st.session_state.game = GameState()

if "researcher_name" not in st.session_state:
    st.session_state.researcher_name = ""

if "detective_notes" not in st.session_state:
    st.session_state.detective_notes = []

if "final_evidence_saved" not in st.session_state:
    st.session_state.final_evidence_saved = []

if "final_reasoning_saved" not in st.session_state:
    st.session_state.final_reasoning_saved = ""


game = st.session_state.game


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def safe_html(value):
    return html.escape(str(value))


def get_profile(character):
    profiles = getattr(case, "PROFILES", {})

    if isinstance(profiles, dict):
        return profiles.get(character, {})

    return {}


def get_question_text(question_key):
    questions = getattr(case, "QUESTION_BANK", {})

    if isinstance(questions, dict):
        return questions.get(question_key, question_key)

    return str(question_key)


def get_statement_data(character):
    statements = getattr(
        game.evidence,
        "suspect_statements",
        {}
    )

    if not isinstance(statements, dict):
        return {}

    value = statements.get(character, {})

    if isinstance(value, dict):
        return value

    return {}


def statement_count():
    total = 0

    statements = getattr(
        game.evidence,
        "suspect_statements",
        {}
    )

    if not isinstance(statements, dict):
        return 0

    for value in statements.values():

        if isinstance(value, dict):
            total += len(value)

        elif value:
            total += 1

    return total


# ============================================================
# LAB RENDERER
# ============================================================

def render_lab_note(lines):
    """
    Render the laboratory note.

    First letters are NOT highlighted.
    The player must discover the acrostic.
    """

    html_output = '<div class="note-card">'

    for item in lines:

        if isinstance(item, str):

            text = item

        elif isinstance(item, (list, tuple)) and len(item) >= 2:

            text = f"{item[0]}{item[1]}"

        elif isinstance(item, dict):

            text = item.get(
                "text",
                item.get("content", "")
            )

            if item.get("letter"):
                text = f"{item['letter']}{text}"

        else:

            text = str(item)

        html_output += (
            '<div class="note-line">'
            f'{safe_html(text)}'
            '</div>'
        )

    html_output += "</div>"

    st.markdown(
        html_output,
        unsafe_allow_html=True
    )


# ============================================================
# STORAGE INVENTORY BOARD
# ============================================================

def render_storage_board(lines):
    """Render the scratched storage inventory board."""

    html_output = '<div class="riddle-board">'

    for item in lines:

        if isinstance(item, dict):

            classes = ["riddle-line"]

            if item.get("struck"):
                classes.append("scratched")

            if item.get("decoy"):
                classes.append("decoy-line")

            if item.get("helper"):
                classes.append("helper-line")

            text = item.get(
                "text",
                item.get("content", "")
            )

        else:

            classes = ["riddle-line"]
            text = str(item)

        class_string = " ".join(classes)

        html_output += (
            f'<div class="{class_string}">'
            f'{safe_html(text)}'
            '</div>'
        )

    html_output += "</div>"

    st.markdown(
        html_output,
        unsafe_allow_html=True
    )


# ============================================================
# STORAGE RIDDLE
# ============================================================

def render_storage_riddle(riddle):
    """
    Render the Storage riddle.

    The answer is never displayed.
    """

    html_output = '<div class="riddle-board">'

    for index, line in enumerate(riddle):

        if index == len(riddle) - 1:

            html_output += (
                '<div class="riddle-question">'
                f'{safe_html(line)}'
                '</div>'
            )

        else:

            html_output += (
                '<div class="riddle-line">'
                f'{safe_html(line)}'
                '</div>'
            )

    html_output += "</div>"

    st.markdown(
        html_output,
        unsafe_allow_html=True
    )


# ============================================================
# CAFETERIA RECEIPT
# ============================================================

def render_receipt(job, pin_digits, redacted):
    """
    Render cafeteria receipt.

    Example:
        4 ? 1 9
    """

    if isinstance(pin_digits, (list, tuple)):
        digits = list(pin_digits)
    else:
        digits = list(str(pin_digits))

    if isinstance(redacted, str):

        redacted_values = [
            char in ("?", "x", "X", "*")
            for char in redacted
        ]

    elif isinstance(redacted, (list, tuple)):

        redacted_values = list(redacted)

    else:

        redacted_values = []

    html_output = '<div class="receipt">'

    html_output += (
        '<div class="receipt-title">'
        'RESTOCKING LOG — MACHINE #3'
        '</div>'
    )

    html_output += (
        '<div>'
        'Restocked by: '
        f'<b>{safe_html(job)}</b>'
        '</div>'
    )

    html_output += (
        '<div class="pin-display">'
        'Employee PIN: '
    )

    for index, digit in enumerate(digits):

        is_redacted = (
            index < len(redacted_values)
            and bool(redacted_values[index])
        )

        if is_redacted:

            html_output += (
                '<span class="pin-digit pin-redacted">'
                '?'
                '</span>'
            )

        else:

            html_output += (
                '<span class="pin-digit">'
                f'{safe_html(digit)}'
                '</span>'
            )

    html_output += "</div>"
    html_output += "</div>"

    st.markdown(
        html_output,
        unsafe_allow_html=True
    )


# ============================================================
# GENERIC CLUE RENDERER
# ============================================================

def render_clue(room, clue):

    if not isinstance(clue, dict):

        st.write(clue)
        return

    # ========================================================
    # LABORATORY
    # ========================================================

    if room == "Laboratory":

        if clue.get("title"):

            st.markdown(
                f"### {safe_html(clue['title'])}"
            )

        if clue.get("lines"):

            render_lab_note(
                clue["lines"]
            )

        if clue.get("note"):

            st.info(
                clue["note"]
            )

        if clue.get("description"):

            st.write(
                clue["description"]
            )

    # ========================================================
    # STORAGE
    # ========================================================

    elif room == "Storage":

        if clue.get("title"):

            st.markdown(
                f"### {safe_html(clue['title'])}"
            )

        if clue.get("lines"):

            render_storage_board(
                clue["lines"]
            )

        if clue.get("riddle"):

            st.markdown(
                "#### Something written in the margin..."
            )

            render_storage_riddle(
                clue["riddle"]
            )

        if clue.get("note"):

            st.info(
                clue["note"]
            )

        if clue.get("description"):

            st.write(
                clue["description"]
            )

    # ========================================================
    # CAFETERIA
    # ========================================================

    elif room == "Cafeteria":

        if clue.get("title"):

            st.markdown(
                f"### {safe_html(clue['title'])}"
            )

        if all(
            key in clue
            for key in (
                "job",
                "pin_digits",
                "redacted"
            )
        ):

            render_receipt(
                clue["job"],
                clue["pin_digits"],
                clue["redacted"]
            )

        if clue.get("note"):

            st.info(
                clue["note"]
            )

        if clue.get("hidden_note"):

            st.caption(
                clue["hidden_note"]
            )

        if clue.get("description"):

            st.write(
                clue["description"]
            )


# ============================================================
# RESET CASE
# ============================================================

def reset_case():

    st.session_state.game = GameState()

    st.session_state.researcher_name = ""

    st.session_state.detective_notes = []

    st.session_state.final_evidence_saved = []

    st.session_state.final_reasoning_saved = ""

    keys_to_remove = [
        "detective_note",
        "final_reasoning",
        "final_suspect",
        "final_evidence",
        "pin_guess",
    ]

    for key in keys_to_remove:

        if key in st.session_state:

            del st.session_state[key]


# ============================================================
# TITLE
# ============================================================

st.title("🧟 WHO IS THE MOLE?")

if st.session_state.researcher_name:

    st.caption(
        f"Detective Case File: "
        f"{st.session_state.researcher_name} | "
        f"{game.actions_remaining} Actions Remaining"
    )

else:

    st.caption(
        "A noir-tinged mystery awaits... "
        "12 actions to crack the case."
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("CASE DOSSIER")

    new_name = st.text_input(
        "Detective name",
        value=st.session_state.researcher_name,
    )

    st.session_state.researcher_name = new_name

    if new_name:

        st.write(
            f"**Detective:** {new_name}"
        )

    st.divider()

    st.subheader(
        "Actions Remaining"
    )

    st.metric(
        "",
        game.actions_remaining
    )

    progress = (
        game.actions_used / TOTAL_BUDGET
        if TOTAL_BUDGET > 0
        else 0
    )

    progress = max(
        0.0,
        min(1.0, progress)
    )

    st.progress(progress)

    st.caption(
        f"{game.actions_used} of "
        f"{TOTAL_BUDGET} actions used"
    )

    st.divider()

    st.subheader(
        "Investigation"
    )

    st.write(
        f"🏚️ Scenes searched: "
        f"**{len(game.visited_rooms)}/{len(ROOMS)}**"
    )

    st.write(
        f"🗣️ Statements collected: "
        f"**{statement_count()}**"
    )

    st.write(
        f"🔎 Physical clues: "
        f"**{len(game.evidence.clues_found)}**"
    )

    if game.pin_cracked:

        st.success(
            "🔓 Cafeteria PIN cracked"
        )

    st.divider()

    with st.expander(
        "📋 CASE LOG"
    ):

        if game.log:

            for entry in reversed(
                game.log[-10:]
            ):

                st.markdown(
                    '<div class="log-entry">'
                    f'• {safe_html(entry)}'
                    '</div>',
                    unsafe_allow_html=True
                )

        else:

            st.write(
                "*No entries yet.*"
            )

    st.divider()

    if st.button(
        "🔄 START NEW CASE",
        use_container_width=True
    ):

        reset_case()
        st.rerun()


# ============================================================
# CASE INTRO
# ============================================================

st.markdown(
    '<div class="case-file">',
    unsafe_allow_html=True
)

case_intro = getattr(
    case,
    "CASE_INTRO",
    "A mysterious incident has occurred."
)

st.markdown(
    case_intro
)

st.markdown(
    "</div>",
    unsafe_allow_html=True
)


# ============================================================
# END OF GAME
# ============================================================

if game.game_over:

    st.divider()

    if game.result == "win":

        st.markdown(
            """
            <div class="verdict-box">
                <h1>CASE SOLVED</h1>
                <h2>THE MOLE HAS BEEN IDENTIFIED</h2>
                <p>
                    Your accusation was correct.
                    The evidence led you to the right suspect.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            """
            <div class="verdict-box">
                <h1>CASE FAILED</h1>
                <h2>THE MOLE GOT AWAY</h2>
                <p>
                    Your accusation did not identify the Mole.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.warning(
            f"The real Mole was **{case.MOLE}**."
        )

    st.divider()

    st.subheader(
        "INVESTIGATION REPORT"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Actions Used",
            f"{game.actions_used}/{TOTAL_BUDGET}"
        )

    with col2:

        st.metric(
            "Scenes Searched",
            len(game.visited_rooms)
        )

    with col3:

        st.metric(
            "Statements",
            statement_count()
        )

    st.divider()

    st.subheader(
        "Your Accusation"
    )

    st.write(
        f"**Suspect:** {game.accused}"
    )

    if game.result == "win":

        st.success(
            "Correct accusation."
        )

    else:

        st.error(
            "Incorrect accusation."
        )

    if st.session_state.final_evidence_saved:

        st.divider()

        st.subheader(
            "Evidence You Selected"
        )

        for evidence in (
            st.session_state.final_evidence_saved
        ):

            st.markdown(
                '<span class="clue-chip">'
                f'✓ {safe_html(evidence)}'
                '</span>',
                unsafe_allow_html=True
            )

    if st.session_state.final_reasoning_saved:

        st.divider()

        st.subheader(
            "Your Reasoning"
        )

        st.markdown(
            '<div class="quote-box">'
            f'{safe_html(st.session_state.final_reasoning_saved)}'
            '</div>',
            unsafe_allow_html=True
        )

    st.divider()

    st.subheader(
        "Your Detective Notes"
    )

    if st.session_state.detective_notes:

        for index, saved_note in enumerate(
            st.session_state.detective_notes,
            start=1
        ):

            st.markdown(
                '<div class="notebook">'
                f'<strong>NOTE {index}</strong>'
                '<br><br>'
                f'{safe_html(saved_note)}'
                '</div>',
                unsafe_allow_html=True
            )

    else:

        st.caption(
            "No notes were recorded."
        )

    st.stop()


# ============================================================
# MAIN TABS
# ============================================================

(
    tab_background,
    tab_evidence,
    tab_rooms,
    tab_people,
    tab_accuse,
) = st.tabs(
    [
        "📋 BACKGROUND",
        "📓 DETECTIVE NOTEBOOK",
        "🏚️ CRIME SCENES",
        "🗣️ INTERROGATIONS",
        "⚖️ ACCUSATION",
    ]
)


# ============================================================
# BACKGROUND TAB
# ============================================================

with tab_background:

    st.subheader(
        "THE NIGHT SHIFT INCIDENT"
    )

    st.write(
        "These are the established facts of the case. "
        "Pay attention to times, locations and who had "
        "access to what."
    )

    background = getattr(
        case,
        "BACKGROUND",
        {}
    )

    if isinstance(background, dict):

        for section, section_data in background.items():

            st.markdown(
                '<div class="background-section">',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="background-title">'
                f'{safe_html(section)}'
                '</div>',
                unsafe_allow_html=True
            )

            if isinstance(section_data, dict):

                if "entries" in section_data:

                    for entry in section_data["entries"]:

                        if (
                            isinstance(entry, (list, tuple))
                            and len(entry) >= 2
                        ):

                            label = entry[0]
                            text = entry[1]

                            st.markdown(
                                '<div class="background-entry">'
                                f'<strong>{safe_html(label)}</strong>'
                                f' &nbsp; '
                                f'{safe_html(text)}'
                                '</div>',
                                unsafe_allow_html=True
                            )

                        else:

                            st.markdown(
                                '<div class="background-entry">'
                                f'{safe_html(entry)}'
                                '</div>',
                                unsafe_allow_html=True
                            )

                if "notes" in section_data:

                    for note_text in section_data["notes"]:

                        st.markdown(
                            '<div class="background-entry">'
                            f'• {safe_html(note_text)}'
                            '</div>',
                            unsafe_allow_html=True
                        )

            else:

                st.write(
                    section_data
                )

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )

    else:

        st.write(
            background
        )


# ============================================================
# DETECTIVE NOTEBOOK
# ============================================================

with tab_evidence:

    st.subheader(
        "📓 Detective Notebook"
    )

    st.write(
        "The game will not tell you who looks guilty. "
        "That's your job."
    )

    st.info(
        "Look for statements that don't fit the facts "
        "in the Background tab."
    )

    # --------------------------------------------------------
    # PHYSICAL EVIDENCE
    # --------------------------------------------------------

    st.subheader(
        "Physical Evidence"
    )

    clue_names = {

        "lab_acrostic":
            "🧪 Laboratory note",

        "storage_riddle":
            "📦 Storage inventory board",

        "cafeteria_pin":
            "🥤 Cafeteria restocking receipt",
    }

    clues = getattr(
        game.evidence,
        "clues_found",
        []
    )

    if clues:

        for clue in clues:

            st.markdown(
                '<span class="clue-chip">'
                f'✓ {safe_html(clue_names.get(clue, clue))}'
                '</span>',
                unsafe_allow_html=True
            )

    else:

        st.caption(
            "No physical evidence collected yet."
        )

    # --------------------------------------------------------
    # STATEMENTS
    # --------------------------------------------------------

    st.divider()

    st.subheader(
        "Collected Statements"
    )

    any_statements = False

    for character in case.CHARACTERS:

        statements = get_statement_data(
            character
        )

        if not statements:
            continue

        any_statements = True

        profile = get_profile(
            character
        )

        role = profile.get(
            "role",
            "Unknown role"
        )

        with st.expander(
            f"🧑 {character} — {role}"
        ):

            for question_key, statement in statements.items():

                if not isinstance(
                    statement,
                    dict
                ):
                    continue

                answer = statement.get(
                    "answer",
                    ""
                )

                st.markdown(
                    '<div class="statement-card">'
                    '<div class="statement-character">'
                    f'{safe_html(character)}'
                    '</div>'
                    '<div class="statement-question">'
                    f'Q: {safe_html(get_question_text(question_key))}'
                    '</div>'
                    '<div class="statement-answer">'
                    f'“{safe_html(answer)}”'
                    '</div>'
                    '</div>',
                    unsafe_allow_html=True
                )

    if not any_statements:

        st.info(
            "No statements collected. "
            "Head to the Interrogations tab."
        )

    # --------------------------------------------------------
    # PLAYER NOTES
    # --------------------------------------------------------

    st.divider()

    st.subheader(
        "✍️ Your Notes"
    )

    st.caption(
        "This is where you connect the dots."
    )

    note = st.text_area(
        "Write a deduction",
        placeholder=(
            "Write down anything suspicious..."
        ),
        height=120,
        key="detective_note",
    )

    if st.button(
        "✍️ ADD TO NOTEBOOK",
        use_container_width=True
    ):

        if note.strip():

            st.session_state.detective_notes.append(
                note.strip()
            )

            del st.session_state["detective_note"]

            st.rerun()

        else:

            st.warning(
                "Write something first."
            )

    if st.session_state.detective_notes:

        st.divider()

        st.subheader(
            "Notebook Entries"
        )

        for index, saved_note in enumerate(
            st.session_state.detective_notes,
            start=1
        ):

            st.markdown(
                '<div class="notebook">'
                f'<strong>NOTE {index}</strong>'
                '<br><br>'
                f'{safe_html(saved_note)}'
                '</div>',
                unsafe_allow_html=True
            )


# ============================================================
# CRIME SCENES
# ============================================================

with tab_rooms:

    st.subheader(
        "🏚️ Crime Scenes"
    )

    st.write(
        f"You have **{game.actions_remaining} actions** remaining."
    )

    room_descriptions = {

        "Laboratory":
            "The centrifuge room where the incident began.",

        "Storage":
            "Shelves, inventory sheets and the ventilation panel.",

        "Cafeteria":
            "A vending machine, a restocking cart "
            "and one suspicious receipt.",
    }

    cols = st.columns(
        len(ROOMS)
    )

    for col, room in zip(
        cols,
        ROOMS
    ):

        with col:

            st.markdown(
                f"### {room}"
            )

            st.caption(
                room_descriptions.get(
                    room,
                    "A location inside the facility."
                )
            )

            # =================================================
            # INVESTIGATED
            # =================================================

            if room in game.visited_rooms:

                st.success(
                    "✓ Location investigated"
                )

                clue = game.visited_rooms[room]

                render_clue(
                    room,
                    clue
                )

                # =================================================
                # CAFETERIA PIN
                # =================================================

                if room == "Cafeteria":

                    st.divider()

                    st.markdown(
                        "**🔐 Crack the Employee PIN**"
                    )

                    if game.pin_cracked:

                        st.success(
                            "🔓 PIN CRACKED"
                        )

                    else:

                        pin_guess = st.text_input(
                            "Enter four digits",
                            max_chars=4,
                            key="pin_guess",
                        )

                        if st.button(
                            "🔓 VERIFY PIN",
                            key="verify_pin",
                            use_container_width=True,
                        ):

                            if (
                                len(pin_guess) != 4
                                or not pin_guess.isdigit()
                            ):

                                st.warning(
                                    "Enter exactly four digits."
                                )

                            else:

                                pin_correct = (
                                    game.attempt_pin(
                                        pin_guess
                                    )
                                )

                                if pin_correct:

                                    st.success(
                                        "🔓 PIN CRACKED"
                                    )

                                    st.rerun()

                                else:

                                    st.error(
                                        "❌ Incorrect PIN."
                                    )

            # =================================================
            # NOT INVESTIGATED
            # =================================================

            else:

                if st.button(
                    f"🔎 Investigate {room}",
                    key=f"visit_{room}",
                    disabled=not game.can_act(),
                    use_container_width=True,
                ):

                    success, payload = (
                        game.visit_room(room)
                    )

                    if success:

                        st.rerun()

                    else:

                        st.warning(
                            str(payload)
                        )


# ============================================================
# INTERROGATIONS
# ============================================================

with tab_people:

    st.subheader(
        "🗣️ Interrogation Room"
    )

    st.write(
        "Everyone has something to say. "
        "The trick is figuring out whether it matters."
    )

    question_bank = getattr(
        case,
        "QUESTION_BANK",
        {}
    )

    for character in case.CHARACTERS:

        profile = get_profile(
            character
        )

        with st.expander(
            f"🧑 {character} — "
            f"{profile.get('role', 'Unknown role')}"
        ):

            st.markdown(
                '<div class="suspect-card">'
                f'<strong>{safe_html(character)}</strong>'
                '<br>'
                '<span style="color:#c9a961;font-size:.8rem;">'
                f'{safe_html(profile.get("role", "Unknown role"))}'
                ' • '
                f'{safe_html(profile.get("location", "Unknown"))}'
                '</span>'
                '<br><br>'
                f'{safe_html(profile.get("description", ""))}'
                '<br><br>'
                f'<i>{safe_html(profile.get("personality", ""))}</i>'
                '</div>',
                unsafe_allow_html=True
            )

            asked_data = game.asked.get(
                character
            )

            # =================================================
            # ALREADY QUESTIONED
            # =================================================

            if asked_data:

                question_key = asked_data.get(
                    "question"
                )

                answer = asked_data.get(
                    "answer",
                    ""
                )

                st.markdown(
                    "**Statement collected:**"
                )

                st.markdown(
                    '<div class="statement-card">'
                    '<div class="statement-question">'
                    f'Q: {safe_html(get_question_text(question_key))}'
                    '</div>'
                    '<div class="statement-answer">'
                    f'“{safe_html(answer)}”'
                    '</div>'
                    '</div>',
                    unsafe_allow_html=True
                )

                st.info(
                    "You have already questioned this person. "
                    "Study their statement against the evidence."
                )

            # =================================================
            # NOT QUESTIONED
            # =================================================

            else:

                if (
                    isinstance(question_bank, dict)
                    and question_bank
                ):

                    question_keys = list(
                        question_bank.keys()
                    )

                    q_key = st.selectbox(
                        "Question",
                        options=question_keys,
                        format_func=get_question_text,
                        key=f"question_{character}",
                    )

                    if st.button(
                        f"💬 Ask {character}",
                        key=f"ask_{character}",
                        disabled=not game.can_act(),
                        use_container_width=True,
                    ):

                        success, answer = (
                            game.ask_question(
                                character,
                                q_key
                            )
                        )

                        if success:

                            st.rerun()

                        else:

                            st.warning(
                                str(answer)
                            )

                else:

                    st.warning(
                        "No questions are configured."
                    )


# ============================================================
# ACCUSATION
# ============================================================

with tab_accuse:

    st.subheader(
        "⚖️ Final Accusation"
    )

    st.warning(
        "Once you submit an accusation, "
        "the investigation ends."
    )

    st.write(
        "Don't accuse someone simply because they lied. "
        "Accuse the person whose statements and actions "
        "connect to the actual incident."
    )

    suspect = st.selectbox(
        "Who is the Mole?",
        case.CHARACTERS,
        key="final_suspect",
    )

    st.divider()

    st.subheader(
        "What convinced you?"
    )

    evidence_options = []

    clue_labels = {

        "lab_acrostic":
            "🧪 Laboratory note",

        "storage_riddle":
            "📦 Storage inventory board",

        "cafeteria_pin":
            "🥤 Cafeteria restocking receipt",
    }

    # Physical clues
    for clue in getattr(
        game.evidence,
        "clues_found",
        []
    ):

        label = clue_labels.get(
            clue,
            str(clue)
        )

        if label not in evidence_options:

            evidence_options.append(
                label
            )

    # Statements
    for character in case.CHARACTERS:

        statements = get_statement_data(
            character
        )

        for question_key in statements:

            label = (
                f"🗣️ {character}: "
                f"{get_question_text(question_key)}"
            )

            if label not in evidence_options:

                evidence_options.append(
                    label
                )

    if evidence_options:

        selected_evidence = st.multiselect(
            "Select the clues/statements "
            "that support your accusation",
            evidence_options,
            key="final_evidence",
        )

    else:

        selected_evidence = []

        st.info(
            "You haven't collected any evidence yet."
        )

    st.divider()

    st.subheader(
        "Your Reasoning"
    )

    reasoning = st.text_area(
        "Build your case",
        placeholder=(
            "Explain why the evidence points to this person..."
        ),
        height=180,
        key="final_reasoning",
    )

    st.divider()

    if st.button(
        "🔨 SUBMIT FINAL ACCUSATION",
        type="primary",
        use_container_width=True,
        disabled=not game.can_act(),
    ):

        if not selected_evidence:

            st.error(
                "A detective needs evidence. "
                "Select at least one piece of evidence."
            )

        elif not reasoning.strip():

            st.error(
                "Explain your reasoning before "
                "closing the case."
            )

        else:

            st.session_state.final_evidence_saved = (
                selected_evidence.copy()
            )

            st.session_state.final_reasoning_saved = (
                reasoning.strip()
            )

            success, result = (
                game.make_accusation(
                    suspect
                )
            )

            if success:

                st.rerun()

            else:

                st.error(
                    str(result)
                )


# ============================================================
# OUT OF ACTIONS
# ============================================================

if (
    game.actions_remaining == 0
    and not game.game_over
):

    st.error(
        "⏰ You have used all 12 actions. "
        "The facility is running out of time. "
        "Make your final accusation."
    )
