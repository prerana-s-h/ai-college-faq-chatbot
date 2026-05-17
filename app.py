"""
College FAQ Chatbot — Streamlit Chat Interface
Premium dark academic theme with glassmorphic design.
"""

import streamlit as st
import sys
import os

# Ensure project root is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config

# ─── Page Configuration ──────────────────────────────────
st.set_page_config(
    page_title="🎓 College FAQ Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS — Premium Dark Academic Theme ────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* ── Global Styles ── */
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1040 30%, #0d1f3c 60%, #0a0e27 100%) !important;
        font-family: 'Inter', sans-serif;
        color: #e2e8f0 !important;
    }

    /* Force ALL text to be visible */
    .stApp p, .stApp span, .stApp li, .stApp label, .stApp div,
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
    .stApp td, .stApp th, .stApp caption, .stApp strong, .stApp em, .stApp b, .stApp i {
        color: #e2e8f0 !important;
    }

    .stApp a {
        color: #818cf8 !important;
    }

    /* ── Hide default Streamlit branding ── */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ── Sidebar Styling ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f1635 0%, #1a1040 100%) !important;
        border-right: 1px solid rgba(99, 102, 241, 0.15);
    }

    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] li,
    [data-testid="stSidebar"] .stMarkdown {
        color: #c7d2fe !important;
    }

    /* ── Main Content Area ── */
    [data-testid="stMainBlockContainer"],
    .main .block-container {
        color: #e2e8f0 !important;
    }

    /* ── Main Chat Container ── */
    .main-header {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(139, 92, 246, 0.1) 100%);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 20px;
        padding: 30px 35px;
        margin-bottom: 25px;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        text-align: center;
        animation: fadeInDown 0.6s ease-out;
    }

    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .main-header h1 {
        background: linear-gradient(135deg, #818cf8, #a78bfa, #c084fc) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0 0 8px 0;
    }

    .main-header p {
        color: #94a3b8 !important;
        font-size: 1rem;
        margin: 0;
        font-weight: 300;
    }

    /* ── Chat Messages ── */
    [data-testid="stChatMessage"] {
        background: rgba(15, 23, 60, 0.6) !important;
        border: 1px solid rgba(99, 102, 241, 0.12) !important;
        border-radius: 16px !important;
        padding: 18px !important;
        margin-bottom: 12px !important;
        backdrop-filter: blur(10px) !important;
        animation: fadeIn 0.4s ease-out;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] li,
    [data-testid="stChatMessage"] span,
    [data-testid="stChatMessage"] strong,
    [data-testid="stChatMessage"] em,
    [data-testid="stChatMessage"] td,
    [data-testid="stChatMessage"] th,
    [data-testid="stChatMessage"] div {
        color: #e2e8f0 !important;
        line-height: 1.7 !important;
    }

    [data-testid="stChatMessage"] ul,
    [data-testid="stChatMessage"] ol {
        color: #e2e8f0 !important;
    }

    /* ── Chat Input ── */
    [data-testid="stChatInput"] {
        border: 1px solid rgba(99, 102, 241, 0.25) !important;
        border-radius: 14px !important;
    }

    [data-testid="stChatInput"] textarea {
        color: #e2e8f0 !important;
        font-family: 'Inter', sans-serif !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #64748b !important;
    }

    /* ── Spinner / Loading ── */
    .stSpinner > div > span {
        color: #a5b4fc !important;
    }

    /* ── Error / Info / Success boxes ── */
    .stAlert p, .stAlert span, .stAlert div {
        color: #e2e8f0 !important;
    }

    /* ── Sidebar Cards ── */
    .sidebar-card {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(139, 92, 246, 0.08) 100%);
        border: 1px solid rgba(99, 102, 241, 0.15);
        border-radius: 14px;
        padding: 18px;
        margin-bottom: 15px;
        backdrop-filter: blur(10px);
    }

    .sidebar-card h3 {
        color: #a5b4fc !important;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin: 0 0 10px 0;
    }

    .sidebar-card p {
        color: #cbd5e1 !important;
        font-size: 0.9rem;
        margin: 4px 0;
    }

    .stat-value {
        color: #818cf8 !important;
        font-weight: 700;
        font-size: 1.3rem;
    }

    /* ── Quick Reply Buttons ── */
    .stButton > button {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.15), rgba(139, 92, 246, 0.1)) !important;
        border: 1px solid rgba(99, 102, 241, 0.25) !important;
        color: #c7d2fe !important;
        border-radius: 12px !important;
        padding: 10px 16px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.3), rgba(139, 92, 246, 0.25)) !important;
        border-color: rgba(129, 140, 248, 0.5) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.2) !important;
    }

    .stButton > button p, .stButton > button span {
        color: #c7d2fe !important;
    }

    /* ── Selectbox ── */
    [data-testid="stSelectbox"] label {
        color: #a5b4fc !important;
        font-weight: 500 !important;
    }

    [data-testid="stSelectbox"] div[data-baseweb="select"] {
        color: #e2e8f0 !important;
    }

    [data-testid="stSelectbox"] div[data-baseweb="select"] span {
        color: #e2e8f0 !important;
    }

    /* ── Divider ── */
    hr {
        border-color: rgba(99, 102, 241, 0.15) !important;
    }

    /* ── Welcome Message ── */
    .welcome-msg {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.08) 0%, rgba(139, 92, 246, 0.05) 100%);
        border: 1px solid rgba(99, 102, 241, 0.12);
        border-radius: 16px;
        padding: 30px;
        text-align: center;
        margin: 20px 0;
    }

    .welcome-msg h2 {
        color: #a5b4fc !important;
        font-size: 1.5rem;
        margin-bottom: 12px;
    }

    .welcome-msg p {
        color: #94a3b8 !important;
        font-size: 0.95rem;
        line-height: 1.6;
    }

    .welcome-msg strong {
        color: #c7d2fe !important;
    }

    /* ── Status badge ── */
    .status-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }

    .status-online {
        background: rgba(34, 197, 94, 0.15);
        color: #4ade80 !important;
        border: 1px solid rgba(34, 197, 94, 0.25);
    }

    .status-offline {
        background: rgba(239, 68, 68, 0.15);
        color: #f87171 !important;
        border: 1px solid rgba(239, 68, 68, 0.25);
    }

    /* ── Markdown rendered content ── */
    .stMarkdown, .stMarkdown p, .stMarkdown li,
    .stMarkdown span, .stMarkdown strong, .stMarkdown em {
        color: #e2e8f0 !important;
    }

    /* ── Streamlit element container text ── */
    .stElementContainer, .stElementContainer p,
    .stElementContainer span, .stElementContainer div {
        color: #e2e8f0 !important;
    }
