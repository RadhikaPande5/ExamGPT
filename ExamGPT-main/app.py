"""
ExamGPT - Frontend
A RAG-based exam preparation assistant.
Backend (ingestion.py, retrieval.py) is untouched — this file only
handles presentation, layout, and session state.
"""

import os
import tempfile

import streamlit as st

os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

from ingestion import ingest_pdf, clear_vectorstore
from retrieval import ask_gemini, extract_citation_info


# ============================================================
# CONSTANTS
# ============================================================

PAGE_TITLE = "ExamGPT"
PAGE_ICON = None  # keep the browser tab clean, no emoji favicon

STEPS = [
    ("01", "Upload", "Add class notes and previous year question papers as PDF files."),
    ("02", "Process", "Documents are chunked, embedded, and stored in a vector index."),
    ("03", "Ask", "Chat naturally. Every answer is grounded in your material, with citations."),
]

FEATURES = [
    ("source", "Cited answers", "Every response references the exact document and page it came from."),
    ("pin", "Frequency detection", "Concepts that match uploaded past papers are flagged automatically."),
    ("lock", "Private by default", "Documents are stored only in this session's local vector index."),
    ("bolt", "Grounded responses", "Answers come only from your uploaded material, nothing else."),
]


# ============================================================
# THEME
# ============================================================

def get_theme(mode: str) -> dict:
    """Return a dict of CSS variable values for the given theme mode."""
    if mode == "dark":
        return {
            "bg": "#0d0e12",
            "bg_elevated": "#15161b",
            "surface": "rgba(255, 255, 255, 0.04)",
            "surface_border": "rgba(255, 255, 255, 0.08)",
            "surface_hover": "rgba(255, 255, 255, 0.07)",
            "text_primary": "#e8e9ed",
            "text_secondary": "#9497a3",
            "text_muted": "#6b6e7d",
            "accent": "#6366f1",
            "accent_soft": "rgba(99, 102, 241, 0.14)",
            "divider": "rgba(255, 255, 255, 0.08)",
            "shadow": "0 1px 2px rgba(0,0,0,0.4)",
            "icon_stroke": "#c7c9d4",
            "input_bg": "rgba(255, 255, 255, 0.03)",
            "success_bg": "rgba(34, 197, 94, 0.12)",
            "success_text": "#4ade80",
            "error_bg": "rgba(239, 68, 68, 0.12)",
            "error_text": "#f87171",
        }
    return {
        "bg": "#fafafa",
        "bg_elevated": "#ffffff",
        "surface": "rgba(255, 255, 255, 0.6)",
        "surface_border": "rgba(15, 15, 20, 0.08)",
        "surface_hover": "rgba(255, 255, 255, 0.9)",
        "text_primary": "#18181b",
        "text_secondary": "#52525b",
        "text_muted": "#8b8b96",
        "accent": "#4f46e5",
        "accent_soft": "rgba(79, 70, 229, 0.08)",
        "divider": "rgba(15, 15, 20, 0.08)",
        "shadow": "0 1px 2px rgba(15,15,20,0.06)",
        "icon_stroke": "#3f3f46",
        "input_bg": "rgba(15, 15, 20, 0.02)",
        "success_bg": "rgba(34, 197, 94, 0.10)",
        "success_text": "#16a34a",
        "error_bg": "rgba(239, 68, 68, 0.10)",
        "error_text": "#dc2626",
    }


