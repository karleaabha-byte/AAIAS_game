"""
app.py - Streamlit front-end for "Who Is the Mole?" — NOIR EDITION

Run with:
    streamlit run app.py
"""

import streamlit as st
import io
import base64

import case
import optimal_path
from game import GameState, TOTAL_BUDGET


# ============================================================
# INLINE SOUND GENERATION
# ============================================================

try:
    import numpy as np
    from scipy.io import wavfile

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
        np.sin(2 * np.pi * frequency * t)
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
    """
    Play audio automatically without displaying
    Streamlit's audio player or play button.
    """

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
       CAFETERIA RECEIPT
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
       EVIDENCE BOARD
       ======================================================== */

    .evidence-grid {

        background:
            #2d1f42;

        border:
            2px solid
            #d4af37;

        border-radius:
            8px;

        padding:
            16px;

        margin:
            10px 0;

        box-shadow:
            0 0 15px
            rgba(212, 175, 55, 0.3);
    }


    .suspect-card {

        background:
            #3d2860;

        border-left:
            4px solid
            #f39c12;

        padding:
            12px;

        margin:
            8px 0;

        border-radius:
            4px;

        font-family:
            'JetBrains Mono',
            monospace;
    }


    .guilt-bar {

        background:
            #1a0f2e;

        border-radius:
            4px;

        height:
            20px;

        overflow:
            hidden;

        margin:
            8px 0;
    }


    .guilt-fill {

        height:
            100%;

        background:
            linear-gradient(
                90deg,
                #f39c12 0%,
                #d4af37 50%,
                #e74c3c 100%
            );

        transition:
            width 0.3s ease;
    }


    .contradiction-alert {

        background:
            #8b0000;

        border-left:
            4px solid
            #ff6b6b;

        color:
            #ffb3b3;

        padding:
            12px;

        margin:
            10px 0;

        border-radius:
            4px;

        font-family:
            'JetBrains Mono',
            monospace;
    }


    /* ========================================================
       CASE LOG
       ======================================================== */

    .log-entry {

        font-family:
            'JetBrains Mono',
            monospace;

        font-size:
            0.9rem;

        color:
            #c9a961;

        padding:
            4px 0;

        border-bottom:
            1px dotted
            #5a3d8a;

        animation:
            typewrite
            0.2s ease-in;
    }


    @keyframes typewrite {

        from {
            opacity: 0;
            transform: translateX(-10px);
        }

        to {
            opacity: 1;
            transform: translateX(0);
        }
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
            12px;

        margin:
            10px 0;

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
            8px;
    }


    .background-entry {

        color:
            #c9a961;

        padding:
            4px 0;

        border-bottom:
            1px dotted
            #5a3d8a;
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
# EVIDENCE BOARD
# ============================================================

def render_evidence_board(game):

    html = """
    <div class="evidence-grid">

        <h3 style="
            color: #d4af37;
            margin-top: 0;
        ">
            EVIDENCE BOARD
        </h3>
    """


    # --------------------------------------------------------
    # CONTRADICTIONS
    # --------------------------------------------------------

    if game.evidence.contradictions:

        for contradiction in (
            game.evidence.contradictions
        ):

            html += f"""
            <div class="contradiction-alert">
                🚨 {contradiction["detail"]}
            </div>
            """


    # --------------------------------------------------------
    # SUSPECT CARDS
    # --------------------------------------------------------

    html += """
        <div style="margin-top: 16px;">
    """


    for character in case.CHARACTERS:

        guilt = (
            game.evidence
            .get_guilt_score(character)
        )

        guilt = max(
            0,
            min(
                100,
                int(guilt)
            )
        )

        profile = case.PROFILES[character]

        job = profile.get(
            "job",
            "Unknown"
        )

        location = profile.get(
            "location",
            "Unknown"
        )


        html += f"""
        <div class="suspect-card">

            <div style="
                font-weight: bold;
                color: #d4af37;
                font-size: 1.05rem;
            ">
                {character}
            </div>

            <div style="
                font-size: 0.85rem;
                color: #c9a961;
                margin-top: 4px;
            ">
                {job} • {location}
            </div>

            <div class="guilt-bar">

                <div
                    class="guilt-fill"
                    style="width: {guilt}%;">
                </div>

            </div>

            <div style="
                font-size: 0.8rem;
                color: #f39c12;
            ">
                Suspicion: {guilt}/100
            </div>

        </div>
        """


    html += """
        </div>
    </div>
    """

    return html


# ============================================================
# SESSION STATE
# ============================================================

if "game" not in st.session_state:

    st.session_state.game = GameState()


if "hints_used" not in st.session_state:

    st.session_state.hints_used = 0


if "researcher_name" not in st.session_state:

    st.session_state.researcher_name = ""


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


    if name:

        st.write(
            f"**Detective:** {name}"
        )


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


    # --------------------------------------------------------
    # GLOBAL SUSPICION
    # --------------------------------------------------------

    st.subheader(
        "Suspicion Level"
    )

    st.write(
        f"{game.suspicion}/100"
    )

    st.progress(
        game.suspicion / 100
    )


    # --------------------------------------------------------
    # HINTS
    # --------------------------------------------------------

    HINT_LIMIT = 2

    if not game.game_over:

        if (
            st.session_state.hints_used
            < HINT_LIMIT
        ):

            if st.button(
                f"💡 Get a Hint "
                f"({HINT_LIMIT - st.session_state.hints_used} left)"
            ):

                st.session_state.hints_used += 1

                st.info(
                    optimal_path.get_hint(game)
                )

        else:

            st.caption(
                "*No hints remaining.*"
            )


    st.divider()


    # --------------------------------------------------------
    # NEW CASE
    # --------------------------------------------------------

    if st.button(
        "🔄 START NEW CASE"
    ):

        st.session_state.game = GameState()

        st.session_state.hints_used = 0

        st.rerun()


    # --------------------------------------------------------
    # CASE LOG
    # --------------------------------------------------------

    with st.expander(
        "📋 CASE LOG"
    ):

        if game.log:

            log_html = (
                '<div class="log-entry">'
                + "<br>".join(
                    game.log[-10:]
                )
                + "</div>"
            )

            st.markdown(
                log_html,
                unsafe_allow_html=True
            )

        else:

            st.write(
                "*No entries yet.*"
            )


# ============================================================
# CASE INTRO
# ============================================================

st.markdown(
    case.CASE_INTRO
)


# ============================================================
# END OF GAME
# ============================================================

if game.game_over:

    st.divider()


    if game.result == "win":

        st.success(
            f"✅ CASE CLOSED: "
            f"{game.accused} is the mole."
        )

        autoplay_audio(
            success_chime()
        )

    else:

        st.error(
            f"❌ CASE FAILED: "
            f"{game.accused} was accused, "
            f"but the true mole was "
            f"{case.MOLE}."
        )


    stats = game.get_stats()

    perf = (
        optimal_path
        .evaluate_performance(stats)
    )


    col1, col2 = st.columns(2)


    # --------------------------------------------------------
    # INVESTIGATION REPORT
    # --------------------------------------------------------

    with col1:

        st.subheader(
            "INVESTIGATION REPORT"
        )

        st.write(
            f"- Actions Used: "
            f"**{stats['actions_used']}/12**"
        )

        st.write(
            f"- Final Suspicion: "
            f"**{stats['suspicion']}/100**"
        )

        st.write(
            f"- Mole Sabotages: "
            f"**{stats['sabotage_count']}**"
        )

        st.write(
            f"- Mole Helps: "
            f"**{stats['help_count']}**"
        )

        st.write(
            f"- Lies Detected: "
            f"**{stats['lie_count']}**"
        )

        st.write(
            f"- Contradictions Found: "
            f"**{'Yes' if stats['contradiction_flagged'] else 'No'}**"
        )

        st.write(
            f"- PIN Cracked: "
            f"**{'Yes' if stats['pin_cracked'] else 'No'}**"
        )


    # --------------------------------------------------------
    # VERDICT
    # --------------------------------------------------------

    with col2:

        st.subheader(
            "VERDICT"
        )

        st.markdown(
            f"### {perf['grade']}"
        )

        st.write(
            perf["message"]
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
        "🔍 EVIDENCE",
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
        "Investigation Background"
    )

    st.write(
        "Review the facts established at "
        "the crime scene. Use these to "
        "guide your interrogations."
    )


    for (
        section_key,
        section_data
    ) in case.BACKGROUND.items():

        with st.expander(
            f"📄 {section_data['title']}",
            expanded=True
        ):

            if "entries" in section_data:

                for entry in (
                    section_data["entries"]
                ):

                    st.write(
                        f"• {entry}"
                    )


            if "notes" in section_data:

                for note in (
                    section_data["notes"]
                ):

                    st.write(
                        f"• {note}"
                    )


# ============================================================
# EVIDENCE TAB
# ============================================================

with tab_evidence:

    st.subheader(
        "Detective Board"
    )


    # IMPORTANT:
    # st.html() renders the HTML directly.
    # This prevents the raw <div> problem.

    st.html(
        render_evidence_board(game)
    )


    # --------------------------------------------------------
    # FLAGGED CONTRADICTIONS
    # --------------------------------------------------------

    if game.evidence.contradictions:

        st.divider()

        st.subheader(
            "Flagged Contradictions"
        )

        for contradiction in (
            game.evidence.contradictions
        ):

            st.warning(
                f"⚠️ "
                f"{contradiction['detail']}"
            )


# ============================================================
# CRIME SCENES TAB
# ============================================================

with tab_rooms:

    cols = st.columns(3)


    for (
        col,
        room
    ) in zip(
        cols,
        case.ROOM_INFO.keys()
    ):

        info = case.ROOM_INFO[room]


        with col:

            st.subheader(
                f"{info['emoji']} {room}"
            )

            st.caption(
                info["flavor"]
            )


            # ------------------------------------------------
            # ROOM ALREADY VISITED
            # ------------------------------------------------

            if room in game.visited_rooms:

                clue = game.visited_rooms[room]


                # --------------------------------------------
                # LABORATORY
                # --------------------------------------------

                if room == "Laboratory":

                    st.markdown(
                        render_lab_note(clue),
                        unsafe_allow_html=True
                    )


                # --------------------------------------------
                # STORAGE
                # --------------------------------------------

                elif room == "Storage":

                    st.markdown(
                        render_riddle_board(clue),
                        unsafe_allow_html=True
                    )


                # --------------------------------------------
                # CAFETERIA
                # --------------------------------------------

                elif room == "Cafeteria":

                    st.markdown(
                        render_receipt(
                            clue["job"],
                            clue["pin_digits"],
                            clue["redacted"]
                        ),
                        unsafe_allow_html=True
                    )


                    st.divider()


                    guess = st.text_input(
                        "PIN Guess",
                        key="pin_guess",
                        max_chars=8
                    )


                    if st.button(
                        "Verify PIN",
                        key="check_pin"
                    ):

                        if game.attempt_pin(guess):

                            st.success(
                                "🔓 Correct PIN! "
                                "Supply Coordinator confirmed."
                            )

                            autoplay_audio(
                                success_chime()
                            )

                        else:

                            st.warning(
                                "Incorrect PIN. "
                                "Double-check your digits."
                            )


            # ------------------------------------------------
            # ROOM NOT VISITED
            # ------------------------------------------------

            else:

                if st.button(
                    f"Investigate {room}",
                    key=f"visit_{room}",
                    disabled=not game.can_act()
                ):

                    ok, clue = (
                        game.visit_room(room)
                    )


                    if ok:

                        # Play automatically.
                        autoplay_audio(
                            typewriter_click()
                        )

                        # DO NOT call st.rerun() here.
                        # Streamlit already reruns after
                        # the button interaction.


                    else:

                        st.warning(
                            clue
                        )


# ============================================================
# INTERROGATIONS TAB
# ============================================================

with tab_people:

    question_lookup = dict(
        case.QUESTION_BANK
    )


    for character in case.CHARACTERS:

        with st.expander(
            f"🧑 {character}",
            expanded=(
                character
                not in game.asked
            )
        ):


            # --------------------------------------------
            # ALREADY ASKED
            # --------------------------------------------

            if character in game.asked:

                qa = game.asked[character]


                st.write(
                    f"**Q:** "
                    f"{question_lookup[qa['question']]}"
                )


                st.write(
                    f"**A:** "
                    f"_{qa['answer']}_"
                )


            # --------------------------------------------
            # NOT ASKED
            # --------------------------------------------

            else:

                q_key = st.selectbox(

                    "Question",

                    options=[
                        k
                        for k, _
                        in case.QUESTION_BANK
                    ],

                    format_func=lambda k:
                        question_lookup[k],

                    key=f"qselect_{character}"
                )


                if st.button(
                    f"Ask {character}",
                    key=f"ask_{character}",
                    disabled=not game.can_act()
                ):

                    ok, answer = (
                        game.ask_question(
                            character,
                            q_key
                        )
                    )


                    if ok:

                        # Automatic interrogation sound.
                        autoplay_audio(
                            typewriter_click()
                        )

                        # No explicit rerun here.


                    else:

                        st.warning(
                            answer
                        )


# ============================================================
# ACCUSATION TAB
# ============================================================

with tab_accuse:

    st.warning(
        "🚨 Making an accusation ends "
        "the investigation immediately."
    )


    suspect = st.selectbox(
        "Accusation",
        options=case.CHARACTERS,
        key="accuse_select"
    )


    if st.button(
        "🔨 ACCUSE",
        type="primary"
    ):

        game.make_accusation(
            suspect
        )

        # Let the normal Streamlit rerun happen.


# ============================================================
# OUT OF ACTIONS
# ============================================================

if (
    game.actions_remaining == 0
    and not game.game_over
):

    st.error(
        "⏰ Out of actions! "
        "Make your final accusation."
    )