</style>
""", unsafe_allow_html=True)


# ─── Initialize Session State ───────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chatbot" not in st.session_state:
    st.session_state.chatbot = None
    st.session_state.bot_ready = False
    st.session_state.init_error = None

if "selected_language" not in st.session_state:
    st.session_state.selected_language = "en"


# ─── Initialize Chatbot ─────────────────────────────────
def init_chatbot():
    """Initialize the chatbot. Reloads .env to pick up changes."""
    try:
        # Reload .env in case the user just added/changed the API key
        from dotenv import load_dotenv
        load_dotenv(override=True)
        import importlib
        importlib.reload(config)

        from src.rag_chain import CollegeChatbot
        bot = CollegeChatbot()
        return bot, None
    except Exception as e:
        return None, str(e)


# ─── Sidebar ────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <div style="font-size: 3rem; margin-bottom: 8px;">🎓</div>
        <h2 style="color: #a5b4fc; font-size: 1.3rem; margin: 0; font-weight: 700;">College Assistant</h2>
        <p style="color: #64748b; font-size: 0.8rem; margin-top: 4px;">AI-Powered FAQ Bot</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Language selector
    lang_options = list(config.SUPPORTED_LANGUAGES.keys())
    selected_lang_name = st.selectbox(
        "🌐 Language",
        lang_options,
        index=0,
        help="Select your preferred language for responses",
    )
    st.session_state.selected_language = config.SUPPORTED_LANGUAGES[selected_lang_name]

    st.divider()

    # Quick reply buttons
    st.markdown("""
    <div class="sidebar-card">
        <h3>⚡ Quick Topics</h3>
    </div>
    """, unsafe_allow_html=True)

    quick_topics = {
        "📋 Admissions": "What is the admission process and eligibility criteria?",
        "💰 Fees": "What is the fee structure for all programs?",
        "🏠 Hostel": "What are the hostel facilities and fees?",
        "🎯 Placements": "What is the placement record and top recruiters?",
        "🎓 Scholarships": "What scholarships are available and how to apply?",
        "📞 Contact": "How can I contact the admissions office?",
        "📚 Courses": "What undergraduate and postgraduate programs are offered?",
        "📝 Exams": "How is the examination and grading system structured?",
    }

    for label, query in quick_topics.items():
        if st.button(label, key=f"quick_{label}", use_container_width=True):
            st.session_state.quick_query = query

    st.divider()

    # Stats card
    if st.session_state.bot_ready and st.session_state.chatbot:
        stats = st.session_state.chatbot.get_stats()
        st.markdown(f"""
        <div class="sidebar-card">
            <h3>📊 Stats</h3>
            <p>📄 Indexed: <span class="stat-value">{stats['total_documents']}</span> chunks</p>
            <p>💬 Turns: <span class="stat-value">{stats['conversation_turns']}</span></p>
            <p>🕐 Updated: {stats['last_index_update']}</p>
            <p>🤖 Model: {stats['model']}</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            if st.session_state.chatbot:
                st.session_state.chatbot.clear_memory()
            st.rerun()

    with col2:
        if st.button("🔄 Rebuild", use_container_width=True):
            if st.session_state.chatbot:
                with st.spinner("Rebuilding index..."):
                    st.session_state.chatbot.rebuild_index()
                st.success("Index rebuilt!")
                st.rerun()


