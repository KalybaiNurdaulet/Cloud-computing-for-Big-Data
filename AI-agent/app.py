"""
app.py — B2B AI Lead Intelligence Tool
R2F Streamlit Interface. No OpenAI imports — delegates entirely to processor.py.
"""

import streamlit as st
from processor import analyze_lead

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="B2B Lead Intelligence Tool",
    page_icon="🎯",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Custom CSS — premium dark theme
# ---------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* App background */
.stApp {
    background: linear-gradient(135deg, #0d0d1a 0%, #141428 50%, #111827 100%);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.03);
    border-right: 1px solid rgba(255,255,255,0.07);
}
section[data-testid="stSidebar"] * {
    color: #cbd5e1 !important;
}

/* Hero */
.hero-title {
    font-size: 2.2rem;
    font-weight: 700;
    background: linear-gradient(90deg, #a78bfa 0%, #60a5fa 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.2;
}
.hero-sub {
    color: #64748b;
    font-size: 0.95rem;
    margin-top: 0.4rem;
    margin-bottom: 1.5rem;
}

/* Metric cards */
.metric-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    text-align: center;
}
.metric-label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.09em;
    text-transform: uppercase;
    color: #64748b;
    margin-bottom: 0.5rem;
}
.metric-value {
    font-size: 2.6rem;
    font-weight: 700;
    line-height: 1;
}
.metric-value.high  { color: #34d399; }
.metric-value.mid   { color: #fbbf24; }
.metric-value.low   { color: #f87171; }
.metric-value.budget { font-size: 1.5rem; color: #93c5fd; }

/* Priority banner */
.priority-banner {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    padding: 0.9rem 1.4rem;
    border-radius: 10px;
    font-weight: 600;
    font-size: 0.95rem;
    margin-bottom: 1.2rem;
}
.priority-high { background: rgba(16,185,129,0.12); border: 1px solid rgba(16,185,129,0.3); color: #34d399; }
.priority-mid  { background: rgba(245,158,11,0.12); border: 1px solid rgba(245,158,11,0.3); color: #fbbf24; }
.priority-low  { background: rgba(239,68,68,0.12);  border: 1px solid rgba(239,68,68,0.3);  color: #f87171; }

/* Info cards */
.info-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 1.1rem 1.4rem;
    margin-bottom: 0.8rem;
}
.info-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.09em;
    text-transform: uppercase;
    color: #64748b;
    margin-bottom: 0.35rem;
}
.info-value { color: #e2e8f0; font-size: 0.95rem; line-height: 1.5; }

/* Flag pills */
.flag { display: inline-block; background: rgba(239,68,68,0.13); border: 1px solid rgba(239,68,68,0.3);
        color: #fca5a5; border-radius: 999px; padding: 0.22rem 0.8rem; font-size: 0.8rem;
        margin: 0.18rem 0.15rem 0 0; }
.ok   { color: #34d399; font-size: 0.9rem; }

/* Text area */
textarea { border-radius: 10px !important; background: rgba(255,255,255,0.03) !important; }

/* Button */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #7c3aed, #4f46e5);
    color: white !important;
    border: none;
    border-radius: 10px;
    padding: 0.75rem;
    font-size: 1rem;
    font-weight: 600;
    letter-spacing: 0.02em;
    transition: opacity 0.2s, transform 0.1s;
}
.stButton > button:hover { opacity: 0.85; transform: translateY(-1px); }
.stButton > button:active { transform: translateY(0); }

hr { border-color: rgba(255,255,255,0.05); }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🎯 Lead Intelligence")
    st.markdown("---")

    st.markdown("#### 🔑 Groq API Key")
    api_key_input = st.text_input(
        label="Groq API Key",
        type="password",
        value="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",
        placeholder="gsk_...",
        help="Paste your Groq API key.",
        label_visibility="collapsed",
    )
    if api_key_input:
        st.success("API key loaded ✓", icon="✅")
    else:
        st.warning("Please enter your Groq API key above.")

    st.markdown("---")
    st.markdown("#### ℹ️ About")
    st.markdown(
        """
        **B2B AI Lead Intelligence Tool** helps SMEs instantly triage raw client inquiries.

        Instead of spending hours manually reading emails, paste any inquiry and get:
        - 📊 A **priority score** (1–10)
        - 💰 The **estimated budget** extracted automatically
        - 📝 A **one-sentence summary**
        - 🚩 **Red flags** like vague scope or unrealistic deadlines

        **Saves 5–10 hours of manual vetting per week.**

        *Powered by Groq llama-3.3-70b-versatile · IT4IT R2F Layer*
        """
    )


# ---------------------------------------------------------------------------
# Main area — Header
# ---------------------------------------------------------------------------
st.markdown('<p class="hero-title">🎯 B2B Lead Intelligence Tool</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="hero-sub">Paste a raw client inquiry or email. '
    'The AI extracts key data and scores the lead in seconds.</p>',
    unsafe_allow_html=True,
)
st.markdown("---")

# ---------------------------------------------------------------------------
# Input
# ---------------------------------------------------------------------------
inquiry = st.text_area(
    label="📋 Paste the B2B inquiry or email here",
    placeholder=(
        'Example:\n\n'
        '"Hi, I\'m James from Meridian Consulting. We need a custom data dashboard '
        'for our finance team (12 users). Our budget is around $20,000 and we have '
        'a board presentation in 8 weeks. Can you help?"'
    ),
    height=220,
)

process_clicked = st.button("⚡ Process Lead", use_container_width=True)

# ---------------------------------------------------------------------------
# Processing & Results
# ---------------------------------------------------------------------------
if process_clicked:
    if not inquiry or not inquiry.strip():
        st.warning("⚠️ Please paste a lead inquiry before processing.")
        st.stop()

    with st.spinner("Analyzing with Groq llama-3.3-70b-versatile — this takes a few seconds…"):
        result, error, stats = analyze_lead(
            inquiry_text=inquiry.strip(),
            api_key=api_key_input.strip() if api_key_input else None,
        )

    if error:
        st.error(f"❌ {error}")
        if stats:
            st.caption(
                f"Tokens used before error: {stats.total_tokens} · "
                f"Estimated cost: {stats.cost_display}"
            )
        st.stop()

    st.markdown("---")
    st.markdown("### 📊 Lead Analysis Results")

    # --- Priority banner ---
    score = result.priority_score
    if score >= 7:
        banner_cls, banner_icon, banner_label = "priority-high", "🟢", "High Priority — Act Immediately"
    elif score >= 4:
        banner_cls, banner_icon, banner_label = "priority-mid",  "🟡", "Medium Priority — Qualify Further"
    else:
        banner_cls, banner_icon, banner_label = "priority-low",  "🔴", "Low Priority — Likely a Tire-Kicker"

    st.markdown(
        f'<div class="priority-banner {banner_cls}">'
        f'{banner_icon} &nbsp; {banner_label}'
        f'</div>',
        unsafe_allow_html=True,
    )

    # --- Metric columns ---
    col1, col2, col3 = st.columns(3)

    score_class = "high" if score >= 7 else ("mid" if score >= 4 else "low")
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Priority Score</div>
            <div class="metric-value {score_class}">{score}<span style="font-size:1rem;color:#64748b"> / 10</span></div>
        </div>""", unsafe_allow_html=True)

    with col2:
        budget_display = result.estimated_budget
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Estimated Budget</div>
            <div class="metric-value budget">{budget_display}</div>
        </div>""", unsafe_allow_html=True)

    with col3:
        flag_count = len(result.red_flags)
        flag_color = "#f87171" if flag_count > 0 else "#34d399"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Red Flags</div>
            <div class="metric-value" style="color:{flag_color};">{flag_count}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Info cards ---
    st.markdown(f"""
    <div class="info-card">
        <div class="info-label">Client</div>
        <div class="info-value">{result.client_name}</div>
    </div>
    <div class="info-card">
        <div class="info-label">Project Summary</div>
        <div class="info-value">{result.project_summary}</div>
    </div>
    """, unsafe_allow_html=True)

    # --- Red flags ---
    st.markdown('<div class="info-card"><div class="info-label">Red Flags</div><div class="info-value">', unsafe_allow_html=True)
    if result.red_flags:
        pills = "".join(f'<span class="flag">⚑ {f}</span>' for f in result.red_flags)
        st.markdown(pills + "</div></div>", unsafe_allow_html=True)
    else:
        st.markdown('<span class="ok">✔ None detected — clean inquiry</span></div></div>', unsafe_allow_html=True)

    st.markdown("---")

    # --- FinOps / D2C cost panel ---
    if stats:
        with st.expander("📊 FinOps — Token Usage & Cost Breakdown", expanded=False):
            fc1, fc2, fc3, fc4 = st.columns(4)
            fc1.metric("Prompt Tokens",     stats.prompt_tokens)
            fc2.metric("Completion Tokens", stats.completion_tokens)
            fc3.metric("Total Tokens",      stats.total_tokens)
            fc4.metric("Est. Cost (USD)",   stats.cost_display)
            st.caption(
                "Pricing: $0.59 / 1M input tokens · $0.79 / 1M output tokens "
                "(llama-3.3-70b-versatile, April 2025). All sessions logged to `activity.log`."
            )

    st.caption("Groq-powered Lead Intelligence · llama-3.3-70b-versatile · IT4IT R2F + D2C Layer")
