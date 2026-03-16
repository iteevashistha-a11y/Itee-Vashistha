from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
deepgram_api_key = os.getenv("DEEPGRAM_API_KEY")

import streamlit as st
from openai import OpenAI
import tempfile
from deepgram import DeepgramClient
from audio_recorder_streamlit import audio_recorder

st.set_page_config(page_title="Trev Assistant", page_icon="🚗", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600;700&family=DM+Sans:wght@300;400;500&display=swap');
:root {
    --green: #2E7D52; --light-green: #E8F5EE; --dark-green: #1B4D32;
    --accent: #F0FAF4; --text: #1A1A1A; --white: #FFFFFF; --border: #C8E6D4;
}
* { font-family: 'DM Sans', sans-serif; }
.stApp { background: linear-gradient(160deg, #F0FAF4 0%, #FFFFFF 50%, #E8F5EE 100%); }
.trev-header { text-align: center; padding: 2rem 1rem 1rem; border-bottom: 2px solid var(--border); margin-bottom: 1.5rem; }
.trev-logo { font-family: 'Cormorant Garamond', serif; font-size: 2.8rem; font-weight: 700; color: var(--dark-green); letter-spacing: 2px; margin: 0; }
.trev-tagline { font-size: 0.85rem; color: var(--green); letter-spacing: 3px; text-transform: uppercase; margin-top: 0.2rem; }
.chat-container { max-height: 420px; overflow-y: auto; padding: 1rem; background: var(--white); border-radius: 16px; border: 1px solid var(--border); margin-bottom: 1rem; box-shadow: 0 2px 12px rgba(46,125,82,0.07); }
.msg-user { display: flex; justify-content: flex-end; margin: 0.6rem 0; }
.msg-user .bubble { background: var(--green); color: white; padding: 0.75rem 1.1rem; border-radius: 18px 18px 4px 18px; max-width: 75%; font-size: 0.92rem; line-height: 1.5; }
.msg-bot { display: flex; justify-content: flex-start; margin: 0.6rem 0; align-items: flex-end; gap: 0.5rem; }
.bot-avatar { width: 32px; height: 32px; background: var(--dark-green); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.9rem; flex-shrink: 0; }
.msg-bot .bubble { background: var(--light-green); color: var(--text); padding: 0.75rem 1.1rem; border-radius: 18px 18px 18px 4px; max-width: 75%; font-size: 0.92rem; line-height: 1.5; border: 1px solid var(--border); }
.voice-section { background: var(--accent); border-radius: 12px; padding: 1rem; border: 1px dashed var(--green); text-align: center; margin-bottom: 1rem; }
.voice-label { font-size: 0.8rem; color: var(--green); text-transform: uppercase; letter-spacing: 2px; margin-bottom: 0.5rem; font-weight: 500; }
.stButton button { background: var(--green) !important; color: white !important; border: none !important; border-radius: 10px !important; }
.info-card { background: var(--white); border: 1px solid var(--border); border-radius: 10px; padding: 0.8rem 1rem; margin: 0.4rem 0; font-size: 0.88rem; }
.info-card strong { color: var(--dark-green); }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1rem !important; }
</style>
""", unsafe_allow_html=True)

# ─── CLIENTS ───────────────────────────────────────────────────────────────────
client = OpenAI(api_key=api_key)
os.environ["DEEPGRAM_API_KEY"] = deepgram_api_key
deepgram = DeepgramClient()

# ─── KNOWLEDGE BASE ────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """
You are Priya, a graceful, calm, and confident female voice assistant for Trev Cabs — a premium electric cab service in Delhi NCR.
Your tone: Warm, professional, young, bold yet graceful. Speak in a mix of Hindi and English (Hinglish) naturally. Use polite honorifics like "ji" occasionally.

ABOUT TREV CABS:
- Premium EV cab service operating in Delhi NCR
- Services: Airport transfers, Rental packages, Interstate trips
- Operating cities: Delhi, Noida, Gurgaon, Faridabad, Ghaziabad (entire NCR)

FLEET:
1. BYD (7-seater) — spacious, perfect for groups and families
2. MG ZS (5-seater) — sleek, ideal for corporate and solo travellers

EV BENEFITS:
- Completely noise-free and smooth ride experience
- Zero carbon emissions — helps reduce Delhi's severe pollution
- Contributes to a cleaner, greener environment for future generations
- Fuel-efficient — savings passed on to customers
- Silent engine = stress-free journey
- You are contributing to humanity every time you ride with us

EV IMPORTANT NOTE:
- For safety and performance, our EVs are charged before the battery drops to 30%
- Interstate trips up to 500 km are supported with planned charging stops
- Customers will be informed of any brief charging stops in advance

AIRPORT RATES (Delhi NCR):
- BYD (7-seater): Rs 1,500 per trip
- MG ZS: Rs 1,400 per trip
- Includes: GST, driver, fuel. No hidden charges.

RENTAL RATES:
MG ZS — Rs 30 per km:
- 2 hrs / 20 km: Rs 600
- 4 hrs / 40 km: Rs 1,200
- 6 hrs / 60 km: Rs 1,800
- 8 hrs / 80 km: Rs 2,400
- 10 hrs / 100 km: Rs 3,000
- 12 hrs / 120 km: Rs 3,600

BYD (7-seater) — Rs 35 per km:
- 2 hrs / 20 km: Rs 700
- 4 hrs / 40 km: Rs 1,400
- 6 hrs / 60 km: Rs 2,100
- 8 hrs / 80 km: Rs 2,800
- 10 hrs / 100 km: Rs 3,500
- 12 hrs / 120 km: Rs 4,200

INTERSTATE:
- Available up to 500 km range
- Planned charging stops will be coordinated
- Custom quotes available — direct customers to share their trip details

IF YOU DO NOT KNOW THE ANSWER:
- Politely say you will check with the team and get back
- Ask for their phone number and email
- Never guess pricing or availability

RESPONSE STYLE:
- Keep responses concise (3-5 lines max)
- Be warm and helpful
- Occasionally use light Hinglish: "bilkul ji", "zaroor", "aapki seva mein"
- Always end with an offer to help further
"""

# ─── SESSION STATE ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "show_contact_form" not in st.session_state:
    st.session_state.show_contact_form = False

# ─── FUNCTIONS ─────────────────────────────────────────────────────────────────
def get_ai_response(user_message):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for m in st.session_state.messages[-10:]:
        messages.append({"role": m["role"], "content": m["content"]})
    messages.append({"role": "user", "content": user_message})
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.4,
        max_tokens=300
    )
    return response.choices[0].message.content

def text_to_speech(text):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            temp_path = f.name
        deepgram.speak.rest.v("1").save(
            temp_path,
            {"text": text},
            {"model": "aura-asteria-en"}
        )
        with open(temp_path, "rb") as f:
            audio_bytes = f.read()
        os.unlink(temp_path)
        return audio_bytes
    except Exception as e:
        return None

def transcribe_audio(audio_bytes):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            f.write(audio_bytes)
            temp_path = f.name
        with open(temp_path, "rb") as f:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                language="hi"
            )
        os.unlink(temp_path)
        return transcript.text
    except Exception as e:
        return None

def render_chat():
    chat_html = '<div class="chat-container">'
    if not st.session_state.messages:
        chat_html += '''<div class="msg-bot"><div class="bot-avatar">🌿</div>
        <div class="bubble">Namaste ji! 🙏 I am Priya, your Trev Assistant. How can I help you today?<br><br>
        Ask me about our <strong>airport transfers, rentals, or interstate trips</strong>. Type or use the voice button below!</div></div>'''
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            chat_html += f'<div class="msg-user"><div class="bubble">{msg["content"]}</div></div>'
        else:
            chat_html += f'<div class="msg-bot"><div class="bot-avatar">🌿</div><div class="bubble">{msg["content"]}</div></div>'
    chat_html += '</div>'
    st.markdown(chat_html, unsafe_allow_html=True)

# ─── UI ────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="trev-header">
    <p class="trev-logo">🚗 TREV</p>
    <p class="trev-tagline">Premium Electric Cab Service · Delhi NCR</p>
</div>
""", unsafe_allow_html=True)

render_chat()

st.markdown('<div class="voice-section"><p class="voice-label">🎙️ Tap to speak with Priya</p>', unsafe_allow_html=True)
audio_bytes = audio_recorder(
    text="",
    recording_color="#2E7D52",
    neutral_color="#1B4D32",
    icon_size="2x",
    pause_threshold=2.0
)
st.markdown('</div>', unsafe_allow_html=True)

col1, col2 = st.columns([5, 1])
with col1:
    user_input = st.text_input("", placeholder="Type your message here...", label_visibility="collapsed", key="text_input")
with col2:
    send_btn = st.button("Send →")

if audio_bytes and len(audio_bytes) > 1000:
    if "last_audio" not in st.session_state or st.session_state.last_audio != audio_bytes:
        st.session_state.last_audio = audio_bytes
        with st.spinner("Priya is listening..."):
            transcript = transcribe_audio(audio_bytes)
            if transcript:
                st.session_state.messages.append({"role": "user", "content": f"🎙️ {transcript}"})
                response = get_ai_response(transcript)
                st.session_state.messages.append({"role": "assistant", "content": response})
                if any(word in response.lower() for word in ["check with", "get back", "team"]):
                    st.session_state.show_contact_form = True
                audio_response = text_to_speech(response)
                if audio_response:
                    st.audio(audio_response, format="audio/mp3", autoplay=True)
                st.rerun()

if (send_btn or user_input) and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("Priya is thinking..."):
        response = get_ai_response(user_input)
    st.session_state.messages.append({"role": "assistant", "content": response})
    if any(word in response.lower() for word in ["check with", "get back", "team"]):
        st.session_state.show_contact_form = True
    audio_response = text_to_speech(response)
    if audio_response:
        st.audio(audio_response, format="audio/mp3", autoplay=True)
    st.rerun()

if st.session_state.show_contact_form:
    st.markdown("### 📋 Leave Your Details")
    st.caption("Our team will get back to you shortly.")
    with st.form("contact_form"):
        name = st.text_input("Your Name")
        phone = st.text_input("Phone Number")
        email = st.text_input("Email Address")
        query = st.text_area("Your Query", height=80)
        submitted = st.form_submit_button("Submit →")
        if submitted and phone and email:
            st.success("✅ Shukriya ji! Our team will contact you within 2 hours.")
            st.session_state.show_contact_form = False

with st.expander("🚗 Quick Rate Reference"):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**✈️ Airport**")
        st.markdown('<div class="info-card"><strong>BYD 7-Seater</strong><br>Rs 1,500 per trip</div>', unsafe_allow_html=True)
        st.markdown('<div class="info-card"><strong>MG ZS</strong><br>Rs 1,400 per trip</div>', unsafe_allow_html=True)
    with col2:
        st.markdown("**🕐 Rentals**")
        st.markdown('<div class="info-card"><strong>MG ZS</strong> — Rs 30/km<br>2hr/20km: Rs 600 | 4hr: Rs 1,200</div>', unsafe_allow_html=True)
        st.markdown('<div class="info-card"><strong>BYD</strong> — Rs 35/km<br>2hr/20km: Rs 700 | 4hr: Rs 1,400</div>', unsafe_allow_html=True)

with st.expander("⭐ Share Your Feedback"):
    with st.form("feedback_form"):
        rating = st.select_slider("Rate your experience", options=["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"], value="⭐⭐⭐⭐⭐")
        feedback = st.text_area("Tell us more (optional)", height=80)
        fb_submitted = st.form_submit_button("Submit Feedback →")
        if fb_submitted:
            st.success("💚 Thank you for your feedback!")

if st.session_state.messages:
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.session_state.show_contact_form = False
        st.rerun()

st.markdown("""
<div style='text-align:center; padding: 2rem 0 1rem; color: #6B7280; font-size: 0.78rem; letter-spacing: 1px;'>
    🌿 TREV CABS · PREMIUM EV EXPERIENCE · DELHI NCR<br>
    <span style='color:#2E7D52'>Noise-free · Eco-friendly · Carbon-neutral journeys</span>
</div>
""", unsafe_allow_html=True)
