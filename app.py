"""
app.py - Streamlit front-end for "Who Is the Mole?"

Run with:
    streamlit run app.py
(Theme colors come from .streamlit/config.toml)
"""
import streamlit as st

import case
import optimal_path
from game import GameState, TOTAL_BUDGET

st.set_page_config(page_title="Who Is the Mole?", page_icon="🧟", layout="wide")

# ---------- one-time CSS polish on top of the dark-blue theme ----------
st.markdown(
    """
    <style>
    .stApp { background: linear-gradient(180deg, #0B1220 0%, #0E1A2E 100%); }
    h1, h2, h3 { color: #93C5FD !important; }
    .stTabs [data-baseweb="tab-list"] { gap: 6px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #131C31;
        border-radius: 8px 8px 0 0;
        padding: 8px 16px;
        color: #93C5FD;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1E3A5F !important;
        color: #E2E8F0 !important;
    }
    div[data-testid="stExpander"] {
        border: 1px solid #1E3A5F;
        border-radius: 10px;
        background-color: #101A2E;
    }
    div[data-testid="stMetricValue"] { color: #60A5FA; }
    .stButton>button {
        background-color: #1D4ED8;
        color: #E2E8F0;
        border-radius: 8px;
        border: 1px solid #3B82F6;
    }
    .stButton>button:hover {
        background-color: #2563EB;
        border: 1px solid #93C5FD;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "game" not in st.session_state:
    st.session_state.game = GameState()
if "hints_used" not in st.session_state:
    st.session_state.hints_used = 0
if "researcher_name" not in st.session_state:
    st.session_state.researcher_name = ""

game = st.session_state.game
name = st.session_state.researcher_name

st.title("🧟 Who Is the Mole?")
if name:
    st.caption(f"Researcher {name} — 9 actions to find the mole before it's too late.")
else:
    st.caption("An adversarial-AI mystery — 9 actions to find the mole before it's too late.")

with st.sidebar:
    st.header("Investigation Status")
    if name:
        st.write(f"🧑‍💼 **Researcher:** {name}")
    st.metric("Actions remaining", game.actions_remaining)
    st.progress(game.actions_used / TOTAL_BUDGET)

    st.write(f"**Suspicion meter:** {game.suspicion}/100")
    st.progress(game.suspicion / 100)

    HINT_LIMIT = 2
    if not game.game_over:
        if st.session_state.hints_used < HINT_LIMIT:
            if st.button(f"💡 Get a hint ({HINT_LIMIT - st.session_state.hints_used} left)"):
                st.session_state.hints_used += 1
                st.info(optimal_path.get_hint(game))
        else:
            st.caption("No hints left — you're on your own now.")

    st.divider()
    if st.button("🔄 New Game"):
        st.session_state.game = GameState()
        st.session_state.hints_used = 0
        st.rerun()

    with st.expander("📜 Case Log"):
        if game.log:
            for entry in game.log:
                st.write(entry)
        else:
            st.write("Nothing logged yet.")

st.markdown(case.CASE_INTRO)

if game.game_over:
    st.divider()
    if game.result == "win":
        st.success(f"✅ You accused **{game.accused}** — correct! The mole is caught.")
    else:
        st.error(f"❌ You accused **{game.accused}** — wrong! The real mole, {case.MOLE}, gets away.")

    stats = game.get_stats()
    perf = optimal_path.evaluate_performance(stats)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Case Report")
        st.write(f"- Actions used: **{stats['actions_used']}**")
        st.write(f"- Final suspicion: **{stats['suspicion']}/100**")
        st.write(f"- Sabotage actions by the mole: **{stats['sabotage_count']}**")
        st.write(f"- Help actions by the mole: **{stats['help_count']}**")
        st.write(f"- Times the mole lied: **{stats['lie_count']}**")
        st.write(f"- Contradiction caught: **{'Yes' if stats['contradiction_flagged'] else 'No'}**")
        st.write(f"- PIN cracked: **{'Yes' if stats['pin_cracked'] else 'No'}**")
    with col2:
        st.subheader("Performance")
        st.markdown(f"### Grade: {perf['grade']}")
        st.write(perf["message"])

    st.stop()

tab_researcher, tab_rooms, tab_people, tab_accuse = st.tabs(
    ["🧑‍💼 Researcher", "🏚️ Investigate Rooms", "🗣️ Question Suspects", "⚖️ Make an Accusation"]
)

with tab_researcher:
    st.subheader("Sign in as the Researcher")
    entered = st.text_input("Your name", value=st.session_state.researcher_name, placeholder="e.g. Dr. Amara Osei")
    if st.button("Save name"):
        st.session_state.researcher_name = entered.strip()
        st.rerun()
    if st.session_state.researcher_name:
        st.success(f"Logged in as Researcher {st.session_state.researcher_name}.")
    else:
        st.info("Enter a name so the case log can address you properly (purely cosmetic — you can still play without it).")

    st.divider()
    st.subheader("Suspect Directory")
    for character in case.CHARACTERS:
        st.write(f"- **{character}** — {case.PROFILES[character]['job']}")

with tab_rooms:
    cols = st.columns(3)
    for col, room in zip(cols, case.ROOM_INFO.keys()):
        info = case.ROOM_INFO[room]
        with col:
            st.subheader(f"{info['emoji']} {room}")
            st.caption(info["flavor"])
            if room in game.visited_rooms:
                st.markdown(game.visited_rooms[room])

                if room == "Cafeteria":
                    st.divider()
                    st.caption("Combine the digits from Laboratory and Storage with the visible digits here.")
                    guess = st.text_input("Crack the PIN", key="pin_guess", max_chars=8)
                    if st.button("Check PIN", key="check_pin"):
                        if game.attempt_pin(guess):
                            st.success(
                                "🔓 Correct! The log confirms this PIN belongs to the **Supply Coordinator**."
                            )
                        else:
                            st.warning("Not quite — double check your digits.")
            else:
                if st.button(f"Investigate {room}", key=f"visit_{room}", disabled=not game.can_act()):
                    ok, clue = game.visit_room(room)
                    if ok:
                        st.rerun()
                    else:
                        st.warning(clue)

with tab_people:
    question_lookup = dict(case.QUESTION_BANK)
    for character in case.CHARACTERS:
        with st.expander(f"🧑 {character}", expanded=character not in game.asked):
            if character in game.asked:
                qa = game.asked[character]
                st.write(f"**You asked:** {question_lookup[qa['question']]}")
                st.write(f"**Answer:** {qa['answer']}")
            else:
                q_key = st.selectbox(
                    "Choose a question",
                    options=[k for k, _ in case.QUESTION_BANK],
                    format_func=lambda k: question_lookup[k],
                    key=f"qselect_{character}",
                )
                if st.button(f"Ask {character}", key=f"ask_{character}", disabled=not game.can_act()):
                    ok, answer = game.ask_question(character, q_key)
                    if ok:
                        st.rerun()
                    else:
                        st.warning(answer)

with tab_accuse:
    st.warning("Making an accusation immediately ends the investigation, whether you're right or not.")
    suspect = st.selectbox("Who is the mole?", options=case.CHARACTERS, key="accuse_select")
    if st.button("🚨 Accuse", type="primary"):
        game.make_accusation(suspect)
        st.rerun()

if game.actions_remaining == 0 and not game.game_over:
    st.error("You're out of actions! Head to the **Make an Accusation** tab to make your final call.")