# ─── Main Content ───────────────────────────────────────

# Header
st.markdown("""
<div class="main-header">
    <h1>🎓 College FAQ Assistant</h1>
    <p>Ask me anything about admissions, courses, fees, hostel, scholarships, and more!</p>
</div>
""", unsafe_allow_html=True)

# Initialize chatbot
if not st.session_state.bot_ready:
    with st.spinner("🔧 Initializing AI Assistant... (first load downloads the embedding model)"):
        bot, error = init_chatbot()
        if bot:
            st.session_state.chatbot = bot
            st.session_state.bot_ready = True
            st.session_state.init_error = None
        else:
            st.session_state.init_error = error

if st.session_state.init_error:
    st.error(f"⚠️ Failed to initialize chatbot: {st.session_state.init_error}")
    st.info("Make sure your `GROQ_API_KEY` is set correctly in the `.env` file, then click Retry.")
    if st.button("🔄 Retry Initialization"):
        st.session_state.bot_ready = False
        st.session_state.init_error = None
        st.session_state.chatbot = None
        st.rerun()
    st.stop()

# Status badge
if st.session_state.bot_ready:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <span class="status-badge status-online">● AI Assistant Online</span>
    </div>
    """, unsafe_allow_html=True)

# Display chat history
if not st.session_state.messages:
    st.markdown("""
    <div class="welcome-msg">
        <h2>👋 Welcome!</h2>
        <p>I'm your AI-powered college assistant. I can help you with questions about:<br>
        <strong>Admissions</strong> • <strong>Courses</strong> • <strong>Fees</strong> • <strong>Hostel</strong> • <strong>Scholarships</strong> • <strong>Placements</strong> • <strong>Exams</strong> • <strong>Campus Life</strong></p>
        <p style="margin-top: 15px; color: #64748b; font-size: 0.85rem;">
            Try the quick topics in the sidebar or type your question below ↓
        </p>
    </div>
    """, unsafe_allow_html=True)

for message in st.session_state.messages:
    avatar = "🧑‍🎓" if message["role"] == "user" else "🎓"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Handle quick query from sidebar
if "quick_query" in st.session_state and st.session_state.quick_query:
    query = st.session_state.quick_query
    st.session_state.quick_query = None

    # Add user message
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user", avatar="🧑‍🎓"):
        st.markdown(query)

    # Get response
    with st.chat_message("assistant", avatar="🎓"):
        with st.spinner("Thinking..."):
            response = st.session_state.chatbot.ask(
                query, language=st.session_state.selected_language
            )
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

# Chat input
if prompt := st.chat_input("Ask about admissions, fees, courses, hostel, placements..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍🎓"):
        st.markdown(prompt)

    # Get response
    with st.chat_message("assistant", avatar="🎓"):
        with st.spinner("Thinking..."):
            response = st.session_state.chatbot.ask(
                prompt, language=st.session_state.selected_language
            )
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
