"""
app.py — Amazon-style Streamlit frontend for OTDS Review Intelligence

Run:  streamlit run app.py
"""

import sys
from pathlib import Path

import streamlit as st

# ── Import search engine from scripts/ ────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).resolve().parent / "scripts"))
from search import search_and_summarize   # noqa: E402

# ── Page config ───────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Amazon OTDS — Review Intelligence",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════════════════════════
#  AMAZON-STYLE CSS
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Amazon+Ember:wght@400;500;700&family=Inter:wght@400;500;600;700&display=swap');

    :root {
        --amz-orange:    #FF9900;
        --amz-orange-dk: #E88B00;
        --amz-navy:      #232F3E;
        --amz-navy-lt:   #37475A;
        --amz-blue:      #007185;
        --amz-blue-hov:  #C7511F;
        --amz-star:      #FFA41C;
        --amz-bg:        #EAEDED;
        --amz-white:     #FFFFFF;
        --amz-text:      #0F1111;
        --amz-text-sec:  #565959;
        --amz-border:    #D5D9D9;
        --amz-green:     #067D62;
        --amz-red:       #B12704;
    }

    * { font-family: 'Inter', 'Amazon Ember', Arial, sans-serif; }

    /* ── Page background ─────────────────────────────── */
    .stApp {
        background: var(--amz-bg) !important;
    }

    /* ── Top nav bar ─────────────────────────────────── */
    .amz-navbar {
        background: var(--amz-navy);
        padding: 0.6rem 2rem;
        margin: -1rem -1rem 0 -1rem;
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }
    .amz-logo {
        font-size: 1.6rem;
        font-weight: 700;
        color: var(--amz-white);
        letter-spacing: -0.5px;
    }
    .amz-logo span {
        color: var(--amz-orange);
    }

    /* ── Search bar container ────────────────────────── */
    .search-wrapper {
        background: var(--amz-white);
        border-radius: 8px;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        border: 1px solid var(--amz-border);
    }
    .stTextInput > div > div > input {
        background: var(--amz-white) !important;
        border: 2px solid var(--amz-border) !important;
        border-radius: 6px !important;
        color: var(--amz-text) !important;
        padding: 0.65rem 1rem !important;
        font-size: 0.95rem !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: var(--amz-orange) !important;
        box-shadow: 0 0 0 3px rgba(255,153,0,0.15) !important;
    }

    /* ── Search button (Amazon-orange) ───────────────── */
    .stButton > button {
        background: linear-gradient(to bottom, #f7dfa5, #f0c14b) !important;
        color: var(--amz-text) !important;
        border: 1px solid #a88734 !important;
        border-radius: 6px !important;
        padding: 0.55rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        transition: background 0.15s ease !important;
    }
    .stButton > button:hover {
        background: linear-gradient(to bottom, #f5d78e, #eeb933) !important;
        transform: none !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.15) !important;
    }

    /* ── Metadata pills ──────────────────────────────── */
    .meta-bar {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        flex-wrap: wrap;
        margin: 0.8rem 0;
    }
    .pill {
        display: inline-block;
        padding: 0.2rem 0.65rem;
        border-radius: 4px;
        font-size: 0.78rem;
        font-weight: 500;
        letter-spacing: 0.2px;
    }
    .pill-topic {
        background: #EAF4F4;
        color: var(--amz-blue);
        border: 1px solid #B5D5D5;
    }
    .pill-positive {
        background: #E8F5E9;
        color: var(--amz-green);
        border: 1px solid #A5D6A7;
    }
    .pill-negative {
        background: #FBE9E7;
        color: var(--amz-red);
        border: 1px solid #FFAB91;
    }
    .pill-neutral {
        background: #F5F5F5;
        color: var(--amz-text-sec);
        border: 1px solid var(--amz-border);
    }

    /* ── Answer box (Featured Result) ────────────────── */
    .answer-box {
        background: var(--amz-white);
        border: 1px solid var(--amz-border);
        border-left: 4px solid var(--amz-orange);
        border-radius: 8px;
        padding: 1.2rem 1.5rem;
        margin: 0.8rem 0 1.2rem 0;
        font-size: 0.98rem;
        line-height: 1.7;
        color: var(--amz-text);
    }
    .answer-box strong {
        color: var(--amz-navy);
    }

    /* ── Section headers ─────────────────────────────── */
    .section-hdr {
        font-size: 1.15rem;
        font-weight: 700;
        color: var(--amz-text);
        margin: 1.5rem 0 0.6rem 0;
        padding-bottom: 0.4rem;
        border-bottom: 2px solid var(--amz-orange);
        display: inline-block;
    }

    /* ── Insight card ─────────────────────────────────── */
    .insight-card {
        background: var(--amz-white);
        border: 1px solid var(--amz-border);
        border-radius: 8px;
        padding: 0.85rem 1.2rem;
        margin: 0.4rem 0;
        color: var(--amz-text);
        font-size: 0.92rem;
        line-height: 1.6;
        display: flex;
        align-items: flex-start;
        gap: 0.5rem;
    }
    .insight-icon {
        color: var(--amz-blue);
        font-size: 1.1rem;
        flex-shrink: 0;
        margin-top: 1px;
    }

    /* ── Product result card ──────────────────────────── */
    .result-card {
        background: var(--amz-white);
        border: 1px solid var(--amz-border);
        border-radius: 8px;
        padding: 1rem 1.3rem;
        margin: 0.6rem 0;
        transition: box-shadow 0.2s ease, border-color 0.2s ease;
    }
    .result-card:hover {
        border-color: #B5B5B5;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .result-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 0.35rem;
    }
    .result-name {
        font-weight: 600;
        font-size: 1rem;
        color: var(--amz-blue);
        text-decoration: none;
        cursor: pointer;
    }
    .result-name:hover {
        color: var(--amz-blue-hov);
        text-decoration: underline;
    }
    .result-score {
        font-size: 0.75rem;
        color: var(--amz-text-sec);
        background: #F0F2F2;
        padding: 0.15rem 0.5rem;
        border-radius: 4px;
        white-space: nowrap;
    }
    .result-stars {
        display: flex;
        align-items: center;
        gap: 0.15rem;
        margin-bottom: 0.4rem;
    }
    .star {
        color: var(--amz-star);
        font-size: 0.95rem;
    }
    .star-empty {
        color: #D5D9D9;
        font-size: 0.95rem;
    }
    .rating-text {
        font-size: 0.8rem;
        color: var(--amz-text-sec);
        margin-left: 0.4rem;
    }
    .result-text {
        color: var(--amz-text);
        font-size: 0.9rem;
        line-height: 1.6;
        margin-bottom: 0.5rem;
    }
    .result-footer {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        flex-wrap: wrap;
    }
    .badge-topic {
        display: inline-block;
        background: #F0F2F2;
        color: var(--amz-text-sec);
        padding: 0.15rem 0.55rem;
        border-radius: 4px;
        font-size: 0.72rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .badge-sentiment {
        display: inline-block;
        padding: 0.15rem 0.55rem;
        border-radius: 4px;
        font-size: 0.72rem;
        font-weight: 600;
    }
    .badge-positive {
        background: #E8F5E9;
        color: var(--amz-green);
    }
    .badge-negative {
        background: #FBE9E7;
        color: var(--amz-red);
    }
    .badge-neutral {
        background: #FFF3E0;
        color: #E65100;
    }
    .badge-pid {
        font-size: 0.72rem;
        color: #888;
    }

    /* ── Stats row ────────────────────────────────────── */
    .stats-row {
        display: flex;
        gap: 1rem;
        margin: 0.8rem 0 1rem 0;
    }
    .stat-box {
        background: var(--amz-white);
        border: 1px solid var(--amz-border);
        border-radius: 8px;
        padding: 0.7rem 1.2rem;
        text-align: center;
        flex: 1;
    }
    .stat-val {
        font-size: 1.4rem;
        font-weight: 700;
        color: var(--amz-navy);
    }
    .stat-label {
        font-size: 0.75rem;
        color: var(--amz-text-sec);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 0.15rem;
    }

    /* ── Example query chips ─────────────────────────── */
    .examples-container {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-top: 0.5rem;
    }
    div[data-testid="stHorizontalBlock"] .stButton > button {
        background: var(--amz-white) !important;
        border: 1px solid var(--amz-border) !important;
        color: var(--amz-text) !important;
        font-weight: 400 !important;
        font-size: 0.82rem !important;
        padding: 0.35rem 0.9rem !important;
        border-radius: 20px !important;
    }
    div[data-testid="stHorizontalBlock"] .stButton > button:hover {
        border-color: var(--amz-orange) !important;
        color: var(--amz-orange) !important;
        background: #FFF8F0 !important;
        box-shadow: none !important;
    }

    /* ── Empty state ──────────────────────────────────── */
    .empty-state {
        text-align: center;
        padding: 3rem 1rem;
        color: var(--amz-text-sec);
    }
    .empty-icon {
        font-size: 3rem;
        margin-bottom: 0.8rem;
    }

    /* ── Footer ───────────────────────────────────────── */
    .amz-footer {
        text-align: center;
        color: var(--amz-text-sec);
        font-size: 0.75rem;
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid var(--amz-border);
    }

    hr { border-color: var(--amz-border) !important; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════════════════════


def render_stars(rating: int, max_stars: int = 5) -> str:
    """Generate HTML for Amazon-style star rating."""
    filled = '★' * rating
    empty  = '★' * (max_stars - rating)
    return (f'<span class="star">{filled}</span>'
            f'<span class="star-empty">{empty}</span>'
            f'<span class="rating-text">{rating}.0 out of 5</span>')


def sentiment_pill(sent: str) -> str:
    """Return pill HTML for a sentiment label."""
    css = {"positive": "pill-positive", "negative": "pill-negative"}
    cls = css.get(sent, "pill-neutral")
    icon = {"positive": "👍", "negative": "👎"}.get(sent, "➖")
    return f'<span class="pill {cls}">{icon} {sent}</span>'


def sentiment_badge(sent: str) -> str:
    """Inline badge for result card."""
    cls = f"badge-{sent}" if sent in ("positive", "negative", "neutral") else "badge-neutral"
    label = {"positive": "✓ Positive", "negative": "✗ Negative"}.get(sent, "~ Mixed")
    return f'<span class="badge-sentiment {cls}">{label}</span>'


# ══════════════════════════════════════════════════════════════════════════════
#  LAYOUT
# ══════════════════════════════════════════════════════════════════════════════


# ── Nav bar ───────────────────────────────────────────────────────────────────

st.markdown("""
<div class="amz-navbar">
    <div class="amz-logo">📦 Amazon <span>OTDS</span></div>
    <div style="color: #CCC; font-size: 0.85rem;">AI-Powered Review Intelligence</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height: 0.8rem'></div>", unsafe_allow_html=True)

# ── Search bar ────────────────────────────────────────────────────────────────

col_input, col_btn = st.columns([5, 1])

with col_input:
    query = st.text_input(
        "search",
        placeholder="🔍  Search reviews...  e.g.  good battery life,  fan noise,  heating issues",
        label_visibility="collapsed",
    )

with col_btn:
    search_clicked = st.button("🔍 Search", use_container_width=True)

# ── Example queries ───────────────────────────────────────────────────────────

if not query and "auto_query" not in st.session_state:
    st.markdown("---")
    st.markdown('<div class="section-hdr">💡 Try a search</div>', unsafe_allow_html=True)

    examples = [
        "great battery life",
        "bad battery life",
        "fan noise issues",
        "overheating laptop",
        "good performance",
        "best display quality",
    ]
    cols = st.columns(3)
    for i, ex in enumerate(examples):
        with cols[i % 3]:
            if st.button(ex, key=f"ex_{i}", use_container_width=True):
                st.session_state["auto_query"] = ex
                st.rerun()

    # Empty state
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">🔍</div>
        <div style="font-size:1.1rem; font-weight:600; color:#232F3E; margin-bottom:0.3rem;">
            Search Customer Reviews
        </div>
        <div>Enter a query above to find relevant product reviews powered by AI semantic search.</div>
    </div>
    """, unsafe_allow_html=True)


# ── Pick up example click ─────────────────────────────────────────────────────

if "auto_query" in st.session_state:
    query = st.session_state.pop("auto_query")

# ══════════════════════════════════════════════════════════════════════════════
#  RESULTS
# ══════════════════════════════════════════════════════════════════════════════

if query and query.strip():
    with st.spinner("Searching reviews …"):
        data = search_and_summarize(query.strip())

    meta    = data["metadata"]
    results = data["results"]

    # ── Metadata pills ────────────────────────────────────────────────────

    pills_html = '<div class="meta-bar">'
    for tp in meta["topics"]:
        pills_html += f'<span class="pill pill-topic">📌 {tp}</span>'
        sent = meta["topic_sentiments"].get(tp, "neutral")
        pills_html += sentiment_pill(sent)
    pills_html += f'<span class="pill pill-neutral">📊 {len(results)} products</span>'
    pills_html += '</div>'
    st.markdown(pills_html, unsafe_allow_html=True)

    # ── Stats row ─────────────────────────────────────────────────────────

    if results:
        pos_count = sum(1 for r in results if r.get("sentiment_label") == "positive")
        neg_count = sum(1 for r in results if r.get("sentiment_label") == "negative")
        avg_rating = sum(r["rating"] for r in results) / len(results)

        st.markdown(f"""
        <div class="stats-row">
            <div class="stat-box">
                <div class="stat-val">{len(results)}</div>
                <div class="stat-label">Products Found</div>
            </div>
            <div class="stat-box">
                <div class="stat-val" style="color: var(--amz-star);">{'★' * round(avg_rating)} {avg_rating:.1f}</div>
                <div class="stat-label">Avg Rating</div>
            </div>
            <div class="stat-box">
                <div class="stat-val" style="color: var(--amz-green);">{pos_count}</div>
                <div class="stat-label">Positive</div>
            </div>
            <div class="stat-box">
                <div class="stat-val" style="color: var(--amz-red);">{neg_count}</div>
                <div class="stat-label">Negative</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Final Answer ──────────────────────────────────────────────────────

    if data["final_answer"]:
        st.markdown('<div class="section-hdr">✨ AI Summary</div>',
                    unsafe_allow_html=True)
        st.markdown(
            f'<div class="answer-box">{data["final_answer"]}</div>',
            unsafe_allow_html=True,
        )

    # ── Key Insights ──────────────────────────────────────────────────────

    if data["summary"]:
        st.markdown('<div class="section-hdr">📋 Key Insights</div>',
                    unsafe_allow_html=True)
        for bullet in data["summary"]:
            st.markdown(
                f'<div class="insight-card">'
                f'<span class="insight-icon">▸</span>'
                f'<span>{bullet}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

    # ── Top Matches ───────────────────────────────────────────────────────

    if results:
        st.markdown(
            f'<div class="section-hdr">📦 Customer Reviews ({len(results)} results)</div>',
            unsafe_allow_html=True,
        )

        for r in results:
            stars_html = render_stars(r["rating"])
            sent_html  = sentiment_badge(r.get("sentiment_label", "neutral"))
            topic_html = f'<span class="badge-topic">{r["topic"]}</span>'
            pid_html   = f'<span class="badge-pid">{r["product_id"]}</span>'
            score_html = f'<span class="result-score">Score: {r["score"]:.4f}</span>'

            st.markdown(f"""
            <div class="result-card">
                <div class="result-header">
                    <span class="result-name">{r["product_name"]}</span>
                    {score_html}
                </div>
                <div class="result-stars">{stars_html}</div>
                <div class="result-text">{r["text"]}</div>
                <div class="result-footer">
                    {topic_html}
                    {sent_html}
                    {pid_html}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Empty state ───────────────────────────────────────────────────────

    if not results:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">🤷</div>
            <div>No results found. Try a different query.</div>
        </div>
        """, unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────

st.markdown("""
<div class="amz-footer">
    Amazon OTDS · AI Review Intelligence · Semantic Search + Re-ranking · Built with Qdrant & Sentence-Transformers
</div>
""", unsafe_allow_html=True)