def inject_css(theme: dict) -> None:
    """Inject the full stylesheet using the active theme's variables."""
    st.markdown(
        f"""
        <style>
        html, body, [class*="css"] {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Inter, Roboto, sans-serif;
        }}

        .stApp {{
            background: {theme['bg']};
        }}

        section[data-testid="stSidebar"] {{
            background: {theme['bg_elevated']};
            border-right: 1px solid {theme['divider']};
        }}

        h1, h2, h3, h4, p, span, label, div {{
            color: {theme['text_primary']};
        }}

        /* ---------- Layout helpers ---------- */
        .block-container {{
            padding-top: 3rem;
            max-width: 1100px;
        }}

        /* ---------- Native top header / toolbar ---------- */
        [data-testid="stHeader"] {{
            background: {theme['bg']} !important;
            border-bottom: 1px solid {theme['divider']};
        }}
        [data-testid="stToolbar"] button,
        [data-testid="stHeader"] svg {{
            color: {theme['text_secondary']} !important;
            fill: {theme['text_secondary']} !important;
        }}
        [data-testid="stDecoration"] {{
            display: none;
        }}
        [data-testid="stAppViewContainer"] {{
            background: {theme['bg']};
        }}
        [data-testid="stMainMenu"] {{
            color: {theme['text_secondary']} !important;
        }}

        /* ---------- Native buttons (force out of Streamlit's own light theme) ---------- */
        .stButton > button,
        .stButton > button:focus,
        .stButton > button:visited {{
            background: {theme['surface']} !important;
            color: {theme['text_primary']} !important;
            border: 1px solid {theme['surface_border']} !important;
        }}
        .stButton > button:hover {{
            background: {theme['surface_hover']} !important;
            border-color: {theme['accent']} !important;
            color: {theme['text_primary']} !important;
        }}
        .stButton > button p {{
            color: inherit !important;
        }}
        .stButton > button[kind="primary"],
        .stButton > button[kind="primaryFormSubmit"] {{
            background: {theme['accent']} !important;
            border: 1px solid {theme['accent']} !important;
            color: #ffffff !important;
        }}
        .stButton > button[kind="primary"]:hover {{
            background: {theme['accent']} !important;
            opacity: 0.9;
            color: #ffffff !important;
        }}
        .stButton > button[kind="primary"] p {{
            color: #ffffff !important;
        }}

        /* ---------- File uploader (dropzone + its internal browse button) ---------- */
        [data-testid="stFileUploaderDropzone"] {{
            background: {theme['input_bg']} !important;
            border: 1px dashed {theme['surface_border']} !important;
            border-radius: 12px;
        }}
        [data-testid="stFileUploaderDropzone"] * {{
            color: {theme['text_secondary']} !important;
        }}
        [data-testid="stFileUploaderDropzone"] button {{
            background: {theme['surface']} !important;
            color: {theme['text_primary']} !important;
            border: 1px solid {theme['surface_border']} !important;
        }}
        [data-testid="stFileUploaderDropzone"] button:hover {{
            background: {theme['surface_hover']} !important;
            border-color: {theme['accent']} !important;
        }}
        [data-testid="stFileUploaderFile"] {{
            background: {theme['surface']} !important;
            border-radius: 8px;
        }}
        [data-testid="stFileUploaderFile"] * {{
            color: {theme['text_primary']} !important;
        }}

        /* ---------- Text input ---------- */
        .stTextInput > div > div {{
            background: {theme['input_bg']} !important;
            border: 1px solid {theme['surface_border']} !important;
        }}
        .stTextInput input {{
            color: {theme['text_primary']} !important;
        }}
        .stTextInput input::placeholder {{
            color: {theme['text_muted']} !important;
        }}

        /* ---------- Glass card ---------- */
        .gp-card {{
            background: {theme['surface']};
            border: 1px solid {theme['surface_border']};
            border-radius: 16px;
            padding: 22px 20px;
            height: 100%;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            box-shadow: {theme['shadow']};
            transition: background 0.15s ease, border-color 0.15s ease;
        }}
        .gp-card:hover {{
            background: {theme['surface_hover']};
            border-color: {theme['accent']};
        }}

        .gp-card-icon {{
            margin-bottom: 14px;
        }}
        .gp-card-title {{
            font-weight: 600;
            font-size: 15px;
            margin-bottom: 6px;
            color: {theme['text_primary']};
            letter-spacing: -0.01em;
        }}
        .gp-card-text {{
            font-size: 13.5px;
            color: {theme['text_secondary']};
            line-height: 1.55;
        }}

        /* ---------- Step badge ---------- */
        .gp-step-num {{
            font-size: 12px;
            font-weight: 700;
            color: {theme['accent']};
            letter-spacing: 0.06em;
            margin-bottom: 10px;
            font-variant-numeric: tabular-nums;
        }}

        /* ---------- Stat card ---------- */
        .gp-stat {{
            background: {theme['surface']};
            border: 1px solid {theme['surface_border']};
            border-radius: 14px;
            padding: 18px 20px;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
        }}
        .gp-stat-value {{
            font-size: 26px;
            font-weight: 700;
            color: {theme['text_primary']};
            letter-spacing: -0.02em;
            font-variant-numeric: tabular-nums;
        }}
        .gp-stat-label {{
            font-size: 12.5px;
            color: {theme['text_muted']};
            margin-top: 2px;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }}

        /* ---------- Section heading ---------- */
        .gp-section-heading {{
            font-weight: 650;
            font-size: 19px;
            margin: 36px 0 14px 0;
            color: {theme['text_primary']};
            letter-spacing: -0.01em;
        }}
        .gp-section-sub {{
            font-size: 13.5px;
            color: {theme['text_muted']};
            margin-top: -10px;
            margin-bottom: 18px;
        }}

        /* ---------- Hero ---------- */
        .gp-hero-title {{
            font-size: 34px;
            font-weight: 700;
            color: {theme['text_primary']};
            letter-spacing: -0.02em;
            margin-bottom: 6px;
        }}
        .gp-hero-sub {{
            font-size: 15.5px;
            color: {theme['text_secondary']};
            max-width: 520px;
            line-height: 1.6;
        }}
        .gp-eyebrow {{
            font-size: 12px;
            font-weight: 650;
            color: {theme['accent']};
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 10px;
        }}

        /* ---------- Sidebar sections ---------- */
        .gp-sidebar-label {{
            font-size: 11.5px;
            font-weight: 650;
            color: {theme['text_muted']};
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin: 18px 0 8px 0;
        }}

        /* ---------- Divider ---------- */
        .gp-divider {{
            height: 1px;
            background: {theme['divider']};
            border: none;
            margin: 28px 0;
        }}

        /* ---------- Chat message polish ---------- */
        [data-testid="stChatMessage"] {{
            background: {theme['surface']};
            border: 1px solid {theme['surface_border']};
            border-radius: 14px;
            backdrop-filter: blur(8px);
        }}

        /* ---------- Buttons ---------- */
        .stButton > button {{
            border-radius: 10px;
            font-weight: 550;
            transition: opacity 0.12s ease;
        }}

        /* ---------- Custom status banners ---------- */
        .gp-banner {{
            border-radius: 10px;
            padding: 12px 14px;
            font-size: 13.5px;
            margin-top: 10px;
        }}
        .gp-banner-success {{
            background: {theme['success_bg']};
            color: {theme['success_text']};
        }}
        .gp-banner-error {{
            background: {theme['error_bg']};
            color: {theme['error_text']};
        }}

        footer {{visibility: hidden;}}
        </style>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# ICONS (inline SVG, stroke color follows theme)
# ============================================================

def get_icons(stroke: str, strong_stroke: str) -> dict:
    return {
        "source": f"""<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="{stroke}" stroke-width="1.7">
            <path d="M4 4h11l5 5v11a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V5a1 1 0 0 1 1-1z"/>
            <path d="M14 4v5h5"/><line x1="7" y1="12" x2="16" y2="12"/><line x1="7" y1="16" x2="13" y2="16"/>
        </svg>""",
        "pin": f"""<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="{stroke}" stroke-width="1.7">
            <path d="M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11z"/><circle cx="12" cy="10" r="2.4"/>
        </svg>""",
        "lock": f"""<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="{stroke}" stroke-width="1.7">
            <rect x="4" y="10" width="16" height="10" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>
        </svg>""",
        "bolt": f"""<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="{stroke}" stroke-width="1.7">
            <polygon points="13 2 3 14 11 14 11 22 21 10 13 10 13 2"/>
        </svg>""",
        "book": f"""<svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="{strong_stroke}" stroke-width="1.6">
            <path d="M4 19.5V4.5A2.5 2.5 0 0 1 6.5 2H20v18H6.5A2.5 2.5 0 0 0 4 22.5"/>
            <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
        </svg>""",
        "folder": f"""<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="{strong_stroke}" stroke-width="1.8" style="vertical-align:-3px; margin-right:6px;">
            <path d="M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V7z"/>
        </svg>""",
        "sun": f"""<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="{strong_stroke}" stroke-width="1.8">
            <circle cx="12" cy="12" r="4.5"/>
            <line x1="12" y1="2" x2="12" y2="4.5"/><line x1="12" y1="19.5" x2="12" y2="22"/>
            <line x1="2" y1="12" x2="4.5" y2="12"/><line x1="19.5" y1="12" x2="22" y2="12"/>
            <line x1="4.9" y1="4.9" x2="6.6" y2="6.6"/><line x1="17.4" y1="17.4" x2="19.1" y2="19.1"/>
            <line x1="4.9" y1="19.1" x2="6.6" y2="17.4"/><line x1="17.4" y1="6.6" x2="19.1" y2="4.9"/>
        </svg>""",
        "moon": f"""<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="{strong_stroke}" stroke-width="1.8">
            <path d="M20 14.5A8.5 8.5 0 1 1 9.5 4a7 7 0 0 0 10.5 10.5z"/>
        </svg>""",
    }


# ============================================================
# SESSION STATE
# ============================================================

def init_session_state() -> None:
    defaults = {
        "theme": "light",
        "processed": False,
        "chat_history": [],
        "num_notes_files": 0,
        "num_pyq_files": 0,
        "total_chunks": 0,
        "last_error": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# ============================================================
# BACKEND CALLS (wrappers only — no logic changes)
# ============================================================

def process_documents(notes_files, pyq_files, pyq_year) -> tuple[bool, str]:
    """
    Runs the exact same ingestion pipeline as before.
    Returns (success, message).
    """
    try:
        clear_vectorstore()
        total_chunks = 0

        for file in notes_files or []:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(file.read())
                tmp_path = tmp.name
            total_chunks += ingest_pdf(tmp_path, doc_type="notes")
            os.unlink(tmp_path)

        if pyq_files:
            year = pyq_year.strip() if pyq_year.strip() else "unknown"
            for file in pyq_files:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(file.read())
                    tmp_path = tmp.name
                metadata = {"year": year, "question_num": "all"}
                total_chunks += ingest_pdf(tmp_path, doc_type="pyq", metadata_extra=metadata)
                os.unlink(tmp_path)

        st.session_state.num_notes_files = len(notes_files) if notes_files else 0
        st.session_state.num_pyq_files = len(pyq_files) if pyq_files else 0
        st.session_state.total_chunks = total_chunks
        st.session_state.processed = True
        st.session_state.chat_history = []
        return True, f"Processed successfully — {total_chunks} chunks stored."
    except Exception as exc:
        return False, f"Something went wrong while processing: {exc}"


def generate_answer(query: str) -> tuple[str, list]:
    """
    Runs the exact same retrieval + generation pipeline as before.
    Returns (answer_text, sources_list).
    """
    try:
        answer, retrieved_chunks, pyq_mention = ask_gemini(query)
        if pyq_mention:
            answer = pyq_mention + "\n\n" + answer
        sources = [extract_citation_info(doc) for doc, _ in retrieved_chunks]
        return answer, sources
    except Exception as exc:
        return f"Error while generating answer: {exc}", []


# ============================================================
# UI: SIDEBAR
# ============================================================

def render_theme_toggle(icons: dict) -> None:
    is_dark = st.session_state.theme == "dark"
    label = "Light mode" if is_dark else "Dark mode"
    icon = icons["sun"] if is_dark else icons["moon"]
    col_icon, col_btn = st.columns([1, 5])
    with col_icon:
        st.markdown(f"<div style='padding-top:8px'>{icon}</div>", unsafe_allow_html=True)
    with col_btn:
        if st.button(label, use_container_width=True, key="theme_toggle"):
            st.session_state.theme = "light" if is_dark else "dark"
            st.rerun()


def render_sidebar(icons: dict) -> None:
    with st.sidebar:
        render_theme_toggle(icons)

        st.markdown(
            f'<div class="gp-sidebar-label">{icons["folder"]}STUDY MATERIALS</div>',
            unsafe_allow_html=True,
        )

        notes_files = st.file_uploader(
            "Class notes (PDF)",
            type="pdf",
            accept_multiple_files=True,
            key="notes_uploader",
        )
        pyq_files = st.file_uploader(
            "Previous year question papers (PDF)",
            type="pdf",
            accept_multiple_files=True,
            key="pyq_uploader",
        )
        pyq_year = st.text_input("Year of uploaded PYQs", placeholder="e.g. 2023")

        process_btn = st.button("Process documents", type="primary", use_container_width=True)

        if process_btn:
            if not notes_files and not pyq_files:
                st.session_state.last_error = "Please upload at least one PDF."
            else:
                with st.spinner("Chunking, embedding, and storing documents..."):
                    success, message = process_documents(notes_files, pyq_files, pyq_year)
                if success:
                    st.session_state.last_error = None
                    st.success(message)
                else:
                    st.session_state.last_error = message

        if st.session_state.last_error:
            st.error(st.session_state.last_error)

        if st.session_state.processed:
            st.markdown('<hr class="gp-divider" style="margin:18px 0;">', unsafe_allow_html=True)
            if st.button("Start new session", use_container_width=True):
                st.session_state.processed = False
                st.session_state.chat_history = []
                st.session_state.num_notes_files = 0
                st.session_state.num_pyq_files = 0
                st.session_state.total_chunks = 0
                st.rerun()


# ============================================================
# UI: LANDING PAGE (pre-processing)
# ============================================================

def render_hero(icons: dict) -> None:
    st.markdown(
        f"""
        <div style="padding: 20px 0 6px 0;">
            <div class="gp-card-icon">{icons['book']}</div>
            <div class="gp-eyebrow">Exam preparation assistant</div>
            <div class="gp-hero-title">ExamGPT</div>
            <div class="gp-hero-sub">
                An assistant that answers strictly from your own notes and past papers,
                with citations for every claim and pattern detection across prior exams.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_steps() -> None:
    st.markdown('<div class="gp-section-heading">How it works</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    for col, (num, title, text) in zip(cols, STEPS):
        with col:
            st.markdown(
                f"""
                <div class="gp-card">
                    <div class="gp-step-num">{num}</div>
                    <div class="gp-card-title">{title}</div>
                    <div class="gp-card-text">{text}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_features(icons: dict) -> None:
    st.markdown('<div class="gp-section-heading">Capabilities</div>', unsafe_allow_html=True)
    cols = st.columns(4)
    for col, (icon_key, title, text) in zip(cols, FEATURES):
        with col:
            st.markdown(
                f"""
                <div class="gp-card">
                    <div class="gp-card-icon">{icons[icon_key]}</div>
                    <div class="gp-card-title">{title}</div>
                    <div class="gp-card-text">{text}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_landing(icons: dict) -> None:
    render_hero(icons)
    render_steps()
    render_features(icons)
    st.markdown('<hr class="gp-divider">', unsafe_allow_html=True)
    st.info("Upload notes and past papers in the sidebar, then click Process documents to begin.")


# ============================================================
# UI: STATS BAR (post-processing)
# ============================================================

def render_stats_bar() -> None:
    stats = [
        (str(st.session_state.num_notes_files), "Notes files"),
        (str(st.session_state.num_pyq_files), "PYQ files"),
        (str(st.session_state.total_chunks), "Chunks indexed"),
        (str(len(st.session_state.chat_history) // 2), "Questions asked"),
    ]
    cols = st.columns(4)
    for col, (value, label) in zip(cols, stats):
        with col:
            st.markdown(
                f"""
                <div class="gp-stat">
                    <div class="gp-stat-value">{value}</div>
                    <div class="gp-stat-label">{label}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ============================================================
# UI: CHAT INTERFACE (post-processing)
# ============================================================

def render_chat_history() -> None:
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("sources"):
                with st.expander("Sources"):
                    for src in msg["sources"]:
                        st.markdown(f"- {src}")


def render_chat_input() -> None:
    query = st.chat_input("Ask a question about your study materials...")
    if not query:
        return

    st.session_state.chat_history.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.spinner("Thinking..."):
        answer, sources = generate_answer(query)

    with st.chat_message("assistant"):
        st.markdown(answer)
        if sources:
            with st.expander("Sources"):
                for src in sources:
                    st.markdown(f"- {src}")

    st.session_state.chat_history.append(
        {"role": "assistant", "content": answer, "sources": sources}
    )


def render_workspace(icons: dict) -> None:
    st.markdown(
        f"""
        <div style="display:flex; align-items:center; gap:10px; padding: 12px 0 4px 0;">
            {icons['book']}
            <div class="gp-hero-title" style="font-size:26px; margin-bottom:0;">ExamGPT</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption("Grounded answers from your uploaded materials")

    render_stats_bar()
    st.markdown('<hr class="gp-divider">', unsafe_allow_html=True)

    render_chat_history()
    render_chat_input()


# ============================================================
# MAIN
# ============================================================

def main() -> None:
    st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout="wide")
    init_session_state()

    theme = get_theme(st.session_state.theme)
    inject_css(theme)
    icons = get_icons(stroke=theme["icon_stroke"], strong_stroke=theme["text_primary"])

    render_sidebar(icons)

    if st.session_state.processed:
        render_workspace(icons)
    else:
        render_landing(icons)

    st.markdown('<hr class="gp-divider">', unsafe_allow_html=True)
    st.caption("ExamGPT — built with RAG, Gemini, and Streamlit.")


if __name__ == "__main__":
    main()