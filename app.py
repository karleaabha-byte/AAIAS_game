"""
app.py
Zom-Mole Hunter
Streamlit noir detective game
"""

import html
import streamlit as st
import case

from game import GameState, TOTAL_BUDGET, ROOMS


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Zom-Mole Hunter",
    page_icon="🧟",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# SESSION STATE
# ============================================================

if "game" not in st.session_state:
    st.session_state.game = GameState()

if "detective_name" not in st.session_state:
    st.session_state.detective_name = ""

if "case_started" not in st.session_state:
    st.session_state.case_started = False

if "notes" not in st.session_state:
    st.session_state.notes = []


game = st.session_state.game


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at top,
                #202020 0%,
                #101010 45%,
                #070707 100%
            );
        color: #e8e8e8;
    }

    .main-title {
        text-align: center;
        font-size: 4rem;
        font-weight: 900;
        letter-spacing: 5px;
        margin-top: 30px;
        margin-bottom: 5px;
        color: #f1f1f1;
        text-shadow: 0 0 20px rgba(255,255,255,0.12);
    }

    .subtitle {
        text-align: center;
        color: #999;
        font-size: 1.1rem;
        letter-spacing: 3px;
        margin-bottom: 35px;
    }

    .story-box {
        background: rgba(20,20,20,0.85);
        border: 1px solid #444;
        border-radius: 8px;
        padding: 30px;
        line-height: 1.8;
        box-shadow: 0 0 25px rgba(0,0,0,0.5);
    }

    .section-title {
        font-size: 1.5rem;
        letter-spacing: 2px;
        font-weight: 700;
        margin-top: 15px;
        margin-bottom: 15px;
    }

    .clue-box {
        background: #151515;
        border: 1px solid #444;
        border-radius: 6px;
        padding: 24px;
        margin: 12px 0;
    }

    .riddle-line {
        font-family: Georgia, serif;
        font-style: italic;
        color: #d0d0d0;
        font-size: 1.1rem;
        padding: 7px 0;
    }

    .pin-display {
        font-family: monospace;
        font-size: 2.5rem;
        letter-spacing: 14px;
        text-align: center;
        padding: 20px;
        border: 1px solid #555;
        background: #0b0b0b;
        margin: 20px 0;
    }

    .unlock-box {
        border: 1px solid #777;
        background: #181818;
        padding: 20px;
        border-radius: 6px;
        margin-top: 20px;
    }

    .locked-box {
        border: 1px dashed #555;
        background: #111;
        padding: 25px;
        text-align: center;
        color: #888;
        border-radius: 6px;
    }

    .log-entry {
        border-left: 2px solid #666;
        padding-left: 10px;
        margin-bottom: 10px;
        color: #aaa;
        font-size: 0.9rem;
    }

    .win-box {
        border: 1px solid #777;
        padding: 35px;
        text-align: center;
        background: #151515;
        border-radius: 8px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HELPERS
# ============================================================

def safe_text(text):
    return html.escape(str(text))


def reset_game():

    st.session_state.game = GameState()

    st.session_state.detective_name = ""

    st.session_state.case_started = False

    st.session_state.notes = []


def render_actions():

    st.sidebar.markdown("## 🕵️ CASE STATUS")

    st.sidebar.metric(
        "Actions Remaining",
        game.actions_remaining
    )

    st.sidebar.progress(
        min(
            game.actions_used / TOTAL_BUDGET,
            1.0
        )
    )

    if game.pin_cracked:

        st.sidebar.success(
            "🔓 Interrogations unlocked"
        )

    else:

        st.sidebar.warning(
            "🔒 Interrogations locked"
        )

    st.sidebar.markdown("---")

    st.sidebar.markdown("### INVESTIGATED")

    for room in ROOMS:

        if room in game.visited_rooms:
            st.sidebar.write(f"✓ {room}")
        else:
            st.sidebar.write(f"○ {room}")

    st.sidebar.markdown("---")

    st.sidebar.markdown("### CASE LOG")

    for entry in reversed(game.log[-8:]):

        st.sidebar.markdown(
            f'<div class="log-entry">{safe_text(entry)}</div>',
            unsafe_allow_html=True
        )

    st.sidebar.markdown("---")

    if st.sidebar.button(
        "↻ RESTART CASE",
        use_container_width=True
    ):

        reset_game()
        st.rerun()


def render_lab(clue):

    st.markdown(
        "### THE LABORATORY NOTE"
    )

    st.markdown(
        '<div class="clue-box">',
        unsafe_allow_html=True
    )

    for line in clue["lines"]:

        st.write(line)

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


def render_storage(clue):

    st.markdown(
        "### THE STORAGE RIDDLE"
    )

    st.markdown(
        '<div class="clue-box">',
        unsafe_allow_html=True
    )

    for line in clue["riddle"]:

        st.markdown(
            f'<div class="riddle-line">{safe_text(line)}</div>',
            unsafe_allow_html=True
        )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


def render_cafeteria(clue):

    st.markdown(
        "### RESTOCKING LOG — MACHINE #3"
    )

    st.markdown(
        '<div class="clue-box">',
        unsafe_allow_html=True
    )

    st.markdown(
        "**Restocked by:** SUPPLY RESTOCK"
    )

    st.markdown(
        "### Employee PIN"
    )

    pin_display = ""

    for digit, redacted in zip(
        clue["pin_digits"],
        clue["redacted"]
    ):

        if redacted:
            pin_display += "?"
        else:
            pin_display += digit

    st.markdown(
        f'<div class="pin-display">{pin_display}</div>',
        unsafe_allow_html=True
    )

    st.write(clue["note"])

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


def render_end_game():

    st.markdown(
        '<div class="main-title">CASE CLOSED</div>',
        unsafe_allow_html=True
    )

    if game.result == "win":

        st.markdown(
            """
            <div class="win-box">

            <h2>🧟 MOLE IDENTIFIED</h2>

            <p>
            Your accusation was correct.
            </p>

            <p>
            The Supply Coordinator was the mole.
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            """
            <div class="win-box">

            <h2>CASE FAILED</h2>

            <p>
            Your accusation was incorrect.
            </p>

            <p>
            The real mole escaped the investigation.
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    st.markdown(
        f"**Detective:** {st.session_state.detective_name}"
    )

    st.markdown(
        f"**Your accusation:** {game.accused}"
    )

    st.markdown(
        f"**PIN attempts:** {game.pin_attempts}"
    )

    st.markdown(
        f"**Actions used:** {game.actions_used}/{TOTAL_BUDGET}"
    )

    if st.button(
        "START A NEW CASE",
        use_container_width=True
    ):

        reset_game()
        st.rerun()


# ============================================================
# START / STORY TAB
# ============================================================

if not st.session_state.case_started:

    st.markdown(
        '<div class="main-title">ZOM-MOLE HUNTER</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">A NOIR DETECTIVE INVESTIGATION</div>',
        unsafe_allow_html=True
    )

    intro_tab, case_tab = st.tabs(
        [
            "🧟 ZOM-MOLE HUNTER",
            "📁 THE CASE"
        ]
    )

    with intro_tab:

        st.markdown(
            """
            <div class="story-box">

            <h2>THE NIGHT SHIFT INCIDENT</h2>

            <p>
            <b>12:18 AM.</b>
            </p>

            <p>
            The research facility should have been asleep.
            </p>

            <p>
            Instead, emergency lights are flashing, the laboratory
            alarm is screaming, and an entire cabinet of experimental
            materials has vanished.
            </p>

            <p>
            At first, security believed it was an equipment failure.
            </p>

            <p>
            Then they found the broken vial.
            </p>

            <p>
            Then they found the ventilation panel.
            </p>

            <p>
            Then someone noticed that three minutes of corridor
            camera footage had disappeared.
            </p>

            <p>
            And finally, they discovered something much worse:
            </p>

            <p>
            <b>
            Someone inside the facility knew exactly where the
            blind spots were.
            </b>
            </p>

            <p>
            Five people were still inside the building that night.
            </p>

            <p>
            One of them is lying.
            </p>

            <p>
            Possibly more than one.
            </p>

            <p>
            Your job is not simply to find someone who lied.
            </p>

            <p>
            Your job is to figure out
            <b>which lie matters.</b>
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")

        st.markdown(
            "## ENTER YOUR DETECTIVE NAME"
        )

        name = st.text_input(
            "Detective name",
            value=st.session_state.detective_name,
            placeholder="Enter your name...",
            label_visibility="collapsed"
        )

        if st.button(
            "ENTER THE CASE →",
            use_container_width=True
        ):

            if not name.strip():

                st.error(
                    "Please enter a detective name."
                )

            else:

                st.session_state.detective_name = name.strip()

                st.session_state.case_started = True

                st.rerun()

    with case_tab:

        st.markdown(
            "## CASE FILE"

        )

        st.markdown(
            """
            ### THE INCIDENT

            **00:10** — Emergency alarm activated.

            **00:12** — Raven discovered inside the Laboratory.

            **00:14** — Six experimental filter cartridges reported missing.

            **00:17** — Storage ventilation panel discovered closed.

            **00:18** — Three minutes of corridor footage missing.

            ---

            ### THE STRANGE PART

            **11:45 PM** — Raven says she began working alone.

            **11:49 PM** — Corridor camera stopped recording.

            **11:50 PM** — Storage ventilation override registered.

            **11:50 PM** — Cafeteria vending machine began restocking.

            **11:52 PM** — Laboratory centrifuge manually interrupted.

            **12:03 AM** — Ventilation panel closed again.

            ---

            ### WHO COULD OPEN THE VENT?

            Only the **Supply Coordinator** and
            **Maintenance Chief** were authorized to use the
            Storage ventilation override.

            The Maintenance Chief was off-site.

            The Supply Coordinator was scheduled for the entire
            night shift.

            But authorization alone does not prove who actually
            used the system.

            **That is for you to determine.**
            """
        )

    st.stop()


# ============================================================
# GAME STARTED
# ============================================================

render_actions()


if game.game_over:

    render_end_game()
    st.stop()


st.markdown(
    '<div class="main-title">ZOM-MOLE HUNTER</div>',
    unsafe_allow_html=True
)

st.markdown(
    f'<div class="subtitle">'
    f'DETECTIVE {safe_text(st.session_state.detective_name).upper()}'
    f'</div>',
    unsafe_allow_html=True
)


# ============================================================
# MAIN GAME TABS
# ============================================================

background_tab, scenes_tab, interrogation_tab, accusation_tab = st.tabs(
    [
        "📁 BACKGROUND",
        "🔎 CRIME SCENES",
        "💬 INTERROGATIONS",
        "⚖️ ACCUSATION"
    ]
)


# ============================================================
# BACKGROUND
# ============================================================

with background_tab:

    st.markdown(
        "## CASE FILE"
    )

    st.markdown(
        """
        Five people remained inside the facility.

        Someone manipulated the night-shift events.

        Someone knew about the facility's blind spots.

        Someone may have lied about where they were.

        Your task is to connect the evidence yourself.
        """
    )

    st.markdown("---")

    for section, data in case.BACKGROUND.items():

        st.markdown(
            f"### {section}"
        )

        for timestamp, text in data["entries"]:

            st.markdown(
                f"**{timestamp}** — {text}"
            )


# ============================================================
# CRIME SCENES
# ============================================================

with scenes_tab:

    st.markdown(
        "## CRIME SCENES"
    )

    st.caption(
        f"{game.actions_remaining} actions remaining."
    )

    for room in ROOMS:

        st.markdown("---")

        if room in game.visited_rooms:

            st.markdown(
                f"### ✓ {room.upper()}"
            )

            clue = game.visited_rooms[room]

            if room == "Laboratory":

                render_lab(clue)

            elif room == "Storage":

                render_storage(clue)

            elif room == "Cafeteria":

                render_cafeteria(clue)

        else:

            st.markdown(
                f"### {room.upper()}"
            )

            if st.button(
                f"INVESTIGATE {room.upper()}",
                key=f"visit_{room}",
                use_container_width=True,
                disabled=not game.can_act()
            ):

                success, payload = game.visit_room(room)

                if success:

                    st.rerun()

                else:

                    st.error(payload)


    # ========================================================
    # PIN CRACKING
    # ========================================================

    if "Cafeteria" in game.visited_rooms:

        st.markdown("---")

        st.markdown(
            "## 🔐 CRACK THE EMPLOYEE PIN"
        )

        if game.pin_cracked:

            st.markdown(
                """
                <div class="unlock-box">

                <h3>🔓 ACCESS GRANTED</h3>

                <p>
                The PIN has been accepted.
                </p>

                <p>
                A restricted employee record has been unlocked.
                </p>

                <p>
                <b>INTERROGATION SYSTEM: ONLINE</b>
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.info(
                "Every PIN attempt costs 1 action."
            )

            pin_guess = st.text_input(
                "Enter 4-digit PIN",
                max_chars=4,
                placeholder="____",
                key="pin_guess"
            )

            if st.button(
                "CRACK PIN",
                use_container_width=True,
                disabled=not game.can_act()
            ):

                success, result = game.attempt_pin(
                    pin_guess
                )

                if success:

                    st.success(
                        "🔓 PIN CRACKED — INTERROGATIONS UNLOCKED."
                    )

                else:

                    st.error(
                        "❌ Incorrect PIN. "
                        f"That attempt used 1 action. "
                        f"{game.actions_remaining} actions remain."
                    )

                st.rerun()


# ============================================================
# INTERROGATIONS
# ============================================================

with interrogation_tab:

    st.markdown(
        "## INTERROGATIONS"
    )

    if not game.pin_cracked:

        st.markdown(
            """
            <div class="locked-box">

            <h2>🔒 INTERROGATION SYSTEM LOCKED</h2>

            <p>
            Restricted personnel records must be accessed first.
            </p>

            <p>
            Investigate the <b>Cafeteria</b> and crack the
            employee PIN to unlock interrogations.
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.success(
            "🔓 Interrogation system unlocked."
        )

        st.caption(
            "Each interrogation costs 1 action."
        )

        for character in case.CHARACTERS:

            st.markdown("---")

            profile = case.get_profile(character)

            st.markdown(
                f"### {character.upper()}"
            )

            st.write(
                f"**{profile['role']}** — "
                f"{profile['description']}"
            )

            if character in game.asked:

                previous = game.asked[character]

                st.markdown(
                    "**Interview recorded:**"
                )

                st.info(
                    previous["answer"]
                )

                continue

            question = st.selectbox(
                "Choose a question",
                options=list(
                    case.QUESTION_BANK.keys()
                ),
                format_func=lambda x: case.QUESTION_BANK[x],
                key=f"question_{character}"
            )

            if st.button(
                f"QUESTION {character.upper()}",
                key=f"ask_{character}",
                use_container_width=True,
                disabled=not game.can_act()
            ):

                success, answer = game.ask_question(
                    character,
                    question
                )

                if success:

                    st.success(answer)

                else:

                    st.error(answer)

                st.rerun()


# ============================================================
# ACCUSATION
# ============================================================

with accusation_tab:

    st.markdown(
        "## FINAL ACCUSATION"
    )

    st.write(
        "You have one chance to name the mole."
    )

    st.warning(
        "Think carefully. Your accusation ends the case."
    )

    accused = st.selectbox(
        "Who is the mole?",
        case.CHARACTERS
    )

    reasoning = st.text_area(
        "Why do you think they are the mole?",
        placeholder=(
            "Explain the evidence and contradictions "
            "that led you to this conclusion..."
        )
    )

    if st.button(
        "⚖️ MAKE FINAL ACCUSATION",
        use_container_width=True
    ):

        if not reasoning.strip():

            st.error(
                "Give your reasoning before making the accusation."
            )

        else:

            success, result = game.make_accusation(
                accused
            )

            if success:

                st.rerun()

            else:

                st.error(result)
