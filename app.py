"""
app.py - Streamlit front-end for "Who Is the Mole?"

Run with:
    streamlit run app.py
"""
import streamlit as st

import case
import optimal_path
from game import GameState, TOTAL_BUDGET

st.set_page_config(page_title="Who Is the Mole?", page_icon="🧟", layout="wide")

if "game" not in st.session_state:
    st.session_state.game = GameState()
if "hints_used" not in st.session_state:
    st.session_state.hints_used = 0

game = st.session_state.game

st.title("🧟 Who Is the Mole?")
st.caption("An adversarial-AI mystery — 9 actions to find the mole before it's too late.")

with st.sidebar:
    st.header("Investigation Status")
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
    with col2:
        st.subheader("Performance")
        st.markdown(f"### Grade: {perf['grade']}")
        st.write(perf["message"])

    st.stop()

tab_rooms, tab_people, tab_accuse = st.tabs(
    ["🏚️ Investigate Rooms", "🗣️ Question Suspects", "⚖️ Make an Accusation"]
)

with tab_rooms:
    cols = st.columns(3)
    for col, room in zip(cols, case.ROOM_INFO.keys()):
        info = case.ROOM_INFO[room]
        with col:
            st.subheader(f"{info['emoji']} {room}")
            st.caption(info["flavor"])
            if room in game.visited_rooms:
                st.markdown(game.visited_rooms[room])
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
