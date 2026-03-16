import streamlit as st
import os
import json
import time
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY", "")

# ── PAGE CONFIG ──
st.set_page_config(
    page_title="Airport Cab Experience Survey",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── CUSTOM CSS + VOICE UI ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --navy: #0D1B2A;
    --blue: #1B3A6B;
    --sky: #2E75B6;
    --accent: #F0A500;
    --light: #EBF3FB;
    --white: #FFFFFF;
    --grey: #F7F9FC;
    --text: #1A1A2E;
    --muted: #6B7A8D;
    --border: #D0DEF0;
    --success: #1DB954;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--grey) !important;
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background: linear-gradient(160deg, #EBF3FB 0%, #F7F9FC 50%, #EBF3FB 100%) !important;
}

#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }

.top-banner {
    background: linear-gradient(135deg, #0D1B2A 0%, #1B3A6B 60%, #2E75B6 100%);
    padding: 48px 60px 40px;
    border-radius: 0 0 32px 32px;
    margin: -80px -60px 40px -60px;
    position: relative;
    overflow: hidden;
}
.top-banner::before {
    content: "✈";
    position: absolute;
    right: 60px;
    top: 20px;
    font-size: 160px;
    opacity: 0.06;
    line-height: 1;
}
.banner-tag {
    display: inline-block;
    background: rgba(240,165,0,0.2);
    color: #F0A500;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 4px 14px;
    border-radius: 20px;
    border: 1px solid rgba(240,165,0,0.3);
    margin-bottom: 16px;
}
.banner-title {
    font-family: 'Playfair Display', serif;
    font-size: 42px;
    font-weight: 900;
    color: white;
    line-height: 1.1;
    margin: 0 0 8px 0;
}
.banner-sub {
    font-size: 15px;
    color: rgba(255,255,255,0.65);
    margin: 0;
    font-weight: 300;
}

.section-header {
    background: linear-gradient(135deg, var(--navy), var(--blue));
    color: white;
    padding: 14px 24px;
    border-radius: 12px;
    font-family: 'Playfair Display', serif;
    font-size: 18px;
    font-weight: 700;
    margin: 32px 0 20px 0;
    display: flex;
    align-items: center;
    gap: 12px;
    box-shadow: 0 4px 16px rgba(27,58,107,0.2);
}

.q-card {
    background: white;
    border-radius: 16px;
    padding: 24px 28px;
    margin-bottom: 16px;
    border: 1px solid var(--border);
    box-shadow: 0 2px 8px rgba(27,58,107,0.05);
}
.q-card:hover { box-shadow: 0 4px 20px rgba(27,58,107,0.1); }
.q-number {
    display: inline-block;
    background: var(--blue);
    color: white;
    font-size: 11px;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 6px;
    margin-bottom: 10px;
}
.q-text {
    font-size: 15px;
    font-weight: 600;
    color: var(--text);
    line-height: 1.5;
    margin: 0 0 12px 0;
}

/* Voice button */
.voice-btn-wrap {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 12px;
}
.mic-btn {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: linear-gradient(135deg, #0D1B2A, #1B3A6B);
    color: white;
    border: none;
    border-radius: 50px;
    padding: 10px 22px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    font-family: 'DM Sans', sans-serif;
    transition: all 0.2s;
    box-shadow: 0 4px 14px rgba(27,58,107,0.3);
}
.mic-btn:hover {
    background: linear-gradient(135deg, #1B3A6B, #2E75B6);
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(27,58,107,0.4);
}
.mic-btn.recording {
    background: linear-gradient(135deg, #c0392b, #e74c3c) !important;
    animation: pulse 1.2s infinite;
}
.mic-btn.processing {
    background: linear-gradient(135deg, #F0A500, #f39c12) !important;
}
@keyframes pulse {
    0%, 100% { box-shadow: 0 4px 14px rgba(231,76,60,0.4); }
    50% { box-shadow: 0 4px 28px rgba(231,76,60,0.8); transform: scale(1.03); }
}

.voice-status {
    font-size: 13px;
    font-weight: 500;
    color: var(--muted);
    font-style: italic;
}
.voice-status.active { color: #e74c3c; font-weight: 600; }
.voice-status.processing { color: #F0A500; font-weight: 600; }
.voice-status.done { color: #1DB954; font-weight: 600; }

.transcript-box {
    background: linear-gradient(135deg, #EBF3FB, #f0f7ff);
    border: 1.5px solid #2E75B6;
    border-radius: 12px;
    padding: 14px 18px;
    font-size: 14px;
    color: #1B3A6B;
    font-weight: 500;
    margin-bottom: 10px;
    line-height: 1.6;
    position: relative;
}
.transcript-box::before {
    content: "🎤 Transcribed:";
    display: block;
    font-size: 11px;
    font-weight: 700;
    color: #2E75B6;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 6px;
}

.voice-tip {
    background: rgba(240,165,0,0.08);
    border: 1px solid rgba(240,165,0,0.25);
    border-radius: 10px;
    padding: 10px 16px;
    font-size: 12.5px;
    color: #856a00;
    margin-bottom: 14px;
}

div[data-testid="stTextArea"] textarea {
    border-radius: 12px !important;
    border: 1.5px solid var(--border) !important;
    font-size: 14px !important;
    font-family: 'DM Sans', sans-serif !important;
    padding: 12px 16px !important;
    background: var(--grey) !important;
}
div[data-testid="stTextArea"] textarea:focus {
    border-color: var(--sky) !important;
    background: white !important;
    box-shadow: 0 0 0 3px rgba(46,117,182,0.1) !important;
}

div[data-testid="stRadio"] label {
    background: var(--grey) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 10px !important;
    padding: 10px 16px !important;
    font-size: 14px !important;
    color: var(--text) !important;
    display: flex !important;
    align-items: center !important;
}
div[data-testid="stRadio"] label:hover {
    border-color: var(--sky) !important;
    background: var(--light) !important;
}

div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #0D1B2A, #1B3A6B) !important;
    color: white !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    padding: 14px 40px !important;
    border-radius: 12px !important;
    border: none !important;
    width: 100% !important;
    box-shadow: 0 4px 16px rgba(27,58,107,0.3) !important;
}

.success-box {
    background: linear-gradient(135deg, #0D1B2A, #1B3A6B);
    border-radius: 20px;
    padding: 48px 40px;
    text-align: center;
    color: white;
    box-shadow: 0 8px 32px rgba(27,58,107,0.3);
}
.success-icon { font-size: 64px; margin-bottom: 16px; }
.success-title {
    font-family: 'Playfair Display', serif;
    font-size: 32px;
    font-weight: 900;
    margin-bottom: 12px;
}
.success-text { font-size: 16px; color: rgba(255,255,255,0.75); line-height: 1.6; }
.success-ref {
    display: inline-block;
    background: rgba(240,165,0,0.15);
    border: 1px solid rgba(240,165,0,0.4);
    color: #F0A500;
    padding: 8px 20px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 600;
    margin-top: 20px;
    letter-spacing: 1px;
}
.fancy-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
    margin: 8px 0;
}
.info-card {
    background: linear-gradient(135deg, #EBF3FB, #F7F9FC);
    border: 1px solid var(--border);
    border-left: 4px solid var(--accent);
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 24px;
    font-size: 14px;
    color: var(--muted);
    line-height: 1.6;
}
.progress-wrap {
    background: white;
    border-radius: 16px;
    padding: 20px 28px;
    margin-bottom: 32px;
    box-shadow: 0 2px 12px rgba(27,58,107,0.08);
    border: 1px solid var(--border);
    display: flex;
    align-items: center;
    gap: 20px;
}
.progress-label { font-size: 13px; font-weight: 600; color: var(--blue); white-space: nowrap; min-width: 120px; }
.progress-bar-outer { flex: 1; background: var(--light); border-radius: 8px; height: 8px; overflow: hidden; }
.progress-bar-inner { height: 100%; background: linear-gradient(90deg, #1B3A6B, #2E75B6, #F0A500); border-radius: 8px; }
.progress-pct { font-size: 14px; font-weight: 700; color: var(--accent); min-width: 40px; text-align: right; }
[data-testid="column"] { padding: 0 8px !important; }
</style>

""", unsafe_allow_html=True)


# ── HELPERS ──
def transcribe_audio(audio_bytes):
    """Call Deepgram server-side — key never exposed to browser"""
    try:
        response = requests.post(
            "https://api.deepgram.com/v1/listen?model=nova-2&language=en-IN&punctuate=true&smart_format=true",
            headers={
                "Authorization": f"Token {DEEPGRAM_API_KEY}",
                "Content-Type": "audio/webm"
            },
            data=audio_bytes,
            timeout=30
        )
        data = response.json()
        return data.get("results", {}).get("channels", [{}])[0].get("alternatives", [{}])[0].get("transcript", "")
    except Exception:
        return ""

def section_header(icon, title):
    st.markdown(f"""
    <div class="section-header">
        <span style="font-size:22px">{icon}</span>
        {title}
    </div>
    """, unsafe_allow_html=True)

def q_label(num, text):
    st.markdown(f"""
    <div style="margin-bottom:6px">
        <span class="q-number">Q{num}</span>
        <p class="q-text">{text}</p>
    </div>
    """, unsafe_allow_html=True)

def card_start():
    st.markdown('<div class="q-card">', unsafe_allow_html=True)

def card_end():
    st.markdown('</div>', unsafe_allow_html=True)

def voice_input(placeholder_text, key, height=110):
    """Voice-enabled text area — transcription happens server-side, key never sent to browser"""
    st.markdown("""
    <div class="voice-tip">
        💡 <strong>Tip:</strong> Record your answer below, or simply type.
    </div>
    """, unsafe_allow_html=True)

    audio = st.audio_input("🎤 Tap to speak", key=f"audio_{key}")

    default_value = ""
    if audio is not None:
        transcript = transcribe_audio(audio.read())
        if transcript:
            default_value = transcript
            st.markdown(f'<div class="transcript-box">{transcript}</div>', unsafe_allow_html=True)
        else:
            st.warning("Couldn't transcribe. Please try again or type below.")

    value = st.text_area(
        "",
        value=default_value,
        placeholder=placeholder_text,
        height=height,
        key=key,
        label_visibility="collapsed"
    )
    return value


# ── SESSION STATE ──
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "responses" not in st.session_state:
    st.session_state.responses = {}

# ── SUBMITTED STATE ──
if st.session_state.submitted:
    ref = datetime.now().strftime("ACS-%Y%m%d-%H%M%S")
    st.markdown(f"""
    <div class="success-box">
        <div class="success-icon">✈️</div>
        <div class="success-title">Thank You for Your Feedback!</div>
        <div class="success-text">
            Your response has been recorded successfully.<br>
            Your insights help us deliver a consistently premium airport cab experience.
        </div>
        <div class="success-ref">REF: {ref}</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("📋 View Your Submitted Responses"):
        st.json(st.session_state.responses)
    if st.button("🔄 Submit Another Response"):
        st.session_state.submitted = False
        st.session_state.responses = {}
        st.rerun()
    st.stop()


# ── BANNER ──
st.markdown("""
<div class="top-banner">
    <div class="banner-tag">Customer Experience Survey</div>
    <h1 class="banner-title">✈ Airport Cab Service</h1>
    <p class="banner-sub">City ↔ Airport &nbsp;|&nbsp; Commercial Cab Industry &nbsp;|&nbsp; Confidential & Internal Use Only</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="info-card">
    <strong style="color:#1B3A6B">Dear Traveller,</strong><br>
    Thank you for choosing our cab service. Your feedback helps us deliver a consistently premium experience every time.
    This survey takes less than <strong>5 minutes</strong> to complete. The last section supports <strong>🎤 voice input</strong> — just speak your thoughts!
</div>
""", unsafe_allow_html=True)

responses = {}

# ══════════════════════════════════════════════
# SECTION A — RESPONDENT PROFILE
# ══════════════════════════════════════════════
section_header("👤", "Section A — Respondent Profile")
col1, col2 = st.columns(2)
with col1:
    card_start()
    q_label(1, "What was the purpose of your trip?")
    r1 = st.radio("", ["Business / Corporate Travel","Leisure / Personal Travel","Airport Pick-up / Drop of a Guest","Medical / Emergency","Other"], key="q1", label_visibility="collapsed")
    responses["Q1_Trip_Purpose"] = r1
    card_end()
with col2:
    card_start()
    q_label(2, "How frequently do you travel to/from the airport?")
    r2 = st.radio("", ["Daily","2–3 times a week","Once a week","2–3 times a month","Occasionally / Rarely"], key="q2", label_visibility="collapsed")
    responses["Q2_Travel_Frequency"] = r2
    card_end()

col3, col4 = st.columns(2)
with col3:
    card_start()
    q_label(3, "Which direction was your most recent ride?")
    r3 = st.radio("", ["City to Airport","Airport to City","Both (Round Trip)"], key="q3", label_visibility="collapsed")
    responses["Q3_Ride_Direction"] = r3
    card_end()
with col4:
    card_start()
    q_label(4, "How did you book this ride?")
    r4 = st.radio("", ["Mobile App","Website","Phone Call","Walk-in / On-spot","Corporate Account / Pre-arranged"], key="q4", label_visibility="collapsed")
    responses["Q4_Booking_Method"] = r4
    card_end()

# ══════════════════════════════════════════════
# SECTION B — PRE-RIDE
# ══════════════════════════════════════════════
section_header("📱", "Section B — Pre-Ride / Booking Experience")
col5, col6 = st.columns(2)
with col5:
    card_start()
    q_label(5, "How easy was the booking process?")
    r5 = st.radio("", ["Very Easy","Easy","Neutral","Difficult","Very Difficult"], key="q5", label_visibility="collapsed")
    responses["Q5_Booking_Ease"] = r5
    card_end()
with col6:
    card_start()
    q_label(6, "Did you receive booking confirmation and driver details on time?")
    r6 = st.radio("", ["Yes, well in advance","Yes, but at the last minute","No, I had to follow up","No confirmation received"], key="q6", label_visibility="collapsed")
    responses["Q6_Booking_Confirmation"] = r6
    card_end()

col7, col8 = st.columns(2)
with col7:
    card_start()
    q_label(7, "How satisfied were you with fare transparency at booking?")
    r7 = st.radio("", ["Completely Satisfied — Price was clear upfront","Mostly Satisfied — Minor confusion","Neutral","Dissatisfied — Hidden charges noticed","Very Dissatisfied — Pricing was unclear"], key="q7", label_visibility="collapsed")
    responses["Q7_Fare_Transparency"] = r7
    card_end()
with col8:
    card_start()
    q_label(8, "Did the cab arrive on time as scheduled?")
    r8 = st.radio("", ["Yes, exactly on time","Early — I preferred it","Slightly late (less than 10 mins)","Late (10–30 mins)","Very late (more than 30 mins)"], key="q8", label_visibility="collapsed")
    responses["Q8_Punctuality"] = r8
    card_end()

card_start()
q_label(9, "Were you informed proactively about any delays or changes before your ride?")
r9 = st.radio("", ["Yes, I was informed well in advance","Yes, but it was very last minute","No, I found out on my own","There was no delay / change"], key="q9", label_visibility="collapsed")
responses["Q9_Delay_Communication"] = r9
card_end()

# ══════════════════════════════════════════════
# SECTION C — IN-RIDE
# ══════════════════════════════════════════════
section_header("🚗", "Section C — In-Ride Experience")
card_start()
q_label(10, "Please rate the following aspects of your ride (1 = Very Poor → 5 = Excellent)")
ride_params = ["Vehicle Cleanliness","Vehicle Comfort & Condition","In-car Amenities (Water, Charger, etc.)","AC / Temperature Control","Driver's Behaviour & Courtesy","Driver's Grooming & Appearance","Safe & Smooth Driving","Knowledge of Route / Navigation","Music / Noise Level","Overall Ride Comfort"]
ratings = {}
for param in ride_params:
    col_a, col_b = st.columns([3, 2])
    with col_a:
        st.markdown(f"<p style='font-size:14px;font-weight:500;color:#1A1A2E;margin:4px 0'>{param}</p>", unsafe_allow_html=True)
    with col_b:
        rating = st.select_slider("", options=["1 — Very Poor","2 — Poor","3 — Average","4 — Good","5 — Excellent"], value="3 — Average", key=f"rating_{param}", label_visibility="collapsed")
        ratings[param] = rating
    st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)
responses["Q10_Ride_Ratings"] = ratings
card_end()

col9, col10 = st.columns(2)
with col9:
    card_start()
    q_label(11, "Did the driver follow the agreed / optimal route?")
    r11 = st.radio("", ["Yes, followed the best route","Mostly yes, minor detour","No, took an unnecessarily longer route","I was unaware of the route"], key="q11", label_visibility="collapsed")
    responses["Q11_Route_Followed"] = r11
    card_end()
with col10:
    card_start()
    q_label(12, "Did you feel safe during the ride?")
    r12 = st.radio("", ["Absolutely — 100% safe","Mostly safe","Neutral","Slightly uncomfortable","No, I did not feel safe"], key="q12", label_visibility="collapsed")
    responses["Q12_Safety"] = r12
    card_end()

# ══════════════════════════════════════════════
# SECTION D — AIRPORT SPECIFIC
# ══════════════════════════════════════════════
section_header("🛫", "Section D — Airport-Specific Experience")
col11, col12 = st.columns(2)
with col11:
    card_start()
    q_label(13, "For Airport Drop — Did the driver drop you at the correct terminal / gate?")
    r13 = st.radio("", ["Yes, exactly the right terminal","Yes, but I had to walk some distance","No, dropped at wrong terminal","Not applicable"], key="q13", label_visibility="collapsed")
    responses["Q13_Terminal_Drop"] = r13
    card_end()
with col12:
    card_start()
    q_label(14, "For Airport Pick-up — How was the pick-up experience?")
    r14 = st.radio("", ["Driver was waiting before I arrived","Driver arrived within 5 minutes","Had to wait more than 10 minutes","Driver was hard to locate / communicate with","Pick-up was confusing and poorly managed"], key="q14", label_visibility="collapsed")
    responses["Q14_Pickup_Experience"] = r14
    card_end()

col13, col14 = st.columns(2)
with col13:
    card_start()
    q_label(15, "Did the driver assist with your luggage?")
    r15 = st.radio("", ["Yes, proactively and without being asked","Yes, when I asked","Partially","No, did not assist","I did not require assistance"], key="q15", label_visibility="collapsed")
    responses["Q15_Luggage_Assist"] = r15
    card_end()
with col14:
    card_start()
    q_label(16, "Was the cab timing sufficient to reach the airport comfortably?")
    r16 = st.radio("", ["Reached well in advance — very comfortable","Reached on time with reasonable buffer","Just made it — very stressful","Reached late — missed / nearly missed flight","Not applicable — airport to city ride"], key="q16", label_visibility="collapsed")
    responses["Q16_Airport_Timing"] = r16
    card_end()

card_start()
q_label(17, "Did the driver communicate about traffic or delays en route to the airport?")
r17 = st.radio("", ["Yes, kept me updated proactively","Communicated when I asked","Did not communicate","There was no delay"], key="q17", label_visibility="collapsed")
responses["Q17_Traffic_Communication"] = r17
card_end()

# ══════════════════════════════════════════════
# SECTION E — DRIVER QUALITY
# ══════════════════════════════════════════════
section_header("👨‍✈️", "Section E — Driver & Service Quality")
col15, col16 = st.columns(2)
with col15:
    card_start()
    q_label(18, "How would you rate your driver overall?")
    r18 = st.radio("", ["⭐⭐⭐⭐⭐  Excellent","⭐⭐⭐⭐     Good","⭐⭐⭐        Average","⭐⭐           Below Average","⭐              Poor"], key="q18", label_visibility="collapsed")
    responses["Q18_Driver_Rating"] = r18
    card_end()
with col16:
    card_start()
    q_label(19, "Was your driver professionally dressed and groomed?")
    r19 = st.radio("", ["Yes, very professional","Acceptable","Somewhat unprofessional","No, clearly unprofessional"], key="q19", label_visibility="collapsed")
    responses["Q19_Driver_Grooming"] = r19
    card_end()

col17, col18 = st.columns(2)
with col17:
    card_start()
    q_label(20, "Did the driver use a mobile phone while driving?")
    r20 = st.radio("", ["No, not at all","Used hands-free / Bluetooth only","Yes, briefly","Yes, frequently — it was concerning"], key="q20", label_visibility="collapsed")
    responses["Q20_Phone_Usage"] = r20
    card_end()
with col18:
    card_start()
    q_label(21, "Did the driver ask for / accept tips in a pressuring way?")
    r21 = st.radio("", ["No, professional throughout","Hinted but did not pressure","Yes, it was mildly uncomfortable","Yes, it was very uncomfortable"], key="q21", label_visibility="collapsed")
    responses["Q21_Tip_Pressure"] = r21
    card_end()

# ══════════════════════════════════════════════
# SECTION F — PRICING
# ══════════════════════════════════════════════
section_header("💰", "Section F — Pricing, Billing & Value for Money")
col19, col20 = st.columns(2)
with col19:
    card_start()
    q_label(22, "Was the fare charged consistent with the quoted / metered price?")
    r22 = st.radio("", ["Yes, exactly as quoted","Slight variation — acceptable","Higher than quoted — unexplained","Much higher than quoted"], key="q22", label_visibility="collapsed")
    responses["Q22_Fare_Accuracy"] = r22
    card_end()
with col20:
    card_start()
    q_label(23, "How would you rate the overall value for money?")
    r23 = st.radio("", ["Excellent value","Good value","Fair","Slightly overpriced","Very overpriced"], key="q23", label_visibility="collapsed")
    responses["Q23_Value_For_Money"] = r23
    card_end()

card_start()
q_label(24, "Were you satisfied with the payment options available?")
r24 = st.radio("", ["Yes, multiple convenient options available","Acceptable","Limited options — minor inconvenience","No, very limited — caused issues"], key="q24", label_visibility="collapsed")
responses["Q24_Payment_Options"] = r24
card_end()

# ══════════════════════════════════════════════
# SECTION G — OVERALL SATISFACTION
# ══════════════════════════════════════════════
section_header("🏆", "Section G — Overall Satisfaction & Loyalty")
col21, col22 = st.columns(2)
with col21:
    card_start()
    q_label(25, "How would you rate your OVERALL experience?")
    r25 = st.radio("", ["⭐⭐⭐⭐⭐  Excellent (5/5)","⭐⭐⭐⭐     Good (4/5)","⭐⭐⭐        Average (3/5)","⭐⭐           Below Average (2/5)","⭐              Poor (1/5)"], key="q25", label_visibility="collapsed")
    responses["Q25_Overall_Rating"] = r25
    card_end()
with col22:
    card_start()
    q_label(26, "How likely are you to use our service again?")
    r26 = st.radio("", ["Definitely will — my go-to service","Very likely","Possibly","Unlikely","Will not use again"], key="q26", label_visibility="collapsed")
    responses["Q26_Repeat_Usage"] = r26
    card_end()

col23, col24 = st.columns(2)
with col23:
    card_start()
    q_label(27, "Would you recommend our service to others?")
    r27 = st.radio("", ["Yes, absolutely — would actively recommend","Yes, if asked","Neutral","Probably not","No, would not recommend"], key="q27", label_visibility="collapsed")
    responses["Q27_Recommendation"] = r27
    card_end()
with col24:
    card_start()
    q_label(28, "Compared to other cab services, how do we rank?")
    r28 = st.radio("", ["Best — significantly better","Better than most","About the same","Below most","Worst — significantly inferior"], key="q28", label_visibility="collapsed")
    responses["Q28_Competitor_Comparison"] = r28
    card_end()

# ══════════════════════════════════════════════
# SECTION H — VOICE-ENABLED OPEN FEEDBACK
# ══════════════════════════════════════════════
section_header("🎤", "Section H — Tell Us In Your Own Words")

st.markdown("""
<div class="info-card">
    <strong style="color:#1B3A6B">🎙️ Voice-Enabled Section</strong><br>
    This section supports voice input! Click <strong>🎤 Tap to Speak</strong> on any question,
    speak naturally, and your words will be transcribed automatically.
    You can always edit the text after speaking.
</div>
""", unsafe_allow_html=True)

card_start()
q_label(29, "What did you like MOST about your experience today?")
r29 = voice_input("Tell us what stood out positively — the driver, the vehicle, the timing, the booking process...", "q29")
responses["Q29_Liked_Most"] = r29
card_end()

card_start()
q_label(30, "What was the BIGGEST pain point or disappointment in your journey?")
r30 = voice_input("Be candid — we want to know exactly what fell short so we can fix it...", "q30")
responses["Q30_Pain_Point"] = r30
card_end()

card_start()
q_label(31, "What ONE improvement would make the biggest difference?")
r31 = voice_input("Your single most impactful suggestion — app feature, driver training, pricing, routing...", "q31")
responses["Q31_Top_Improvement"] = r31
card_end()

card_start()
q_label(32, "Any additional comments, compliments, or suggestions?")
r32 = voice_input("Anything else — a compliment for a great driver, a specific incident, a broader thought...", "q32")
responses["Q32_Additional_Comments"] = r32
card_end()

# ══════════════════════════════════════════════
# PROGRESS & SUBMIT
# ══════════════════════════════════════════════
answered = sum([bool(r1),bool(r2),bool(r3),bool(r4),bool(r5),bool(r6),bool(r7),bool(r8),bool(r9),bool(r11),bool(r12),bool(r13),bool(r14),bool(r15),bool(r16),bool(r17),bool(r18),bool(r19),bool(r20),bool(r21),bool(r22),bool(r23),bool(r24),bool(r25),bool(r26),bool(r27),bool(r28)])
pct = int((answered / 27) * 100)

st.markdown(f"""
<div class="progress-wrap">
    <div class="progress-label">Survey Progress</div>
    <div class="progress-bar-outer">
        <div class="progress-bar-inner" style="width:{pct}%"></div>
    </div>
    <div class="progress-pct">{pct}%</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    if st.button("✈️  Submit My Feedback"):
        responses["submitted_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.responses = responses
        st.session_state.submitted = True
        st.rerun()

st.markdown("""
<p style='text-align:center;font-size:12px;color:#9AA5B4;margin-top:16px;'>
    🔒 Your responses are confidential and used solely for service improvement purposes.
</p>
""", unsafe_allow_html=True)
