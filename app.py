import streamlit as st
import random
from graph import create_evaluate_graph, create_defender_graph, setup_story, setup_custom_story
from agents import hunter_generate_claim, generate_random_topic_llm

st.set_page_config(
    page_title="Make it make sense",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cute Neobrutalism CSS theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&display=swap');
    
    * {
        font-family: 'Space Grotesk', sans-serif;
    }
    
    .stApp {
        background-color: #fce4ec; /* Soft base background */
        background-image: radial-gradient(#e0c5ce 1px, transparent 1px);
        background-size: 20px 20px;
    }
    
    .story-card {
        background: #fffbdf; /* Light yellow */
        border: 4px solid #111;
        border-radius: 12px;
        padding: 1.75rem;
        box-shadow: 6px 6px 0px #111;
        color: #111;
        font-weight: 500;
        font-size: 1.05rem;
    }
    
    .hunter-message {
        background: #ffaaa5; /* Pastel Pink */
        border: 4px solid #111;
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        box-shadow: 4px 4px 0px #111;
        color: #111;
    }
    
    .defender-message {
        background: #a8e6cf; /* Mint green */
        border: 4px solid #111;
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        box-shadow: 4px 4px 0px #111;
        color: #111;
    }
    
    .reveal-container {
        background: #dcedc1; /* Light Lime */
        border: 4px solid #111;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 4px 4px 0px #111;
        color: #111;
        filter: blur(6px);
        transition: all 0.2s ease-in-out;
        cursor: pointer;
    }
    
    .reveal-container:hover {
        filter: blur(0);
        transform: translate(-2px, -2px);
        box-shadow: 6px 6px 0px #111;
    }
    
    .glow-title {
        font-size: 100rem;
        font-weight: 800;
        color: #111;
        text-transform: uppercase;
        text-align: center;
        text-shadow: 4px 4px 0px #ffaaa5, 8px 8px 0px #a8e6cf;
        letter-spacing: 4px;
        margin-top: 1rem;
        margin-bottom: 1rem;
        line-height: 2;
    }
    
    .section-header {
        font-size: 1.5rem;
        font-weight: 800;
        margin-bottom: 1rem;
        color: #111;
        border-bottom: 4px solid #111;
        display: inline-block;
        padding-bottom: 4px;
        text-transform: uppercase;
    }
    
    .winner-badge {
        display: inline-block;
        background: #ffd3b6;
        border: 3px solid #111;
        padding: 5px 15px;
        font-weight: 800;
        border-radius: 20px;
        box-shadow: 3px 3px 0px #111;
        font-size: 0.95rem;
        margin-bottom: 15px;
        text-transform: uppercase;
        color: #111;
    }

    [data-testid="stSidebar"] {
        background-color: #fff;
        border-right: 4px solid #111;
        box-shadow: inset -6px 0 0 rgba(0,0,0,0.05);
    }
    
    [data-testid="stSpinner"] * {
        color: #111 !important;
        font-weight: 700;
    }
    
    .judge-container {
        background: #cbaacb;
        border: 3px solid #111;
        border-radius: 8px;
        padding: 0.75rem;
        margin-bottom: 0.75rem;
        box-shadow: 2px 2px 0px #111;
        color: #111;
    }
    
    .coach-container {
        background: #abdee6;
        border: 3px solid #111;
        border-radius: 8px;
        padding: 0.75rem;
        box-shadow: 2px 2px 0px #111;
        color: #111;
    }
    
    /* Make sidebar text elements black */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] .stMarkdown p {
        color: #111 !important;
        font-weight: 600 !important;
    }
/* Force white text on ALL buttons */
.stButton button {
    color: white !important;
}

.stButton button p {
    color: white !important;
}

/* Make sure the primary button (DROP IN & START) has white text */
.stButton button[kind="primary"] {
    color: white !important;
}

.stButton button[kind="primary"] p {
    color: white !important;
}

/* Keep white text on the secondary button too */
.stButton button[kind="secondary"] {
    color: white !important;
}

.stButton button[kind="secondary"] p {
    color: white !important;
}

/* Specific fix for DROP IN & START button */
button[kind="primary"][data-testid="baseButton-primary"] {
    color: white !important;
}

button[kind="primary"] p {
    color: white !important;
    font-weight: 700 !important;
}

/* Override any Streamlit default colors */
.stButton button p,
.stButton button span,
.stButton button div {
    color: white !important;
}

/* Button styling structural rules - White text by default */
.stButton > button {
    background: #111 !important;
    border: 4px solid #111 !important;
    border-radius: 8px !important;
    box-shadow: 4px 4px 0px #a8e6cf !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    transition: transform 0.1s !important;
}

/* Hover state - Keep text white */
.stButton > button:hover {
    transform: translate(2px, 2px);
    box-shadow: 2px 2px 0px #111;
    background-color: #ffaaa5 !important;
}

.stButton > button:hover p,
.stButton > button:hover div,
.stButton > button:hover span,
.stButton > button:hover * {
    color: #111 !important;  /* Keep text white on hover too */
}
    
    .stTextArea textarea, .stTextInput input, .stSelectbox [data-baseweb="select"] {
        border: 3px solid #111 !important;
        border-radius: 8px !important;
        box-shadow: 4px 4px 0px #dcedc1 !important;
        background: #fff;
        color: #111;
        font-weight: 500;
    }
    
    .stTextArea textarea:focus, .stSelectbox [data-baseweb="select"]:focus {
        border-color: #ffaaa5 !important;
        box-shadow: 4px 4px 0px #ffaaa5 !important;
    }

    /* Radio button custom styling */
    .stRadio label {
        color: #111 !important;
        font-weight: 700 !important;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #111;
        font-weight: 800;
        font-size: 2rem;
    }
    [data-testid="stMetricLabel"] {
        color: #111;
        font-weight: 600;
        font-size: 1rem;
        text-transform: uppercase;
    }
    
    .role-badge {
        display: inline-flex;
        align-items: center;
        background: #a8e6cf;
        color: #111;
        border: 3px solid #111;
        box-shadow: 3px 3px 0px #111;
        padding: 0.4rem 1rem;
        font-weight: 800;
        text-transform: uppercase;
    }
</style>
""", unsafe_allow_html=True)

# Title Section
col_left, col_mid, col_right = st.columns([1, 4, 1])
with col_mid:
    st.markdown('<p class="glow-title">Make it make sense</p>', unsafe_allow_html=True)
with col_right:
    if st.session_state.get("role"):
        st.markdown(f'<div class="role-badge" style="float: right; margin-top: 40px;">Role: {st.session_state.role}</div>', unsafe_allow_html=True)

st.markdown("<hr style='border: 2px solid #111;'>", unsafe_allow_html=True)

# Initialize Session State
if "story" not in st.session_state:
    st.session_state.story = ""
if "topic" not in st.session_state:
    st.session_state.topic = ""
if "history" not in st.session_state:
    st.session_state.history = []
if "role" not in st.session_state:
    st.session_state.role = "Hunter"
if "topic_input_val" not in st.session_state:
    st.session_state.topic_input_val = "A political satire where animals run the parliament."
if "ai_hunter_claim" not in st.session_state:
    st.session_state.ai_hunter_claim = ""
if "language_val" not in st.session_state:
    st.session_state.language_val = "English"

# Graphs
eval_graph = create_evaluate_graph()
defender_graph = create_defender_graph()

def generate_random_topic():
    try:
        new_topic = generate_random_topic_llm(st.session_state.language_val)
        st.session_state.topic_input_val = new_topic
    except Exception:
        st.session_state.topic_input_val = "A suspenseful mystery in an abandoned theme park."

def on_role_change():
    if st.session_state.role == "Defender" and st.session_state.story:
        if not st.session_state.ai_hunter_claim:
            try:
                ai_claim = hunter_generate_claim(st.session_state.story, st.session_state.language_val)
                st.session_state.ai_hunter_claim = ai_claim
            except Exception:
                pass

# Sidebar
with st.sidebar:
    st.markdown("<div class='section-header'>Setup Arena</div>", unsafe_allow_html=True)
    
    st.markdown("### Language Selection")
    st.session_state.language_val = st.selectbox(
        "Language:", 
        ["English", "Tanglish", "Tamil", "Spanish", "French", "German", "Japanese"], 
        index=0, 
        label_visibility="collapsed"
    )
    
    st.markdown("### Story Source")
    story_source = st.radio("Source:", ["AI Generated", "Provide Custom Story"], label_visibility="collapsed")
    
    if story_source == "AI Generated":
        if st.button("Generate Random Topic", use_container_width=True):
            with st.spinner("Generating creative topic..."):
                generate_random_topic()
                
        topic_input = st.text_area("Topic:", value=st.session_state.topic_input_val, height=100)
        custom_story_input = None
    else:
        topic_input = None
        custom_story_input = st.text_area("Your Custom Story:", placeholder="Paste your story here...", height=250)
    
    st.markdown("### Select Your Role")
    st.radio(
        "", 
        ["Hunter", "Defender"], 
        index=0 if st.session_state.role == "Hunter" else 1, 
        label_visibility="collapsed",
        key="role",
        on_change=on_role_change
    )
    
    st.markdown("---")
    start_btn_text = "Drop in & Start"
    if st.button(start_btn_text, type="primary", use_container_width=True, key="drop_in_btn"):
        if story_source == "Provide Custom Story" and not custom_story_input:
            st.warning("Please paste a story to begin.")
        else:
            with st.spinner("Preparing the debate arena..."):
                try:
                    if story_source == "AI Generated":
                        story = setup_story(topic_input, st.session_state.language_val)
                    else:
                        story = setup_custom_story(custom_story_input)
                        
                    st.session_state.story = story
                    st.session_state.topic = topic_input if topic_input else "Custom Text"
                    st.session_state.history = []
                    st.session_state.ai_hunter_claim = ""
                    
                    if st.session_state.role == "Defender":
                        with st.spinner("AI Hunter is analyzing the story for contradictions..."):
                            ai_claim = hunter_generate_claim(story, st.session_state.language_val)
                            st.session_state.ai_hunter_claim = ai_claim
                            
                    st.rerun()
                except Exception as e:
                    st.error(f"Error starting game. Ensure LM Studio is running. Details: {e}")
    
    if st.button("Reset Game", use_container_width=True):
        for key in ["story", "topic", "history", "ai_hunter_claim"]:
            if key in st.session_state:
                if key == "history":
                    st.session_state[key] = []
                else:
                    st.session_state[key] = ""
        st.rerun()

if st.session_state.story:
    
    # Render Story
    st.markdown('<div class="section-header">The Storyteller\'s Narrative</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="story-card">{st.session_state.story}</div>', unsafe_allow_html=True)
    
    st.markdown("<hr style='margin: 3rem 0; border: 2px solid #111;'>", unsafe_allow_html=True)
    
    # Render ReasonIt
    st.markdown('<div class="section-header">ReasonIt</div>', unsafe_allow_html=True)
    
    history_container = st.container()
    with history_container:
        if st.session_state.history:
            for idx, item in enumerate(st.session_state.history):
                hist_col1, hist_col2 = st.columns(2, gap="large")
                
                with hist_col1:
                    st.markdown(f'<div class="hunter-message"><strong>Hunter Claim #{idx+1}</strong><br>{item["hunter"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="defender-message"><strong>Defender Response #{idx+1}</strong><br>{item["defender"]}</div>', unsafe_allow_html=True)
                
                with hist_col2:
                    judge_text = str(item.get("judge", ""))
                    winner_html = ""
                    if "Winner: Hunter" in judge_text:
                        winner_html = '<div class="winner-badge">WINNER: HUNTER</div>'
                    elif "Winner: Defender" in judge_text:
                        winner_html = '<div class="winner-badge">WINNER: DEFENDER</div>'
                    
                    st.markdown(f'{winner_html}<div style="margin-bottom: 10px; font-weight: 800; color: #111; text-transform: uppercase;">Round {idx+1} Evaluation <span style="font-size:0.8rem; font-weight:600; color:#444;">(Hover to reveal)</span></div>', unsafe_allow_html=True)
                    
                    eval_html = '<div class="reveal-container">'
                    if item.get('judge'):
                        eval_html += f'<div class="judge-container"><strong>JUDGE:</strong> {judge_text}</div>'
                    if item.get('coach'):
                        eval_html += f'<div class="coach-container"><strong>COACH:</strong> {item["coach"]}</div>'
                    eval_html += '</div>'
                    st.markdown(eval_html, unsafe_allow_html=True)
                
                if idx < len(st.session_state.history) - 1:
                    st.markdown('<hr style="margin: 2rem 0; border: 2px solid rgba(17, 17, 17, 0.2);">', unsafe_allow_html=True)
        else:
            st.info("No debates yet. Submit a claim or defense to start the arena!")
    
    st.markdown("<hr style='border: 2px solid #111;'>", unsafe_allow_html=True)
    
    # Interactive UI
    if st.session_state.role == "Hunter":
        st.markdown("<div class='section-header'>Your Turn as Hunter</div>", unsafe_allow_html=True)
        hunter_claim = st.text_area(
            "Claim:", 
            placeholder="Point out a contradiction...",
            key=f"hunter_claim_{len(st.session_state.history)}",
            label_visibility="collapsed"
        )
        if st.button("Launch Attack", type="primary"):
            if hunter_claim:
                with st.spinner("Agents are evaluating your claim..."):
                    try:
                        state_input = {
                            "story": st.session_state.story,
                            "hunter_claim": hunter_claim,
                            "defender_response": None,
                            "judge_summary": None,
                            "coach_feedback": None,
                            "language": st.session_state.language_val
                        }
                        result = eval_graph.invoke(state_input)
                        
                        st.session_state.history.append({
                            "hunter": hunter_claim,
                            "defender": result["defender_response"],
                            "judge": result["judge_summary"],
                            "coach": result["coach_feedback"]
                        })
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error processing debate: {e}")
            else:
                st.warning("Please enter a claim first.")
                
    else:  # Role == Defender
        st.markdown("<div class='section-header'>AI Hunter Challenges You</div>", unsafe_allow_html=True)
        st.markdown(f'<div class="hunter-message"><strong>AI Hunter\'s Claim:</strong><br>{st.session_state.ai_hunter_claim}</div>', unsafe_allow_html=True)
        
        st.markdown("<div class='section-header'>Your Defense</div>", unsafe_allow_html=True)
        defender_resp = st.text_area(
            "Defense:", 
            placeholder="Refute the AI's claim...",
            key=f"def_resp_{len(st.session_state.history)}",
            label_visibility="collapsed"
        )
        if st.button("Block Attack", type="primary"):
            if defender_resp:
                with st.spinner("Judge and Coach are evaluating..."):
                    try:
                        state_input = {
                            "story": st.session_state.story,
                            "hunter_claim": st.session_state.ai_hunter_claim,
                            "defender_response": defender_resp,
                            "judge_summary": None,
                            "coach_feedback": None,
                            "language": st.session_state.language_val
                        }
                        result = defender_graph.invoke(state_input)
                        
                        st.session_state.history.append({
                            "hunter": st.session_state.ai_hunter_claim,
                            "defender": defender_resp,
                            "judge": result["judge_summary"],
                            "coach": result["coach_feedback"]
                        })
                        
                        with st.spinner("AI Hunter is analyzing for the next contradiction..."):
                            ai_claim = hunter_generate_claim(st.session_state.story, st.session_state.language_val)
                            st.session_state.ai_hunter_claim = ai_claim
                            
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error processing debate: {e}")
            else:
                st.warning("Please enter your defense first.")

    st.markdown("---")
    col_stats1, col_stats2, col_stats3, col_stats4 = st.columns(4)
    with col_stats1:
        st.metric("Story Length", f"{len(st.session_state.story)} chars")
    with col_stats2:
        st.metric("Debates", len(st.session_state.history))
    with col_stats3:
        hunter_wins = sum(1 for item in st.session_state.history if "Winner: Hunter" in str(item.get("judge", "")))
        st.metric("Hunter Wins", hunter_wins)
    with col_stats4:
        defender_wins = sum(1 for item in st.session_state.history if "Winner: Defender" in str(item.get("judge", "")))
        st.metric("Defender Wins", defender_wins)

else:
    st.markdown("""
    <div style="background: #fffbdf; border: 4px solid #111; box-shadow: 8px 8px 0px #111; border-radius: 20px; padding: 4rem 2rem; text-align: center; margin: 3rem auto; max-width: 800px;">
        <h1 style="font-size: 3rem; color: #111; text-transform: uppercase; font-weight: 800; margin-bottom: 1rem;">Enter the Arena</h1>
        <p style="color: #444; font-size: 1.25rem; font-weight: 500; margin-bottom: 2rem;">Configure your game in the sidebar to begin hunting contradictions.</p>
        <div style="display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap;">
            <div style="background: #ffaaa5; border: 3px solid #111; padding: 1rem 2rem; box-shadow: 4px 4px 0px #111; border-radius: 12px; font-weight: 800; color: #111; text-transform: uppercase;">1. Set Language</div>
            <div style="background: #a8e6cf; border: 3px solid #111; padding: 1rem 2rem; box-shadow: 4px 4px 0px #111; border-radius: 12px; font-weight: 800; color: #111; text-transform: uppercase;">2. Pick Role</div>
            <div style="background: #dcedc1; border: 3px solid #111; padding: 1rem 2rem; box-shadow: 4px 4px 0px #111; border-radius: 12px; font-weight: 800; color: #111; text-transform: uppercase;">3. Drop In</div>
        </div>
    </div>
    """, unsafe_allow_html=True)