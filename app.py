"""
app.py - Streamlit front-end for "Who Is the Mole?" — NOIR EDITION

Run with:
    streamlit run app.py
"""
import streamlit as st

import case
import optimal_path
from game import GameState, TOTAL_BUDGET
import sounds

st.set_page_config(page_title="Who Is the Mole?", page_icon="🧟", layout="wide")

# ---------- NOIR AESTHETIC: Dark purples + amber accents ----------
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Crimson+Text:ital@0;1&display=swap" rel="stylesheet">
    <style>
    .stApp {
        background: linear-gradient(135deg, #1a0f2e 0%, #2d1b4e 50%, #1f1135 100%);
        color: #e0d5d5;
    }
    body { font-family: 'Crimson Text', serif; }
    h1 { 
        color: #d4af37; 
        font-family: 'JetBrains Mono', monospace;
        font-size: 2.5rem;
        text-shadow: 0 0 10px rgba(212, 175, 55, 0.5);
        letter-spacing: 3px;
    }
    h2, h3 { 
        color: #f39c12;
        font-family: 'JetBrains Mono', monospace;
        text-shadow: 0 0 8px rgba(243, 156, 18, 0.4);
    }
    .stTabs [data-baseweb="tab-list"] { gap: 6px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #3d2860;
        border-radius: 8px 8px 0 0;
        padding: 10px 18px;
        color: #c9a961;
        font-family: 'JetBrains Mono', monospace;
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
        font-family: 'JetBrains Mono', monospace;
    }
    .stButton>button {
        background-color: #5a3d8a;
        color: #d4af37;
        border-radius: 8px;
        border: 1.5px solid #d4af37;
        font-family: 'JetBrains Mono', monospace;
        font-weight: bold;
        box-shadow: 0 0 8px rgba(212, 175, 55, 0.3);
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #d4af37;
        color: #1a0f2e;
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.8);
    }
    .note-card {
        background: #f4ecd8;
        color: #3a3226;
        font-family: 'Kalam', cursive;
        padding: 22px 24px 16px 24px;
        border-radius: 2px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.7);
        transform: rotate(-1deg);
        position: relative;
        margin: 14px 4px;
        line-height: 1.7;
        font-size: 1.05rem;
    }
    .note-card::before {
        content: "📌";
        position: absolute;
        top: -16px;
        left: 22px;
        font-size: 1.5rem;
    }
    .hint-letter {
        font-size: 1.6rem;
        font-weight: 800;
        color: #b91c1c;
        text-decoration: underline;
        margin-right: 2px;
    }
    .riddle-board {
        background-color: #10151f;
        background-image:
            linear-gradient(#1c2434 1px, transparent 1px),
            linear-gradient(90deg, #1c2434 1px, transparent 1px);
        background-size: 22px 22px;
        color: #e5e7eb;
        font-family: 'Caveat', cursive;
        font-size: 1.4rem;
        padding: 24px;
        border-radius: 8px;
        border: 2px solid #334155;
        line-height: 1.9;
        margin: 14px 4px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.7);
    }
    .riddle-line { margin: 2px 0; }
    .scratched {
        text-decoration: line-through;
        text-decoration-thickness: 4px;
        text-decoration-color: #ef4444;
        color: #94a3b8;
        display: inline-block;
    }
    .decoy-line { color: #fbbf24; font-style: italic; }
    .helper-line { color: #34d399; }
    .receipt {
        background: #fdfdfd;
        color: #111;
        font-family: 'Courier New', monospace;
        padding: 16px 20px;
        border: 1px dashed #999;
        max-width: 320px;
        margin: 14px auto;
        box-shadow: 0 4px 20px rgba(0,0,0,0.7);
    }
    .receipt-title { text-align: center; font-weight: bold; margin-bottom: 8px; }
    .pin-digit {
        display: inline-block;
        width: 28px;
        text-align: center;
        border-bottom: 2px solid #333;
        margin: 0 3px;
        font-weight: bold;
        font-size: 1.1rem;
    }
    .pin-digit.redacted { color: #bbb; }

    /* --- Evidence Board --- */
    .evidence-grid {
        background: #2d1f42;
        border: 2px solid #d4af37;
        border-radius: 8px;
        padding: 16px;
        margin: 10px 0;
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.3);
    }
    .suspect-card {
        background: #3d2860;
        border-left: 4px solid #f39c12;
        padding: 12px;
        margin: 8px 0;
        border-radius: 4px;
        font-family: 'JetBrains Mono', monospace;
    }
    .guilt-bar {
        background: #1a0f2e;
        border-radius: 4px;
        height: 20px;
        overflow: hidden;
        margin: 8px 0;
    }
    .guilt-fill {
        height: 100%;
        background: linear-gradient(90deg, #f39c12 0%, #d4af37 50%, #e74c3c 100%);
        transition: width 0.3s ease;
    }
    .contradiction-alert {
        background: #8b0000;
        border-left: 4px solid #ff6b6b;
        color: #ffb3b3;
        padding: 12px;
        margin: 10px 0;
        border-radius: 4px;
        font-family: 'JetBrains Mono', monospace;
    }
    .log-entry {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.9rem;
        color: #c9a961;
        padding: 4px 0;
        border-bottom: 1px dotted #5a3d8a;
        animation: typewrite 0.2s ease-in;
    }
    @keyframes typewrite {
        from { opacity: 0; transform: translateX(-10px); }
        to { opacity: 1; transform: translateX(0); }
    }
    .suspicion-meter {
        background: #1a0f2e;
        border: 2px solid #d4af37;
        border-radius: 8px;
        padding: 12px;
        margin: 10px 0;
    }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Kalam:wght@400;700&family=Caveat:wght@500;700&display=swap" rel="stylesheet">
    """,
    unsafe_allow_html=True,
)


# ---------- Clue renderers ----------
def render_lab_note(lines):
    html = '<div class="note-card">'
    for letter, rest in lines:
        html += f'<div><span class="hint-letter">{letter}</span>{rest}</div>'
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
        html += f'<div class="{classes}">{item["text"]}</div>'
    html += "</div>"
    return html


def render_receipt(job, pin_digits, redacted):
    html = '<div class="receipt">'
    html += '<div class="receipt-title">RESTOCKING LOG — MACHINE #3</div>'
    html += f"<div>Restocked by: <b>{job}</b></div>"
    html += '<div style="margin-top:10px;">Employee PIN: '
    for digit, is_redacted in zip(pin_digits, redacted):
        if is_redacted:
            html += '<span class="pin-digit redacted">?</span>'
        else:
            html += f'<span class="pin-digit">{digit}</span>'
    html += "</div></div>"
    return html


def render_evidence_board(game):
    """Render the detective board with suspect guilt scores and contradictions."""
    html = '<div class="evidence-grid">'
    html += '<h3 style="color: #d4af37; margin-top: 0;">EVIDENCE BOARD</h3>'

    # Contradictions
    if game.evidence.contradictions:
        for contradiction in game.evidence.contradictions:
            html += f'<div class="contradiction-alert">🚨 {contradiction["detail"]}</div>'

    # Suspect guilt scores
    html += '<div style="margin-top: 16px;">'
    for character in case.CHARACTERS:
        guilt = game.evidence.get_guilt_score(character)
        guilt_pct = int((guilt / 100) * 100)
        location = case.PROFILES[character]["location"]
        job = case.PROFILES[character]["job"]
        html += f'''
        <div class="suspect-card">
            <div style="font-weight: bold; color: #d4af37;">{character}</div>
            <div style="font-size: 0.85rem; color: #c9a961;">{job} • {location}</div>
            <div class="guilt-bar">
                <div class="guilt-fill" style="width: {guilt_pct}%;"></div>
            </div>
            <div style="font-size: 0.8rem; color: #f39c12;">Suspicion: {guilt}/100</div>
        </div>
        '''
    html += '</div></div>'
    return html


# ---------- Session state ----------
if "game" not in st.session_state:
    st.session_state.game = GameState()
if "hints_used" not in st.session_state:
    st.session_state.hints_used = 0
if "researcher_name" not in st.session_state:
    st.session_state.researcher_name = ""
if "play_sound" not in st.session_state:
    st.session_state.play_sound = False

game = st.session_state.game
name = st.session_state.researcher_name

st.title("🧟 WHO IS THE MOLE?")
if name:
    st.caption(f"Detective Case File: {name} | 9 Actions Remaining")
else:
    st.caption("A noir-tinged mystery awaits... 9 actions to crack the case.")

# ---------- Sidebar ----------
with st.sidebar:
    st.header("CASE DOSSIER")
    if name:
        st.write(f"**Detective:** {name}")
    
    st.subheader("Actions Remaining")
    st.metric("", game.actions_remaining)
    st.progress(game.actions_used / TOTAL_BUDGET)

    st.subheader("Suspicion Level")
    st.write(f"{game.suspicion}/100")
    col_sus = st.columns([1])
    with col_sus[0]:
        st.progress(game.suspicion / 100)

    HINT_LIMIT = 2
    if not game.game_over:
        if st.session_state.hints_used < HINT_LIMIT:
            if st.button(f"💡 Get a Hint ({HINT_LIMIT - st.session_state.hints_used} left)"):
                st.session_state.hints_used += 1
                st.info(optimal_path.get_hint(game))
        else:
            st.caption("*No hints remaining.*")

    st.divider()
    if st.button("🔄 START NEW CASE"):
        st.session_state.game = GameState()
        st.session_state.hints_used = 0
        st.rerun()

    with st.expander("📋 CASE LOG"):
        if game.log:
            st.markdown('<div class="log-entry">' + '<br>'.join(game.log[-10:]) + '</div>', unsafe_allow_html=True)
        else:
            st.write("*No entries yet.*")

st.markdown(case.CASE_INTRO)

# ---------- End-of-game screen ----------
if game.game_over:
    st.divider()
    if game.result == "win":
        st.success(f"✅ CASE CLOSED: {game.accused} is the mole.")
        st.audio(sounds.success_chime(), format="audio/wav")
    else:
        st.error(f"❌ CASE FAILED: {game.accused} was accused, but the true mole was {case.MOLE}.")

    stats = game.get_stats()
    perf = optimal_path.evaluate_performance(stats)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("INVESTIGATION REPORT")
        st.write(f"- Actions Used: **{stats['actions_used']}/9**")
        st.write(f"- Final Suspicion: **{stats['suspicion']}/100**")
        st.write(f"- Mole Sabotages: **{stats['sabotage_count']}**")
        st.write(f"- Mole Helps: **{stats['help_count']}**")
        st.write(f"- Lies Detected: **{stats['lie_count']}**")
        st.write(f"- Contradictions Found: **{'Yes' if stats['contradiction_flagged'] else 'No'}**")
        st.write(f"- PIN Cracked: **{'Yes' if stats['pin_cracked'] else 'No'}**")
    with col2:
        st.subheader("VERDICT")
        st.markdown(f"### {perf['grade']}")
        st.write(perf["message"])

    st.stop()

# ---------- Main tabs ----------
tab_researcher, tab_evidence, tab_rooms, tab_people, tab_accuse = st.tabs(
    ["🧑‍💼 DETECTIVE", "🔍 EVIDENCE", "🏚️ CRIME SCENES", "🗣️ INTERROGATIONS", "⚖️ ACCUSATION"]
)

with tab_researcher:
    st.subheader("Detective Profile")
    entered = st.text_input(
        "Your name (optional)", value=st.session_state.researcher_name, placeholder="e.g. Detective Osei"
    )
    if st.button("Register"):
        st.session_state.researcher_name = entered.strip()
        st.rerun()

    st.divider()
    st.subheader("Suspects")
    for character in case.CHARACTERS:
        job = case.PROFILES[character]["job"]
        location = case.PROFILES[character]["location"]
        st.write(f"**{character}** — {job} *(Last seen: {location})*")

with tab_evidence:
    st.subheader("Detective Board")
    st.markdown(render_evidence_board(game), unsafe_allow_html=True)

    if game.evidence.contradictions:
        st.divider()
        st.subheader("Flagged Contradictions")
        for contradiction in game.evidence.contradictions:
            st.warning(f"⚠️ {contradiction['detail']}")

with tab_rooms:
    cols = st.columns(3)
    for col, room in zip(cols, case.ROOM_INFO.keys()):
        info = case.ROOM_INFO[room]
        with col:
            st.subheader(f"{info['emoji']} {room}")
            st.caption(info["flavor"])
            if room in game.visited_rooms:
                clue = game.visited_rooms[room]
                if room == "Laboratory":
                    st.markdown(render_lab_note(clue), unsafe_allow_html=True)
                elif room == "Storage":
                    st.markdown(render_riddle_board(clue), unsafe_allow_html=True)
                elif room == "Cafeteria":
                    st.markdown(
                        render_receipt(clue["job"], clue["pin_digits"], clue["redacted"]),
                        unsafe_allow_html=True,
                    )
                    st.divider()
                    guess = st.text_input("PIN Guess", key="pin_guess", max_chars=8, placeholder="e.g. 4619")
                    if st.button("Verify PIN", key="check_pin"):
                        if game.attempt_pin(guess):
                            st.success("🔓 Correct PIN! Supply Coordinator confirmed.")
                            st.audio(sounds.success_chime(), format="audio/wav")
                        else:
                            st.warning("Incorrect PIN. Double-check your digits.")
            else:
                if st.button(f"Investigate {room}", key=f"visit_{room}", disabled=not game.can_act()):
                    ok, clue = game.visit_room(room)
                    if ok:
                        st.audio(sounds.typewriter_click(), format="audio/wav")
                        st.rerun()
                    else:
                        st.warning(clue)

with tab_people:
    question_lookup = dict(case.QUESTION_BANK)
    for character in case.CHARACTERS:
        with st.expander(f"🧑 {character}", expanded=character not in game.asked):
            if character in game.asked:
                qa = game.asked[character]
                st.write(f"**Q:** {question_lookup[qa['question']]}")
                st.write(f"**A:** _{qa['answer']}_")
                if qa["lied"]:
                    st.warning("⚠️ This answer was a lie.")
            else:
                q_key = st.selectbox(
                    "Question",
                    options=[k for k, _ in case.QUESTION_BANK],
                    format_func=lambda k: question_lookup[k],
                    key=f"qselect_{character}",
                )
                if st.button(f"Ask {character}", key=f"ask_{character}", disabled=not game.can_act()):
                    ok, answer = game.ask_question(character, q_key)
                    if ok:
                        st.audio(sounds.typewriter_click(), format="audio/wav")
                        st.rerun()
                    else:
                        st.warning(answer)

with tab_accuse:
    st.warning("🚨 Making an accusation ends the investigation immediately.")
    suspect = st.selectbox("Accusation", options=case.CHARACTERS, key="accuse_select")
    if st.button("🔨 ACCUSE", type="primary"):
        game.make_accusation(suspect)
        st.rerun()

if game.actions_remaining == 0 and not game.game_over:
    st.error("⏰ Out of actions! Make your final accusation.")
