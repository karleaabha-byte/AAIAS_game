"""
app.py - Streamlit front-end for "Who Is the Mole?" — NOIR EDITION

Run with:
    streamlit run app.py
"""

import streamlit as st
import io
import base64

import numpy as np
from scipy.io import wavfile

import case
from game import GameState, TOTAL_BUDGET


# ============================================================
# INLINE SOUND GENERATION
# ============================================================

try:
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False


def generate_beep(
    frequency=1000,
    duration=0.2,
    sample_rate=22050
):
    if not AUDIO_AVAILABLE:
        return None

    t = np.linspace(
        0,
        duration,
        int(sample_rate * duration),
        endpoint=False
    )

    wave = (
        np.sin(
            2 * np.pi * frequency * t
        ) * 0.3
    )

    wave = (
        wave * 32767
    ).astype(np.int16)

    buffer = io.BytesIO()

    wavfile.write(
        buffer,
        sample_rate,
        wave
    )

    buffer.seek(0)

    return buffer


def typewriter_click():
    return generate_beep(
        frequency=2000,
        duration=0.05
    )


def success_chime():

    if not AUDIO_AVAILABLE:
        return None

    sample_rate = 22050
    duration = 0.5

    t = np.linspace(
        0,
        duration,
        int(sample_rate * duration),
        endpoint=False
    )

    freq_progression = np.concatenate([
        np.full(len(t) // 3, 262),
        np.full(len(t) // 3, 330),
        np.full(
            len(t) - 2 * (len(t) // 3),
            392
        ),
    ])

    wave = (
        np.sin(
            2
            * np.pi
            * freq_progression[:len(t)]
            * t
        )
        * 0.3
    )

    wave = (
        wave * 32767
    ).astype(np.int16)

    buffer = io.BytesIO()

    wavfile.write(
        buffer,
        sample_rate,
        wave
    )

    buffer.seek(0)

    return buffer


# ============================================================
# AUTOPLAY AUDIO
# ============================================================

def autoplay_audio(audio_buffer):

    if audio_buffer is None:
        return

    audio_buffer.seek(0)

    audio_bytes = audio_buffer.read()

    audio_base64 = (
        base64.b64encode(audio_bytes)
        .decode("utf-8")
    )

    st.markdown(
        f"""
        <audio autoplay>
            <source
                src="data:audio/wav;base64,{audio_base64}"
                type="audio/wav"
            >
        </audio>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Who Is the Mole?",
    page_icon="🧟",
    layout="wide"
)


# ============================================================
# NOIR AESTHETIC
# ============================================================

st.markdown(
    """
    <link
        href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Crimson+Text:ital@0;1&display=swap"
        rel="stylesheet"
    >

    <style>

    /* ========================================================
       MAIN APP
       ======================================================== */

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
        font-family: 'Crimson Text', serif;
    }


    /* ========================================================
       HEADINGS
       ======================================================== */

    h1 {
        color: #d4af37;

        font-family:
            'JetBrains Mono',
            monospace;

        font-size: 2.5rem;

        text-shadow:
            0 0 10px
            rgba(212, 175, 55, 0.5);

        letter-spacing: 3px;
    }

    h2,
    h3 {
        color: #f39c12;

        font-family:
            'JetBrains Mono',
            monospace;

        text-shadow:
            0 0 8px
            rgba(243, 156, 18, 0.4);
    }


    /* ========================================================
       TABS
       ======================================================== */

    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: #3d2860;

        border-radius:
            8px 8px 0 0;

        padding:
            10px 18px;

        color: #c9a961;

        font-family:
            'JetBrains Mono',
            monospace;

        border:
            1px solid
            #5a3d8a;
    }

    .stTabs [aria-selected="true"] {
        background-color:
            #5a3d8a !important;

        color:
            #d4af37 !important;

        border:
            1px solid
            #d4af37;
    }


    /* ========================================================
       EXPANDERS
       ======================================================== */

    div[data-testid="stExpander"] {
        border:
            1px solid
            #5a3d8a;

        border-radius:
            10px;

        background-color:
            #2d1f42;
    }


    /* ========================================================
       METRICS
       ======================================================== */

    div[data-testid="stMetricValue"] {
        color:
            #f39c12;

        font-size:
            1.8rem;

        font-family:
            'JetBrains Mono',
            monospace;
    }


    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button {
        background-color:
            #5a3d8a;

        color:
            #d4af37;

        border-radius:
            8px;

        border:
            1.5px solid
            #d4af37;

        font-family:
            'JetBrains Mono',
            monospace;

        font-weight:
            bold;

        box-shadow:
            0 0 8px
            rgba(212, 175, 55, 0.3);

        transition:
            all 0.2s ease;
    }

    .stButton > button:hover {
        background-color:
            #d4af37;

        color:
            #1a0f2e;

        box-shadow:
            0 0 15px
            rgba(212, 175, 55, 0.8);
    }


    /* ========================================================
       STORY / CASE FILE
       ======================================================== */

    .case-file {
        background:
            rgba(45, 31, 66, 0.85);

        border:
            1px solid
            #5a3d8a;

        border-left:
            4px solid
            #d4af37;

        border-radius:
            8px;

        padding:
            20px;

        margin:
            15px 0;

        box-shadow:
            0 5px 25px
            rgba(0, 0, 0, 0.35);
    }


    /* ========================================================
       BACKGROUND
       ======================================================== */

    .background-section {
        background:
            #2d1f42;

        border:
            1px solid
            #5a3d8a;

        border-radius:
            8px;

        padding:
            16px;

        margin:
            12px 0;

        font-family:
            'JetBrains Mono',
            monospace;
    }

    .background-title {
        color:
            #d4af37;

        font-weight:
            bold;

        margin-bottom:
            12px;

        font-size:
            1rem;

        letter-spacing:
            1px;
    }

    .background-entry {
        color:
            #c9a961;

        padding:
            8px 0;

        border-bottom:
            1px dotted
            #5a3d8a;

        line-height:
            1.5;
    }


    /* ========================================================
       LAB NOTE
       ======================================================== */

    .note-card {
        background:
            #f4ecd8;

        color:
            #3a3226;

        font-family:
            'Kalam',
            cursive;

        padding:
            22px 24px 16px 24px;

        border-radius:
            2px;

        box-shadow:
            0 4px 20px
            rgba(0, 0, 0, 0.7);

        transform:
            rotate(-1deg);

        position:
            relative;

        margin:
            14px 4px;

        line-height:
            1.7;

        font-size:
            1.05rem;
    }

    .note-card::before {
        content:
            "📌";

        position:
            absolute;

        top:
            -16px;

        left:
            22px;

        font-size:
            1.5rem;
    }

    .hint-letter {
        font-size:
            1.6rem;

        font-weight:
            800;

        color:
            #b91c1c;

        text-decoration:
            underline;

        margin-right:
            2px;
    }


    /* ========================================================
       STORAGE RIDDLE
       ======================================================== */

    .riddle-board {
        background-color:
            #10151f;

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

        background-size:
            22px 22px;

        color:
            #e5e7eb;

        font-family:
            'Caveat',
            cursive;

        font-size:
            1.4rem;

        padding:
            24px;

        border-radius:
            8px;

        border:
            2px solid
            #334155;

        line-height:
            1.9;

        margin:
            14px 4px;

        box-shadow:
            0 4px 20px
            rgba(0, 0, 0, 0.7);
    }

    .riddle-line {
        margin:
            2px 0;
    }

    .scratched {
        text-decoration:
            line-through;

        text-decoration-thickness:
            4px;

        text-decoration-color:
            #ef4444;

        color:
            #94a3b8;

        display:
            inline-block;
    }

    .decoy-line {
        color:
            #fbbf24;

        font-style:
            italic;
    }

    .helper-line {
        color:
            #34d399;
    }


    /* ========================================================
       RECEIPT
       ======================================================== */

    .receipt {
        background:
            #fdfdfd;

        color:
            #111;

        font-family:
            'Courier New',
            monospace;

        padding:
            16px 20px;

        border:
            1px dashed
            #999;

        max-width:
            320px;

        margin:
            14px auto;

        box-shadow:
            0 4px 20px
            rgba(0, 0, 0, 0.7);
    }

    .receipt-title {
        text-align:
            center;

        font-weight:
            bold;

        margin-bottom:
            8px;
    }

    .pin-digit {
        display:
            inline-block;

        width:
            28px;

        text-align:
            center;

        border-bottom:
            2px solid
            #333;

        margin:
            0 3px;

        font-weight:
            bold;

        font-size:
            1.1rem;
    }

    .pin-digit.redacted {
        color:
            #bbb;
    }


    /* ========================================================
       DETECTIVE NOTEBOOK
       ======================================================== */

    .notebook {
        background:
            repeating-linear-gradient(
                #21182b,
                #21182b 31px,
                #392b42 32px
            );

        border:
            1px solid
            #705d7d;

        border-radius:
            6px;

        padding:
            22px;

        margin:
            10px 0;

        min-height:
            150px;
    }


    /* ========================================================
       STATEMENT CARD
       ======================================================== */

    .statement-card {
        background:
            #241936;

        border-left:
            4px solid
            #d4af37;

        border-radius:
            6px;

        padding:
            16px;

        margin:
            12px 0;
    }

    .statement-character {
        color:
            #d4af37;

        font-family:
            'JetBrains Mono',
            monospace;

        font-weight:
            bold;

        font-size:
            1rem;
    }

    .statement-question {
        color:
            #9d8ca8;

        font-size:
            .8rem;

        margin-top:
            8px;
    }

    .statement-answer {
        color:
            #f0e7d8;

        font-family:
            'Crimson Text',
            serif;

        font-size:
            1.3rem;

        line-height:
            1.5;

        margin-top:
            8px;
    }


    /* ========================================================
       SUSPECT CARD
       ======================================================== */

    .suspect-card {
        background:
            #3d2860;

        border-left:
            4px solid
            #f39c12;

        padding:
            15px;

        margin:
            8px 0;

        border-radius:
            4px;
    }


    /* ========================================================
       QUOTE
       ======================================================== */

    .quote-box {
        background:
            #1a1024;

        border-left:
            3px solid
            #d4af37;

        padding:
            18px;

        margin:
            12px 0;

        font-family:
            'Crimson Text',
            serif;

        font-size:
            1.35rem;

        line-height:
            1.5;

        color:
            #f0e7d8;
    }


    /* ========================================================
       LOG
       ======================================================== */

    .log-entry {
        font-family:
            'JetBrains Mono',
            monospace;

        font-size:
            0.85rem;

        color:
            #c9a961;

        padding:
            5px 0;

        border-bottom:
            1px dotted
            #5a3d8a;
    }


    /* ========================================================
       CLUE CHIP
       ======================================================== */

    .clue-chip {
        display:
            inline-block;

        padding:
            7px 12px;

        margin:
            4px;

        border:
            1px solid
            #725b7b;

        color:
            #d8c9dc;

        background:
            #201825;

        font-size:
            .75rem;

        border-radius:
            4px;
    }


    /* ========================================================
       FINAL REPORT
       ======================================================== */

    .verdict-box {
        background:
            #21152d;

        border:
            2px solid
            #d4af37;

        border-radius:
            8px;

        padding:
            25px;

        text-align:
            center;

        box-shadow:
            0 0 25px
            rgba(212, 175, 55, 0.2);
    }

    </style>


    <link
        href="https://fonts.googleapis.com/css2?family=Kalam:wght@400;700&family=Caveat:wght@500;700&display=swap"
        rel="stylesheet"
    >
    """,
    unsafe_allow_html=True
)


# ============================================================
# CLUE RENDERERS
# ============================================================

def render_lab_note(lines):

    html = '<div class="note-card">'

    for letter, rest in lines:

        html += (
            f'<div>'
            f'<span class="hint-letter">'
            f'{letter}'
            f'</span>'
            f'{rest}'
            f'</div>'
        )

    html += "</div>"

    return html


def render_riddle_board(lines):

    html = '<div class="riddle-board">'

    for item in lines:

        classes = "riddle-line"

        if item.get("struck"):
            classes += " scratched"

        if item.get("decoy"):
            classes += " decoy-line"

        if item.get("helper"):
            classes += " helper-line"

        html += (
            f'<div class="{classes}">'
            f'{item["text"]}'
            f'</div>'
        )

    html += "</div>"

    return html


def render_receipt(
    job,
    pin_digits,
    redacted
):

    html = '<div class="receipt">'

    html += (
        '<div class="receipt-title">'
        'RESTOCKING LOG — MACHINE #3'
        '</div>'
    )

    html += (
        f"<div>"
        f"Restocked by: <b>{job}</b>"
        f"</div>"
    )

    html += (
        '<div style="margin-top:10px;">'
        'Employee PIN: '
    )

    for digit, is_redacted in zip(
        pin_digits,
        redacted
    ):

        if is_redacted:

            html += (
                '<span class="pin-digit redacted">'
                '?'
                '</span>'
            )

        else:

            html += (
                f'<span class="pin-digit">'
                f'{digit}'
                f'</span>'
            )

    html += "</div></div>"

    return html


# ============================================================
# SESSION STATE
# ============================================================

if "game" not in st.session_state:

    st.session_state.game = GameState()


if "researcher_name" not in st.session_state:

    st.session_state.researcher_name = ""


if "last_room_result" not in st.session_state:

    st.session_state.last_room_result = None


if "last_interrogation" not in st.session_state:

    st.session_state.last_interrogation = None


game = st.session_state.game

name = st.session_state.researcher_name


# ============================================================
# TITLE
# ============================================================

st.title(
    "🧟 WHO IS THE MOLE?"
)

if name:

    st.caption(
        f"Detective Case File: "
        f"{name} | "
        f"{game.actions_remaining} "
        f"Actions Remaining"
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

    st.header(
        "CASE DOSSIER"
    )

    # --------------------------------------------------------
    # DETECTIVE NAME
    # --------------------------------------------------------

    new_name = st.text_input(
        "Detective name",
        value=st.session_state.researcher_name
    )

    st.session_state.researcher_name = new_name

    name = new_name

    if name:

        st.write(
            f"**Detective:** {name}"
        )

    st.divider()

    # --------------------------------------------------------
    # ACTIONS
    # --------------------------------------------------------

    st.subheader(
        "Actions Remaining"
    )

    st.metric(
        "",
        game.actions_remaining
    )

    st.progress(
        game.actions_used / TOTAL_BUDGET
    )

    st.caption(
        f"{game.actions_used} of {TOTAL_BUDGET} actions used"
    )

    st.divider()

    # --------------------------------------------------------
    # INVESTIGATION STATUS
    # --------------------------------------------------------

    st.subheader(
        "Investigation"
    )

    st.write(
        f"🏚️ Scenes searched: "
        f"**{len(game.visited_rooms)}/{len(case.ROOMS)}**"
    )

    statements_count = sum(
        len(statements)
        for statements
        in game.evidence.suspect_statements.values()
    )

    st.write(
        f"🗣️ Statements collected: "
        f"**{statements_count}**"
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

    # --------------------------------------------------------
    # CASE LOG
    # --------------------------------------------------------

    with st.expander(
        "📋 CASE LOG"
    ):

        if game.log:

            for entry in reversed(
                game.log[-10:]
            ):

                st.markdown(
                    f'<div class="log-entry">'
                    f'• {entry}'
                    f'</div>',
                    unsafe_allow_html=True
                )

        else:

            st.write(
                "*No entries yet.*"
            )

    st.divider()

    # --------------------------------------------------------
    # NEW CASE
    # --------------------------------------------------------

    if st.button(
        "🔄 START NEW CASE",
        use_container_width=True
    ):

        st.session_state.game = GameState()

        st.session_state.last_room_result = None

        st.session_state.last_interrogation = None

        st.rerun()


# ============================================================
# CASE INTRO
# ============================================================

st.markdown(
    '<div class="case-file">',
    unsafe_allow_html=True
)

st.markdown(
    case.CASE_INTRO
)

st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# END OF GAME
# ============================================================

if game.game_over:

    st.divider()

    if game.result == "PERFECT":

        autoplay_audio(
            success_chime()
        )

        st.markdown(
            """
            <div class="verdict-box">

            <h1>CASE SOLVED</h1>

            <h2>PERFECT DETECTION</h2>

            <p>
            You identified the Mole and built a strong
            chain of evidence.
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )

    elif game.result in (
        "WIN",
        "LUCKY_WIN"
    ):

        autoplay_audio(
            success_chime()
        )

        st.success(
            f"✅ CASE CLOSED — "
            f"{game.accused} was the Mole."
        )

        if game.result == "LUCKY_WIN":

            st.info(
                "You got the right suspect, "
                "but your evidence trail was thin."
            )

    else:

        st.error(
            f"❌ CASE FAILED — "
            f"{game.accused} was not the Mole."
        )

        st.warning(
            f"The real Mole was **{case.MOLE}**."
        )

    # --------------------------------------------------------
    # FINAL REPORT
    # --------------------------------------------------------

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

        statements_count = sum(
            len(v)
            for v in
            game.evidence.suspect_statements.values()
        )

        st.metric(
            "Statements Collected",
            statements_count
        )

    st.divider()

    st.subheader(
        "Your Accusation"
    )

    st.write(
        f"**Suspect:** {game.accused}"
    )

    st.write(
        f"**Result:** {game.result}"
    )

    st.divider()

    st.subheader(
        "Your Detective Notes"
    )

    if game.evidence.notes:

        for index, note in enumerate(
            game.evidence.notes,
            start=1
        ):

            st.markdown(
                f"""
                <div class="notebook">
                    <b>NOTE {index}</b><br><br>
                    {note}
                </div>
                """,
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
    tab_accuse
) = st.tabs(
    [
        "📋 BACKGROUND",
        "📓 DETECTIVE NOTEBOOK",
        "🏚️ CRIME SCENES",
        "🗣️ INTERROGATIONS",
        "⚖️ ACCUSATION"
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
        "Pay attention to times, locations and who had access "
        "to what."
    )

    for section, section_data in case.BACKGROUND.items():

        st.markdown(
            '<div class="background-section">',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div class="background-title">'
            f'{section}'
            f'</div>',
            unsafe_allow_html=True
        )

        if "entries" in section_data:

            for label, text in section_data["entries"]:

                st.markdown(
                    f"""
                    <div class="background-entry">
                        <strong>{label}</strong>
                        &nbsp; {text}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        if "notes" in section_data:

            for note in section_data["notes"]:

                st.markdown(
                    f"""
                    <div class="background-entry">
                        • {note}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
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
    # PHYSICAL CLUES
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
            "🥤 Cafeteria restocking receipt"
    }

    if game.evidence.clues_found:

        for clue in game.evidence.clues_found:

            st.markdown(
                f'<span class="clue-chip">'
                f'✓ {clue_names.get(clue, clue)}'
                f'</span>',
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

    if game.evidence.suspect_statements:

        for character in case.CHARACTERS:

            statements = (
                game.evidence.suspect_statements
                .get(character, {})
            )

            if not statements:
                continue

            profile = case.PROFILES[character]

            with st.expander(
                f"🧑 {character} — "
                f"{profile['role']}"
            ):

                for question_key, statement in statements.items():

                    st.markdown(
                        f"""
                        <div class="statement-card">

                            <div class="statement-character">
                                {character}
                            </div>

                            <div class="statement-question">
                                Q: {case.QUESTION_BANK[question_key]}
                            </div>

                            <div class="statement-answer">
                                “{statement['answer']}”
                            </div>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

    else:

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
            "Example: Zephyr says he stayed in Storage "
            "at 11:50, but the cafeteria receipt says..."
        ),
        height=120,
        key="detective_note"
    )

    if st.button(
        "✍️ ADD TO NOTEBOOK",
        use_container_width=True
    ):

        if game.add_note(note):

            st.success(
                "Added to your detective notebook."
            )

            st.rerun()

        else:

            st.warning(
                "Write something first."
            )

    if game.evidence.notes:

        st.divider()

        st.subheader(
            "Notebook Entries"
        )

        for index, saved_note in enumerate(
            game.evidence.notes,
            start=1
        ):

            st.markdown(
                f"""
                <div class="notebook">

                    <strong>
                        NOTE {index}
                    </strong>

                    <br><br>

                    {saved_note}

                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# CRIME SCENES TAB
# ============================================================

with tab_rooms:

    st.subheader(
        "🏚️ Crime Scenes"
    )

    st.write(
        f"You have **{game.actions_remaining} actions** remaining."
    )

    # --------------------------------------------------------
    # THREE ROOMS
    # --------------------------------------------------------

    cols = st.columns(3)

    for col, room in zip(
        cols,
        case.ROOMS
    ):

        with col:

            st.markdown(
                f"### {room}"
            )

            room_descriptions = {
                "Laboratory":
                    "The centrifuge room where the incident began.",

                "Storage":
                    "Shelves, inventory sheets and the ventilation panel.",

                "Cafeteria":
                    "A vending machine, a restocking cart and one suspicious receipt."
            }

            st.caption(
                room_descriptions.get(
                    room,
                    "A location inside the facility."
                )
            )

            # ------------------------------------------------
            # ALREADY VISITED
            # ------------------------------------------------

            if room in game.visited_rooms:

                st.success(
                    "✓ Location investigated"
                )

                clue = None

                # Recover clue from the relevant case data
                if room == "Laboratory":

                    clue = case.get_lab_clue()

                    st.markdown(
                        f"**{clue['title']}**"
                    )

                    st.markdown(
                        render_lab_note(
                            clue["lines"]
                        ),
                        unsafe_allow_html=True
                    )

                    st.caption(
                        "The first letters may be worth remembering."
                    )

                elif room == "Storage":

                    clue = case.get_storage_clue()

                    st.markdown(
                        f"**{clue['title']}**"
                    )

                    st.markdown(
                        render_riddle_board(
                            clue["lines"]
                        ),
                        unsafe_allow_html=True
                    )

                    st.caption(
                        "Someone clearly didn't want the original "
                        "inventory count left intact."
                    )

                elif room == "Cafeteria":

                    clue = case.get_cafeteria_clue()

                    st.markdown(
                        f"**{clue['title']}**"
                    )

                    st.markdown(
                        render_receipt(
                            clue["job"],
                            clue["pin_digits"],
                            clue["redacted"]
                        ),
                        unsafe_allow_html=True
                    )

                    st.info(
                        clue["note"]
                    )

                    st.caption(
                        clue["hidden_note"]
                    )

                    # ----------------------------------------
                    # PIN
                    # ----------------------------------------

                    st.divider()

                    st.markdown(
                        "**Crack the Employee PIN**"
                    )

                    if game.pin_cracked:

                        st.success(
                            "🔓 PIN CRACKED"
                        )

                    else:

                        pin_guess = st.text_input(
                            "Enter four digits",
                            max_chars=4,
                            key="pin_guess"
                        )

                        if st.button(
                            "🔓 VERIFY PIN",
                            key="verify_pin"
                        ):

                            result = game.attempt_pin(
                                pin_guess
                            )

                            if result["correct"]:

                                autoplay_audio(
                                    success_chime()
                                )

                                st.success(
                                    result["message"]
                                )

                            else:

                                st.error(
                                    result["message"]
                                )

            # ------------------------------------------------
            # NOT VISITED
            # ------------------------------------------------

            else:

                if st.button(
                    f"🔎 Investigate {room}",
                    key=f"visit_{room}",
                    disabled=not game.can_act(),
                    use_container_width=True
                ):

                    result = game.visit_room(
                        room
                    )

                    if result["success"]:

                        autoplay_audio(
                            typewriter_click()
                        )

                        st.session_state.last_room_result = result

                        st.rerun()

                    else:

                        st.warning(
                            result["message"]
                        )


# ============================================================
# INTERROGATIONS TAB
# ============================================================

with tab_people:

    st.subheader(
        "🗣️ Interrogation Room"
    )

    st.write(
        "Everyone has something to say. "
        "The trick is figuring out whether it matters."
    )

    for character in case.CHARACTERS:

        profile = case.PROFILES[character]

        with st.expander(
            f"🧑 {character} — {profile['role']}"
        ):

            # ------------------------------------------------
            # PROFILE
            # ------------------------------------------------

            st.markdown(
                f"""
                <div class="suspect-card">

                    <strong>
                        {character}
                    </strong>

                    <br>

                    <span style="
                        color:#c9a961;
                        font-size:.8rem;
                    ">
                        {profile['role']}
                        •
                        {profile['location']}
                    </span>

                    <br><br>

                    {profile['description']}

                    <br><br>

                    <i>
                        {profile['personality']}
                    </i>

                </div>
                """,
                unsafe_allow_html=True
            )

            # ------------------------------------------------
            # PREVIOUS QUESTIONS
            # ------------------------------------------------

            asked_questions = game.asked.get(
                character,
                set()
            )

            if asked_questions:

                st.markdown(
                    "**Previous statements:**"
                )

                statements = (
                    game.evidence
                    .suspect_statements
                    .get(character, {})
                )

                for question_key in asked_questions:

                    statement = statements.get(
                        question_key
                    )

                    if not statement:
                        continue

                    st.markdown(
                        f"""
                        <div class="statement-card">

                            <div class="statement-question">
                                Q: {case.QUESTION_BANK[question_key]}
                            </div>

                            <div class="statement-answer">
                                “{statement['answer']}”
                            </div>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            # ------------------------------------------------
            # AVAILABLE QUESTIONS
            # ------------------------------------------------

            available_questions = [
                key
                for key in case.QUESTION_BANK
                if key not in asked_questions
            ]

            if available_questions:

                st.markdown(
                    "**Ask another question:**"
                )

                q_key = st.selectbox(
                    "Question",
                    options=available_questions,
                    format_func=lambda key:
                        case.QUESTION_BANK[key],
                    key=f"question_{character}"
                )

                if st.button(
                    f"Ask {character}",
                    key=f"ask_{character}",
                    disabled=not game.can_act(),
                    use_container_width=True
                ):

                    result = game.ask_question(
                        character,
                        q_key
                    )

                    if result["success"]:

                        autoplay_audio(
                            typewriter_click()
                        )

                        st.session_state.last_interrogation = result

                        st.rerun()

                    else:

                        st.warning(
                            result["message"]
                        )

            else:

                st.info(
                    "You have asked this person every available question."
                )


# ============================================================
# ACCUSATION TAB
# ============================================================

with tab_accuse:

    st.subheader(
        "⚖️ Final Accusation"
    )

    st.warning(
        "Once you submit an accusation, the investigation ends."
    )

    st.write(
        "Don't accuse someone simply because they lied. "
        "Accuse the person whose lies connect to the actual incident."
    )

    # --------------------------------------------------------
    # SUSPECT
    # --------------------------------------------------------

    suspect = st.selectbox(
        "Who is the Mole?",
        case.CHARACTERS,
        key="final_suspect"
    )

    st.divider()

    # --------------------------------------------------------
    # EVIDENCE SELECTION
    # --------------------------------------------------------

    st.subheader(
        "What convinced you?"
    )

    evidence_options = []

    # Physical clues
    clue_labels = {
        "lab_acrostic":
            "🧪 Laboratory note",

        "storage_riddle":
            "📦 Storage inventory board",

        "cafeteria_pin":
            "🥤 Cafeteria restocking receipt"
    }

    for clue in game.evidence.clues_found:

        evidence_options.append(
            clue_labels.get(
                clue,
                clue
            )
        )

    # Statements
    for character, statements in (
        game.evidence.suspect_statements.items()
    ):

        for question_key in statements:

            evidence_options.append(
                f"🗣️ {character}: "
                f"{case.QUESTION_BANK[question_key]}"
            )

    if evidence_options:

        selected_evidence = st.multiselect(
            "Select the clues/statements "
            "that support your accusation",
            evidence_options,
            key="final_evidence"
        )

    else:

        selected_evidence = []

        st.info(
            "You haven't collected any evidence yet."
        )

    st.divider()

    # --------------------------------------------------------
    # REASONING
    # --------------------------------------------------------

    st.subheader(
        "Your Reasoning"
    )

    reasoning = st.text_area(
        "Build your case",
        placeholder=(
            "Example:\n\n"
            "Zephyr claimed he stayed in Storage all night. "
            "However, the ventilation override happened at 11:50 "
            "and only the Supply Coordinator and Maintenance Chief "
            "had access. The Maintenance Chief was off shift..."
        ),
        height=180,
        key="final_reasoning"
    )

    st.divider()

    # --------------------------------------------------------
    # SUBMIT
    # --------------------------------------------------------

    if st.button(
        "🔨 SUBMIT FINAL ACCUSATION",
        type="primary",
        use_container_width=True,
        disabled=not game.can_act()
    ):

        if not selected_evidence:

            st.error(
                "A detective needs evidence. "
                "Select at least one piece of evidence."
            )

        elif not reasoning.strip():

            st.error(
                "Explain your reasoning before closing the case."
            )

        else:

            result = game.make_accusation(
                suspect,
                selected_evidence
            )

            if result["success"]:

                st.rerun()


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
