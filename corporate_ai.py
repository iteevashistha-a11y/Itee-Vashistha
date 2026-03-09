import streamlit as st
from datetime import datetime

# ── PAGE CONFIG ──
st.set_page_config(
    page_title="Corporate AI Adoption Survey",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── CUSTOM CSS ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');

:root {
    --ink: #0A0A0F;
    --deep: #111827;
    --purple: #4F46E5;
    --violet: #7C3AED;
    --cyan: #06B6D4;
    --emerald: #10B981;
    --amber: #F59E0B;
    --rose: #F43F5E;
    --surface: #F9FAFB;
    --card: #FFFFFF;
    --border: #E5E7EB;
    --muted: #6B7280;
    --text: #111827;
}

html, body, [data-testid="stAppViewContainer"] {
    background: #F0F2F8 !important;
    font-family: 'IBM Plex Sans', sans-serif;
}

#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }
[data-testid="stSidebar"] { display: none; }

/* ── HERO ── */
.hero {
    background: linear-gradient(135deg, #0A0A0F 0%, #111827 40%, #1E1B4B 100%);
    border-radius: 24px;
    padding: 56px 60px 48px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: "";
    position: absolute;
    top: -60px; right: -60px;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(79,70,229,0.3) 0%, transparent 70%);
    border-radius: 50%;
}
.hero::after {
    content: "";
    position: absolute;
    bottom: -40px; left: 30%;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(6,182,212,0.15) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(79,70,229,0.15);
    border: 1px solid rgba(79,70,229,0.4);
    color: #818CF8;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 5px 14px;
    border-radius: 20px;
    margin-bottom: 20px;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 46px;
    font-weight: 800;
    color: white;
    line-height: 1.1;
    margin: 0 0 12px 0;
}
.hero-title span { color: #818CF8; }
.hero-sub {
    font-size: 15px;
    color: rgba(255,255,255,0.55);
    margin: 0;
    font-weight: 300;
    max-width: 600px;
    line-height: 1.7;
}
.hero-stats {
    display: flex;
    gap: 32px;
    margin-top: 36px;
    position: relative;
    z-index: 2;
}
.hero-stat {
    text-align: left;
}
.hero-stat-num {
    font-family: 'Syne', sans-serif;
    font-size: 28px;
    font-weight: 800;
    color: #818CF8;
    line-height: 1;
}
.hero-stat-label {
    font-size: 12px;
    color: rgba(255,255,255,0.4);
    margin-top: 4px;
    letter-spacing: 0.3px;
}

/* ── SECTION HEADERS ── */
.sec-head {
    display: flex;
    align-items: center;
    gap: 14px;
    margin: 40px 0 20px 0;
}
.sec-icon {
    width: 44px; height: 44px;
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px;
    flex-shrink: 0;
}
.sec-icon-purple { background: rgba(79,70,229,0.12); }
.sec-icon-cyan { background: rgba(6,182,212,0.12); }
.sec-icon-emerald { background: rgba(16,185,129,0.12); }
.sec-icon-amber { background: rgba(245,158,11,0.12); }
.sec-icon-rose { background: rgba(244,63,94,0.12); }
.sec-icon-violet { background: rgba(124,58,237,0.12); }
.sec-title {
    font-family: 'Syne', sans-serif;
    font-size: 20px;
    font-weight: 700;
    color: var(--text);
}
.sec-sub {
    font-size: 13px;
    color: var(--muted);
    margin-top: 2px;
}
.sec-line {
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, var(--border), transparent);
}

/* ── CARDS ── */
.q-card {
    background: white;
    border-radius: 16px;
    padding: 22px 24px;
    margin-bottom: 14px;
    border: 1px solid var(--border);
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    transition: box-shadow 0.2s, border-color 0.2s;
}
.q-card:hover {
    box-shadow: 0 4px 16px rgba(79,70,229,0.08);
    border-color: rgba(79,70,229,0.2);
}
.q-badge {
    display: inline-block;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 6px;
    margin-bottom: 8px;
}
.badge-purple { background: rgba(79,70,229,0.1); color: #4F46E5; }
.badge-cyan { background: rgba(6,182,212,0.1); color: #06B6D4; }
.badge-emerald { background: rgba(16,185,129,0.1); color: #10B981; }
.badge-amber { background: rgba(245,158,11,0.1); color: #D97706; }
.badge-rose { background: rgba(244,63,94,0.1); color: #F43F5E; }
.badge-violet { background: rgba(124,58,237,0.1); color: #7C3AED; }
.q-text {
    font-size: 15px;
    font-weight: 600;
    color: var(--text);
    line-height: 1.5;
    margin: 0 0 14px 0;
}
.q-hint {
    font-size: 12px;
    color: var(--muted);
    margin-bottom: 12px;
    font-style: italic;
}

/* ── PROGRESS ── */
.prog-wrap {
    background: white;
    border-radius: 14px;
    padding: 18px 24px;
    margin-bottom: 28px;
    border: 1px solid var(--border);
    display: flex;
    align-items: center;
    gap: 16px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
.prog-label { font-size: 13px; font-weight: 600; color: var(--text); white-space: nowrap; }
.prog-outer { flex: 1; background: #F3F4F6; border-radius: 6px; height: 6px; overflow: hidden; }
.prog-inner { height: 100%; border-radius: 6px; background: linear-gradient(90deg, #4F46E5, #7C3AED, #06B6D4); transition: width 0.4s; }
.prog-pct { font-size: 14px; font-weight: 700; color: #4F46E5; min-width: 38px; text-align: right; }

/* ── SUBMIT ── */
div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #4F46E5, #7C3AED) !important;
    color: white !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    padding: 14px 40px !important;
    border-radius: 12px !important;
    border: none !important;
    width: 100% !important;
    box-shadow: 0 4px 20px rgba(79,70,229,0.35) !important;
    letter-spacing: 0.3px !important;
    transition: all 0.3s !important;
}
div[data-testid="stButton"] > button:hover {
    background: linear-gradient(135deg, #4338CA, #6D28D9) !important;
    box-shadow: 0 6px 28px rgba(79,70,229,0.45) !important;
    transform: translateY(-1px) !important;
}

/* ── INPUTS ── */
div[data-testid="stRadio"] div[role="radiogroup"] { gap: 6px !important; }
div[data-testid="stRadio"] label {
    background: #F9FAFB !important;
    border: 1.5px solid #E5E7EB !important;
    border-radius: 10px !important;
    padding: 10px 16px !important;
    font-size: 14px !important;
    font-weight: 400 !important;
    color: var(--text) !important;
    transition: all 0.15s !important;
    cursor: pointer !important;
}
div[data-testid="stRadio"] label:hover {
    border-color: #4F46E5 !important;
    background: rgba(79,70,229,0.04) !important;
}
div[data-testid="stMultiSelect"] > div > div {
    border-radius: 10px !important;
    border: 1.5px solid #E5E7EB !important;
    font-size: 14px !important;
    background: #F9FAFB !important;
}
div[data-testid="stTextArea"] textarea {
    border-radius: 12px !important;
    border: 1.5px solid #E5E7EB !important;
    font-size: 14px !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
    background: #F9FAFB !important;
    padding: 12px 16px !important;
}
div[data-testid="stTextArea"] textarea:focus {
    border-color: #4F46E5 !important;
    background: white !important;
    box-shadow: 0 0 0 3px rgba(79,70,229,0.1) !important;
}
div[data-testid="stSelectbox"] > div > div {
    border-radius: 10px !important;
    border: 1.5px solid #E5E7EB !important;
    background: #F9FAFB !important;
    font-size: 14px !important;
}
div[data-testid="stSlider"] { padding: 4px 0; }

/* ── SUCCESS ── */
.success-wrap {
    background: linear-gradient(135deg, #0A0A0F, #1E1B4B);
    border-radius: 24px;
    padding: 60px 40px;
    text-align: center;
    color: white;
    box-shadow: 0 12px 48px rgba(79,70,229,0.3);
}
.success-emoji { font-size: 72px; margin-bottom: 20px; }
.success-title {
    font-family: 'Syne', sans-serif;
    font-size: 36px;
    font-weight: 800;
    margin-bottom: 14px;
}
.success-title span { color: #818CF8; }
.success-body { font-size: 16px; color: rgba(255,255,255,0.6); line-height: 1.7; max-width: 500px; margin: 0 auto; }
.success-ref {
    display: inline-block;
    background: rgba(79,70,229,0.2);
    border: 1px solid rgba(79,70,229,0.4);
    color: #818CF8;
    padding: 8px 22px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 600;
    margin-top: 24px;
    letter-spacing: 1px;
}

/* ── CHIP TAGS ── */
.chip-row { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 4px; }
.chip {
    background: rgba(79,70,229,0.08);
    border: 1px solid rgba(79,70,229,0.2);
    color: #4F46E5;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 500;
}

/* Info note */
.info-note {
    background: rgba(79,70,229,0.05);
    border: 1px solid rgba(79,70,229,0.15);
    border-left: 3px solid #4F46E5;
    border-radius: 10px;
    padding: 14px 18px;
    font-size: 13px;
    color: var(--muted);
    margin-bottom: 24px;
    line-height: 1.6;
}

[data-testid="column"] { padding: 0 6px !important; }
</style>
""", unsafe_allow_html=True)


# ── HELPERS ──
def sec(icon, icon_color, title, subtitle):
    st.markdown(f"""
    <div class="sec-head">
        <div class="sec-icon sec-icon-{icon_color}">{icon}</div>
        <div>
            <div class="sec-title">{title}</div>
            <div class="sec-sub">{subtitle}</div>
        </div>
        <div class="sec-line"></div>
    </div>
    """, unsafe_allow_html=True)

def qstart(badge_color, badge_text, question, hint=""):
    st.markdown(f"""
    <div class="q-card">
        <span class="q-badge badge-{badge_color}">{badge_text}</span>
        <p class="q-text">{question}</p>
        {"<p class='q-hint'>"+hint+"</p>" if hint else ""}
    """, unsafe_allow_html=True)

def qend():
    st.markdown("</div>", unsafe_allow_html=True)


# ── SESSION STATE ──
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "responses" not in st.session_state:
    st.session_state.responses = {}


# ══════════════════════════════════════
# SUCCESS SCREEN
# ══════════════════════════════════════
if st.session_state.submitted:
    ref = datetime.now().strftime("CAI-%Y%m%d-%H%M%S")
    st.markdown(f"""
    <div class="success-wrap">
        <div class="success-emoji">🤖</div>
        <div class="success-title">Response <span>Recorded!</span></div>
        <div class="success-body">
            Thank you for sharing your organization's AI journey with us.<br>
            Your insights will help shape the future of enterprise AI adoption in India.
        </div>
        <div class="success-ref">REF: {ref}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("📊 View Your Submitted Responses"):
        st.json(st.session_state.responses)

    if st.button("🔄 Submit Another Response"):
        st.session_state.submitted = False
        st.session_state.responses = {}
        st.rerun()
    st.stop()


# ══════════════════════════════════════
# HERO
# ══════════════════════════════════════
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">🧠 Enterprise Intelligence Survey 2026</div>
    <h1 class="hero-title">Corporate <span>AI Adoption</span><br>& Readiness Index</h1>
    <p class="hero-sub">
        A comprehensive diagnostic to understand where your organization stands in its AI journey —
        current adoption stages, functional integration, challenges, and future expectations.
    </p>
    <div class="hero-stats">
        <div class="hero-stat">
            <div class="hero-stat-num">8</div>
            <div class="hero-stat-label">Focus Areas</div>
        </div>
        <div class="hero-stat">
            <div class="hero-stat-num">35</div>
            <div class="hero-stat-label">Questions</div>
        </div>
        <div class="hero-stat">
            <div class="hero-stat-num">~7</div>
            <div class="hero-stat-label">Minutes</div>
        </div>
        <div class="hero-stat">
            <div class="hero-stat-num">100%</div>
            <div class="hero-stat-label">Confidential</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="info-note">
    <strong style="color:#4F46E5">Who should fill this?</strong> — C-Suite executives, Heads of Technology, HR Leaders, Operations Heads, or any senior decision-maker responsible for digital or AI strategy in your organization.
</div>
""", unsafe_allow_html=True)

responses = {}

# ══════════════════════════════════════════════════════
# SECTION A — COMPANY PROFILE
# ══════════════════════════════════════════════════════
sec("🏢", "purple", "Section A — Company Profile", "Tell us about your organization")

col1, col2 = st.columns(2)
with col1:
    qstart("purple", "A1 · Profile", "What is your industry sector?")
    r_a1 = st.selectbox("", [
        "Information Technology / Software",
        "Banking, Financial Services & Insurance (BFSI)",
        "Manufacturing & Engineering",
        "Healthcare & Pharmaceuticals",
        "Retail & E-Commerce",
        "Logistics, Supply Chain & Transportation",
        "Education & EdTech",
        "Media, Entertainment & Publishing",
        "Real Estate & Construction",
        "Government / PSU",
        "Consulting & Professional Services",
        "Hospitality & Travel",
        "Energy & Utilities",
        "Other"
    ], key="a1", label_visibility="collapsed")
    responses["A1_Industry"] = r_a1
    qend()

with col2:
    qstart("purple", "A2 · Profile", "What is the size of your organization?")
    r_a2 = st.radio("", [
        "Startup (1–50 employees)",
        "Small (51–200 employees)",
        "Mid-size (201–1,000 employees)",
        "Large (1,001–5,000 employees)",
        "Enterprise (5,000+ employees)"
    ], key="a2", label_visibility="collapsed")
    responses["A2_Company_Size"] = r_a2
    qend()

col3, col4 = st.columns(2)
with col3:
    qstart("purple", "A3 · Profile", "What is your role / function?")
    r_a3 = st.selectbox("", [
        "CEO / MD / Founder",
        "CTO / CIO / Technology Head",
        "CFO / Finance Head",
        "CHRO / HR Head",
        "COO / Operations Head",
        "CMO / Marketing Head",
        "Business Development Head",
        "Product / Strategy Head",
        "Data / Analytics Lead",
        "Other Senior Leader"
    ], key="a3", label_visibility="collapsed")
    responses["A3_Role"] = r_a3
    qend()

with col4:
    qstart("purple", "A4 · Profile", "What is your annual revenue range (approx.)?")
    r_a4 = st.radio("", [
        "Under ₹1 Crore",
        "₹1 Cr – ₹10 Cr",
        "₹10 Cr – ₹100 Cr",
        "₹100 Cr – ₹500 Cr",
        "₹500 Cr – ₹1,000 Cr",
        "Above ₹1,000 Cr"
    ], key="a4", label_visibility="collapsed")
    responses["A4_Revenue"] = r_a4
    qend()


# ══════════════════════════════════════════════════════
# SECTION B — CURRENT AI ADOPTION STAGE
# ══════════════════════════════════════════════════════
sec("📊", "cyan", "Section B — Current AI Adoption Stage", "Where is your organization today on the AI journey?")

qstart("cyan", "B1 · Adoption", "How would you describe your organization's current AI adoption stage?")
r_b1 = st.radio("", [
    "🔴  Stage 0 — No AI in use. Still evaluating.",
    "🟠  Stage 1 — Awareness & Exploration. Pilots being discussed.",
    "🟡  Stage 2 — Early Adoption. 1–2 tools in limited use (e.g. ChatGPT, Copilot).",
    "🟢  Stage 3 — Functional Integration. AI embedded in specific departments.",
    "🔵  Stage 4 — Scaled Deployment. AI across multiple business units.",
    "🟣  Stage 5 — AI-First Organization. AI is core to strategy and operations."
], key="b1", label_visibility="collapsed")
responses["B1_AI_Stage"] = r_b1
qend()

col5, col6 = st.columns(2)
with col5:
    qstart("cyan", "B2 · Tools", "Which AI tools / platforms is your organization currently using?",
           "Select all that apply")
    r_b2 = st.multiselect("", [
        "ChatGPT (OpenAI)",
        "Claude (Anthropic)",
        "Gemini (Google)",
        "Microsoft Copilot",
        "GitHub Copilot",
        "Midjourney / DALL-E (Image AI)",
        "Salesforce Einstein",
        "HubSpot AI",
        "Custom / In-house AI Models",
        "IBM Watson",
        "AWS AI Services",
        "Azure AI Services",
        "Google Cloud AI",
        "None currently"
    ], key="b2")
    responses["B2_Tools_Used"] = r_b2
    qend()

with col6:
    qstart("cyan", "B3 · Functions", "Which business functions are currently using AI in your organization?",
           "Select all that apply")
    r_b3 = st.multiselect("", [
        "Human Resources (Hiring, L&D, Payroll)",
        "Sales & Business Development",
        "Marketing & Content",
        "Customer Service / Support",
        "Finance & Accounting",
        "Operations & Supply Chain",
        "IT & Cybersecurity",
        "Product Development",
        "Legal & Compliance",
        "Data Analytics & BI",
        "Executive / C-Suite Decision Making",
        "None — AI not yet in any function"
    ], key="b3")
    responses["B3_Functions_Using_AI"] = r_b3
    qend()

qstart("cyan", "B4 · Investment", "What is your approximate annual budget allocated to AI tools and initiatives?")
r_b4 = st.radio("", [
    "No budget allocated yet",
    "Under ₹5 Lakhs",
    "₹5 – ₹25 Lakhs",
    "₹25 – ₹1 Crore",
    "₹1 – ₹5 Crore",
    "Above ₹5 Crore"
], key="b4", label_visibility="collapsed")
responses["B4_AI_Budget"] = r_b4
qend()

qstart("cyan", "B5 · Decision", "Who is the primary decision-maker for AI adoption in your organization?")
r_b5 = st.radio("", [
    "CEO / Founder — top-down mandate",
    "CTO / Technology Head — tech-driven",
    "Cross-functional AI Committee",
    "Department Heads independently",
    "No clear owner — ad hoc adoption",
    "External Consultants / Vendors driving it"
], key="b5", label_visibility="collapsed")
responses["B5_AI_Decision_Maker"] = r_b5
qend()


# ══════════════════════════════════════════════════════
# SECTION C — AI USE CASES IN PRACTICE
# ══════════════════════════════════════════════════════
sec("⚙️", "emerald", "Section C — AI Use Cases in Practice", "How is AI actually being applied day-to-day?")

qstart("emerald", "C1 · Use Cases", "What are the primary use cases for which your organization is using AI?",
       "Select all that apply")
r_c1 = st.multiselect("", [
    "Content Creation (emails, reports, decks)",
    "Customer Service / Chatbots",
    "Data Analysis & Reporting",
    "Code Writing / Development Assistance",
    "HR Automation (JDs, screening, onboarding)",
    "Sales Forecasting & Lead Scoring",
    "Marketing Personalization & Campaigns",
    "Financial Modelling & Analysis",
    "Document Summarization & Review",
    "Meeting Notes & Transcription",
    "Fraud Detection & Risk Management",
    "Supply Chain Optimization",
    "Predictive Maintenance (Manufacturing)",
    "Legal Document Review",
    "Training & Learning Development",
    "Executive Research & Decision Support",
    "Not using AI for specific use cases yet"
], key="c1")
responses["C1_AI_Use_Cases"] = r_c1
qend()

col7, col8 = st.columns(2)
with col7:
    qstart("emerald", "C2 · Productivity", "How much productivity improvement has your organization experienced from AI adoption?")
    r_c2 = st.radio("", [
        "No measurable improvement yet",
        "Under 10% improvement",
        "10–25% improvement",
        "25–50% improvement",
        "More than 50% improvement",
        "We haven't measured it"
    ], key="c2", label_visibility="collapsed")
    responses["C2_Productivity_Gain"] = r_c2
    qend()

with col8:
    qstart("emerald", "C3 · Satisfaction", "How satisfied are employees with the AI tools currently in use?")
    r_c3 = st.radio("", [
        "Very Satisfied — strong adoption and positive feedback",
        "Satisfied — mostly positive with minor friction",
        "Neutral — mixed reactions",
        "Dissatisfied — resistance or poor usability",
        "Very Dissatisfied — tools not meeting needs",
        "Not enough adoption to gauge"
    ], key="c3", label_visibility="collapsed")
    responses["C3_Employee_Satisfaction"] = r_c3
    qend()

qstart("emerald", "C4 · ROI", "Has your organization formally measured ROI from AI investments?")
r_c4 = st.radio("", [
    "Yes — clear positive ROI demonstrated",
    "Yes — ROI measured but results mixed",
    "No — ROI not yet formally measured",
    "No — too early to measure",
    "We don't plan to measure ROI"
], key="c4", label_visibility="collapsed")
responses["C4_ROI_Measurement"] = r_c4
qend()


# ══════════════════════════════════════════════════════
# SECTION D — CHALLENGES & PAIN POINTS
# ══════════════════════════════════════════════════════
sec("⚠️", "rose", "Section D — Challenges & Pain Points", "What is holding your organization back? Holistic view.")

qstart("rose", "D1 · Barriers", "What are the BIGGEST barriers to AI adoption in your organization?",
       "Select your top 3 challenges")
r_d1 = st.multiselect("", [
    "Lack of AI literacy / skills in the workforce",
    "High cost of AI tools and implementation",
    "Data quality, availability or governance issues",
    "Resistance to change from employees",
    "Unclear ROI / business case for AI",
    "Privacy, security and compliance concerns",
    "Lack of leadership vision or AI strategy",
    "Integration challenges with existing systems",
    "Vendor lock-in and dependency risks",
    "Ethical concerns about AI decisions",
    "Regulatory / legal uncertainty",
    "Difficulty in finding the right AI talent",
    "Too many tools — no standardization",
    "Fear of job displacement among staff"
], key="d1")
responses["D1_AI_Barriers"] = r_d1
qend()

col9, col10 = st.columns(2)
with col9:
    qstart("rose", "D2 · People", "What is the biggest PEOPLE challenge related to AI in your organization?")
    r_d2 = st.radio("", [
        "Employees fear AI will replace their jobs",
        "Workforce lacks basic AI/digital literacy",
        "Leadership doesn't understand AI well enough",
        "No dedicated AI/data team internally",
        "Resistance from middle management",
        "High attrition of AI-skilled talent"
    ], key="d2", label_visibility="collapsed")
    responses["D2_People_Challenge"] = r_d2
    qend()

with col10:
    qstart("rose", "D3 · Data", "What is your organization's biggest DATA challenge for AI?")
    r_d3 = st.radio("", [
        "Data is siloed across departments",
        "Data quality is poor or inconsistent",
        "No centralized data infrastructure",
        "Privacy / GDPR / data compliance concerns",
        "Lack of labelled data for training",
        "No dedicated data team",
        "Data is available but not structured for AI"
    ], key="d3", label_visibility="collapsed")
    responses["D3_Data_Challenge"] = r_d3
    qend()

col11, col12 = st.columns(2)
with col11:
    qstart("rose", "D4 · Technology", "What is your biggest TECHNOLOGY challenge for AI adoption?")
    r_d4 = st.radio("", [
        "Legacy systems that don't support AI integration",
        "Cybersecurity risks from AI tools",
        "No clear tech stack / architecture for AI",
        "Vendor reliability and support quality",
        "AI outputs are inconsistent or unreliable",
        "Lack of APIs or integration capability",
        "Too dependent on cloud vendors"
    ], key="d4", label_visibility="collapsed")
    responses["D4_Tech_Challenge"] = r_d4
    qend()

with col12:
    qstart("rose", "D5 · Strategy", "What is the biggest STRATEGIC challenge around AI in your organization?")
    r_d5 = st.radio("", [
        "No formal AI strategy or roadmap",
        "AI initiatives are fragmented — no cohesion",
        "Unclear ownership and accountability for AI",
        "Board / investors not aligned on AI priority",
        "Competitive pressure — falling behind peers",
        "Compliance and regulatory uncertainty",
        "Budget constraints limiting AI ambitions"
    ], key="d5", label_visibility="collapsed")
    responses["D5_Strategy_Challenge"] = r_d5
    qend()

qstart("rose", "D6 · Holistic", "From a holistic business perspective, which areas are MOST disrupted or stressed by the pace of AI change?",
       "Rank your top 3 areas of organizational stress")
r_d6 = st.multiselect("", [
    "Talent Acquisition — job profiles changing rapidly",
    "Learning & Development — training content outdated quickly",
    "Process Re-engineering — workflows need redesigning",
    "Customer Experience — rising expectations from AI",
    "Competitive Positioning — industry disruption",
    "Financial Planning — unclear AI cost-benefit",
    "Legal & Compliance — new regulations emerging",
    "Culture — fear, uncertainty, distrust of AI",
    "Leadership — C-Suite under pressure to demonstrate AI vision",
    "Vendor Management — too many AI vendors to evaluate"
], key="d6")
responses["D6_Holistic_Stress_Areas"] = r_d6
qend()


# ══════════════════════════════════════════════════════
# SECTION E — AI READINESS & GOVERNANCE
# ══════════════════════════════════════════════════════
sec("🛡️", "violet", "Section E — AI Readiness & Governance", "How prepared is your organization for responsible AI?")

col13, col14 = st.columns(2)
with col13:
    qstart("violet", "E1 · Policy", "Does your organization have a formal AI usage policy?")
    r_e1 = st.radio("", [
        "Yes — comprehensive AI policy in place",
        "Yes — basic guidelines exist",
        "Under development",
        "No — we rely on individual judgment",
        "No — and it's not a priority yet"
    ], key="e1", label_visibility="collapsed")
    responses["E1_AI_Policy"] = r_e1
    qend()

with col14:
    qstart("violet", "E2 · Ethics", "How does your organization handle AI ethics and bias concerns?")
    r_e2 = st.radio("", [
        "Formal AI ethics framework in place",
        "Ethics reviewed on a case-by-case basis",
        "Aware of concerns but no formal process",
        "Not currently addressed",
        "Don't know"
    ], key="e2", label_visibility="collapsed")
    responses["E2_AI_Ethics"] = r_e2
    qend()

col15, col16 = st.columns(2)
with col15:
    qstart("violet", "E3 · Training", "What AI training / upskilling has your organization provided?")
    r_e3 = st.radio("", [
        "Comprehensive AI training for all staff",
        "Role-specific AI training for key teams",
        "Awareness sessions only",
        "Individual self-learning — no org-level training",
        "No AI training provided yet"
    ], key="e3", label_visibility="collapsed")
    responses["E3_AI_Training"] = r_e3
    qend()

with col16:
    qstart("violet", "E4 · Vendor", "How does your organization evaluate and select AI vendors?")
    r_e4 = st.radio("", [
        "Formal vendor due diligence and RFP process",
        "CTO / IT team evaluates and recommends",
        "Department heads choose independently",
        "Based on peer recommendations",
        "No formal process — ad hoc decisions",
        "We build in-house, don't use vendors"
    ], key="e4", label_visibility="collapsed")
    responses["E4_Vendor_Selection"] = r_e4
    qend()


# ══════════════════════════════════════════════════════
# SECTION F — EXPECTATIONS FROM AI
# ══════════════════════════════════════════════════════
sec("🚀", "amber", "Section F — Expectations from AI", "What do you want AI to deliver for your organization?")

qstart("amber", "F1 · Priority", "What are your TOP expectations from AI over the next 12–24 months?",
       "Select your top 3 priorities")
r_f1 = st.multiselect("", [
    "Significant cost reduction through automation",
    "Faster and smarter decision making",
    "Better customer experience and personalization",
    "Improved employee productivity and focus",
    "New revenue streams and business models",
    "Competitive differentiation in the market",
    "Predictive analytics for risk management",
    "Reduction in human errors",
    "Faster product / service innovation",
    "Better talent acquisition and retention",
    "Stronger compliance and audit capabilities",
    "Real-time operational visibility"
], key="f1")
responses["F1_AI_Expectations"] = r_f1
qend()

col17, col18 = st.columns(2)
with col17:
    qstart("amber", "F2 · Timeline", "In what timeframe do you expect AI to become CORE to your business operations?")
    r_f2 = st.radio("", [
        "Already is — AI is core today",
        "Within 6 months",
        "Within 1 year",
        "Within 2–3 years",
        "3–5 years",
        "Not in the foreseeable future"
    ], key="f2", label_visibility="collapsed")
    responses["F2_AI_Timeline"] = r_f2
    qend()

with col18:
    qstart("amber", "F3 · Partner", "What kind of AI partner / support does your organization need most?")
    r_f3 = st.radio("", [
        "AI Strategy Consulting — roadmap and vision",
        "Hands-on Implementation Partner",
        "AI Training & Upskilling for our team",
        "Custom AI Tool Development",
        "AI Governance & Policy Advisory",
        "Ongoing AI Managed Services",
        "We are self-sufficient — no external support needed"
    ], key="f3", label_visibility="collapsed")
    responses["F3_AI_Partner_Need"] = r_f3
    qend()

qstart("amber", "F4 · Investment", "Is your organization planning to INCREASE AI investment in the next financial year?")
r_f4 = st.radio("", [
    "Yes — significantly (>50% increase)",
    "Yes — moderately (10–50% increase)",
    "Maintaining current level",
    "Reducing AI spend — rationalizing",
    "No AI budget planned"
], key="f4", label_visibility="collapsed")
responses["F4_Investment_Plan"] = r_f4
qend()

qstart("amber", "F5 · Jobs", "How do you see AI impacting your workforce headcount over the next 3 years?")
r_f5 = st.radio("", [
    "Net increase — AI creates more roles than it eliminates",
    "Neutral — redeployment, not reduction",
    "Some reduction in routine / repetitive roles",
    "Significant workforce reduction expected",
    "Too uncertain to predict",
    "We haven't thought about this yet"
], key="f5", label_visibility="collapsed")
responses["F5_Workforce_Impact"] = r_f5
qend()


# ══════════════════════════════════════════════════════
# SECTION G — INDUSTRY & COMPETITIVE LANDSCAPE
# ══════════════════════════════════════════════════════
sec("🌐", "cyan", "Section G — Industry & Competitive View", "AI in the context of your market and peers")

col19, col20 = st.columns(2)
with col19:
    qstart("cyan", "G1 · Peers", "Compared to your direct competitors, where does your organization stand on AI adoption?")
    r_g1 = st.radio("", [
        "Leading — significantly ahead of peers",
        "Ahead — slightly ahead of most",
        "On par — similar to industry average",
        "Behind — most peers are ahead of us",
        "Far behind — we are lagging significantly",
        "Not sure — we don't track this"
    ], key="g1", label_visibility="collapsed")
    responses["G1_Competitive_Position"] = r_g1
    qend()

with col20:
    qstart("cyan", "G2 · Disruption", "How concerned are you about AI-driven disruption to your industry within 3 years?")
    r_g2 = st.radio("", [
        "Extremely concerned — existential threat",
        "Very concerned — major shifts expected",
        "Moderately concerned — significant changes likely",
        "Slightly concerned — some impact expected",
        "Not concerned — our industry is resilient",
        "Excited — AI is an opportunity for us"
    ], key="g2", label_visibility="collapsed")
    responses["G2_Disruption_Concern"] = r_g2
    qend()

qstart("cyan", "G3 · Regulation", "How ready is your organization for upcoming AI regulations and compliance requirements?")
r_g3 = st.radio("", [
    "Fully prepared — monitoring regulations actively",
    "Partially prepared — some measures in place",
    "Aware but not yet prepared",
    "Not aware of upcoming AI regulations",
    "Relying on legal team to handle it when needed"
], key="g3", label_visibility="collapsed")
responses["G3_Regulation_Readiness"] = r_g3
qend()


# ══════════════════════════════════════════════════════
# SECTION H — OPEN FEEDBACK
# ══════════════════════════════════════════════════════
sec("💬", "purple", "Section H — Open Feedback & Insights", "Your candid voice matters most here")

qstart("purple", "H1 · Success", "Describe a SPECIFIC SUCCESS your organization has achieved using AI (even if small).")
r_h1 = st.text_area("", placeholder="E.g. We used ChatGPT to cut our proposal writing time by 60%... or We automated our HR screening and reduced time-to-hire by 3 weeks...", height=100, key="h1", label_visibility="collapsed")
responses["H1_AI_Success"] = r_h1
qend()

qstart("purple", "H2 · Failure", "Describe a CHALLENGE or FAILURE your organization experienced with an AI initiative.")
r_h2 = st.text_area("", placeholder="E.g. We invested in an AI chatbot that employees didn't adopt... or Data quality issues made our AI model unreliable...", height=100, key="h2", label_visibility="collapsed")
responses["H2_AI_Challenge"] = r_h2
qend()

qstart("purple", "H3 · Wish", "If you could solve ONE problem in your organization using AI tomorrow, what would it be?")
r_h3 = st.text_area("", placeholder="Be specific — what keeps you up at night that you believe AI could solve?", height=100, key="h3", label_visibility="collapsed")
responses["H3_AI_Wish"] = r_h3
qend()

qstart("purple", "H4 · Advice", "What advice would you give to other corporate leaders who are just beginning their AI journey?")
r_h4 = st.text_area("", placeholder="Your honest perspective from the trenches...", height=100, key="h4", label_visibility="collapsed")
responses["H4_Leadership_Advice"] = r_h4
qend()

qstart("purple", "H5 · Feedback", "Any feedback, suggestions, or additional thoughts you would like to share with us?")
r_h5 = st.text_area("", placeholder="Anything else on your mind — about AI, about this survey, about your industry...", height=100, key="h5", label_visibility="collapsed")
responses["H5_General_Feedback"] = r_h5
qend()


# ══════════════════════════════════════════════════════
# PROGRESS + SUBMIT
# ══════════════════════════════════════════════════════
mcq_responses = [r_a1, r_a2, r_a3, r_a4, r_b1, r_b4, r_b5, r_c2, r_c3, r_c4,
                 r_d2, r_d3, r_d4, r_d5, r_e1, r_e2, r_e3, r_e4, r_f2, r_f3,
                 r_f4, r_f5, r_g1, r_g2, r_g3]
multi_responses = [r_b2, r_b3, r_c1, r_d1, r_d6, r_f1]
answered = sum([1 for r in mcq_responses if r]) + sum([1 for r in multi_responses if r])
total = 31
pct = int((answered / total) * 100)

st.markdown(f"""
<div class="prog-wrap">
    <div class="prog-label">Survey Completion</div>
    <div class="prog-outer">
        <div class="prog-inner" style="width:{pct}%"></div>
    </div>
    <div class="prog-pct">{pct}%</div>
</div>
""", unsafe_allow_html=True)

col_s1, col_s2, col_s3 = st.columns([1, 2, 1])
with col_s2:
    if st.button("🤖  Submit Corporate AI Survey"):
        responses["submitted_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.responses = responses
        st.session_state.submitted = True
        st.rerun()

st.markdown("""
<p style='text-align:center;font-size:12px;color:#9CA3AF;margin-top:12px;'>
    🔒 All responses are completely confidential and used solely for AI adoption research purposes.
</p>
""", unsafe_allow_html=True)
