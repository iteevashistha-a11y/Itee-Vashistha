import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Car Engineering India – Career Hub",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CUSTOM CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Exo+2:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Exo 2', sans-serif;
}

/* Background */
.stApp {
    background: linear-gradient(135deg, #0a0e1a 0%, #0d1b2a 50%, #0a0e1a 100%);
    color: #e0e8f0;
}

/* Hero Banner */
.hero-banner {
    background: linear-gradient(135deg, #0f1923 0%, #1a2a3a 40%, #0d2137 100%);
    border: 1px solid rgba(255,140,0,0.3);
    border-radius: 16px;
    padding: 40px 50px;
    margin-bottom: 30px;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 220px; height: 220px;
    background: radial-gradient(circle, rgba(255,140,0,0.12) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-banner::after {
    content: '';
    position: absolute;
    bottom: -60px; left: 10%;
    width: 400px; height: 400px;
    background: radial-gradient(ellipse, rgba(0,162,255,0.06) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: 3rem;
    font-weight: 700;
    background: linear-gradient(90deg, #FF8C00, #FFD700, #FF6B35);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 8px 0;
    letter-spacing: 2px;
}
.hero-subtitle {
    font-family: 'Exo 2', sans-serif;
    font-size: 1.1rem;
    color: #8ab4cc;
    margin: 0;
    letter-spacing: 1px;
}

/* Metric cards */
.metric-row { display: flex; gap: 16px; margin-bottom: 24px; }
.metric-card {
    flex: 1;
    background: linear-gradient(135deg, #111d2b, #162030);
    border: 1px solid rgba(255,140,0,0.2);
    border-left: 4px solid #FF8C00;
    border-radius: 10px;
    padding: 20px 24px;
    text-align: center;
}
.metric-card .metric-value {
    font-family: 'Rajdhani', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: #FF8C00;
}
.metric-card .metric-label {
    font-size: 0.8rem;
    color: #8ab4cc;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 4px;
}

/* Section headers */
.section-header {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.7rem;
    font-weight: 700;
    color: #FFB347;
    letter-spacing: 2px;
    border-bottom: 2px solid rgba(255,140,0,0.3);
    padding-bottom: 8px;
    margin-bottom: 20px;
}

/* Institute cards */
.institute-card {
    background: linear-gradient(135deg, #111d2b, #0e1922);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 14px;
    transition: border-color 0.3s;
    position: relative;
    overflow: hidden;
}
.institute-card:hover { border-color: rgba(255,140,0,0.4); }
.institute-name {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.2rem;
    font-weight: 700;
    color: #e8f4ff;
}
.institute-tier {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    margin-left: 10px;
}
.tier-premium { background: rgba(255,140,0,0.2); color: #FFD700; border: 1px solid rgba(255,215,0,0.4); }
.tier-top { background: rgba(0,180,255,0.15); color: #5bc8f5; border: 1px solid rgba(91,200,245,0.4); }
.tier-good { background: rgba(50,205,50,0.15); color: #7ddf7d; border: 1px solid rgba(125,223,125,0.4); }

.star-rating { color: #FFB347; font-size: 0.95rem; }
.badge {
    display: inline-block;
    background: rgba(255,140,0,0.12);
    border: 1px solid rgba(255,140,0,0.25);
    color: #FFA040;
    border-radius: 4px;
    padding: 1px 8px;
    font-size: 0.72rem;
    margin: 2px;
}

/* Company cards */
.company-card {
    background: #0e1822;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 10px;
    padding: 16px 18px;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 14px;
}
.company-logo {
    width: 44px; height: 44px;
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.3rem;
    font-weight: 700;
    flex-shrink: 0;
}
.company-name { font-family: 'Rajdhani', sans-serif; font-size: 1rem; font-weight: 700; color: #e0e8f0; }
.company-role { font-size: 0.78rem; color: #7a9bb8; margin-top: 2px; }
.salary-badge {
    margin-left: auto;
    background: rgba(50,180,50,0.15);
    border: 1px solid rgba(50,205,50,0.3);
    color: #6ddf6d;
    border-radius: 6px;
    padding: 4px 10px;
    font-size: 0.78rem;
    font-weight: 600;
    white-space: nowrap;
    flex-shrink: 0;
}

/* Course cards */
.course-card {
    background: linear-gradient(135deg, #111d2b, #0e1922);
    border: 1px solid rgba(91,200,245,0.2);
    border-top: 3px solid #00a2ff;
    border-radius: 10px;
    padding: 18px;
    margin-bottom: 14px;
}
.course-name { font-family: 'Rajdhani', sans-serif; font-size: 1.05rem; font-weight: 600; color: #5bc8f5; }
.course-meta { font-size: 0.78rem; color: #7a9bb8; margin-top: 4px; }
.course-topics { margin-top: 10px; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: #090e18 !important;
    border-right: 1px solid rgba(255,140,0,0.15);
}
[data-testid="stSidebar"] * { color: #c0d4e8 !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] { gap: 6px; background: transparent; }
.stTabs [data-baseweb="tab"] {
    background: rgba(255,255,255,0.04);
    border-radius: 8px 8px 0 0;
    color: #8ab4cc;
    font-family: 'Exo 2', sans-serif;
    border: 1px solid rgba(255,255,255,0.07);
    font-weight: 500;
}
.stTabs [aria-selected="true"] {
    background: rgba(255,140,0,0.15) !important;
    color: #FFB347 !important;
    border-color: rgba(255,140,0,0.4) !important;
}

/* Select/filter boxes */
.stSelectbox label, .stMultiSelect label, .stSlider label { color: #8ab4cc !important; font-size: 0.85rem; }

/* Info boxes */
.info-strip {
    background: rgba(0,162,255,0.08);
    border-left: 4px solid #00a2ff;
    border-radius: 0 8px 8px 0;
    padding: 10px 16px;
    margin: 12px 0;
    font-size: 0.88rem;
    color: #aad4f0;
}

hr { border-color: rgba(255,255,255,0.06); margin: 8px 0; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════ DATA ════════════════════════════════════════

INSTITUTES = [
    {
        "name": "IIT Madras", "city": "Chennai, Tamil Nadu", "type": "Government/IIT",
        "nirf_rank": 1, "rating": 4.9, "tier": "premium",
        "courses": ["B.Tech ME (Automotive Spec.)", "Dual Degree Engineering Design – Automotive", "M.Tech Automotive Eng."],
        "fee_lakh": 8.5, "avg_package_lpa": 18,
        "specializations": ["Autonomous Vehicles", "Powertrain Design", "Automotive Electronics"],
        "highlights": ["First Engineering Design Dept in India (2006)", "IIT-Madras Racing Formula SAE team", "DRDO & NASA collaborations"],
        "entrance": "JEE Advanced",
        "website": "https://www.iitm.ac.in"
    },
    {
        "name": "IIT Delhi", "city": "New Delhi", "type": "Government/IIT",
        "nirf_rank": 2, "rating": 4.8, "tier": "premium",
        "courses": ["B.Tech Mechanical (Automotive track)", "M.Tech Automotive Systems", "Ph.D. Automotive R&D"],
        "fee_lakh": 8.0, "avg_package_lpa": 20,
        "specializations": ["EV & Hybrid Tech", "Smart Transport", "Vehicle Dynamics"],
        "highlights": ["Electric Vehicle Cell funded by DST", "Collaboration with Bosch & MRF", "Top 200 QS World Rankings"],
        "entrance": "JEE Advanced",
        "website": "https://www.iitd.ac.in"
    },
    {
        "name": "IIT Kharagpur", "city": "Kharagpur, West Bengal", "type": "Government/IIT",
        "nirf_rank": 3, "rating": 4.8, "tier": "premium",
        "courses": ["B.Tech Mechanical with Auto Electives", "M.Tech Machine Design", "M.Tech Manufacturing Science"],
        "fee_lakh": 8.0, "avg_package_lpa": 17,
        "specializations": ["Vehicle Manufacturing", "CAD/CAM", "Lightweight Structures"],
        "highlights": ["NIRF #5 overall engineering", "100+ industry partnerships", "Oldest IIT (1951)"],
        "entrance": "JEE Advanced",
        "website": "https://www.iitkgp.ac.in"
    },
    {
        "name": "VIT Vellore", "city": "Vellore, Tamil Nadu", "type": "Private (Deemed)",
        "nirf_rank": 15, "rating": 4.5, "tier": "top",
        "courses": ["B.Tech ME – Automotive Spec.", "M.Tech Automotive Engineering", "B.Tech Mechatronics"],
        "fee_lakh": 7.8, "avg_package_lpa": 7,
        "specializations": ["EV Systems", "Automotive Mechatronics", "Vehicle Testing & Validation"],
        "highlights": ["SMEC School since 1984", "Faculty with global PhDs", "SAE India club – national winners"],
        "entrance": "VITEEE",
        "website": "https://www.vit.ac.in"
    },
    {
        "name": "SRM IST Chennai", "city": "Kattankulathur, Tamil Nadu", "type": "Private (Deemed)",
        "nirf_rank": 20, "rating": 4.3, "tier": "top",
        "courses": ["B.Tech Automobile Engineering", "M.Tech Automotive Engineering", "B.Tech Mechatronics"],
        "fee_lakh": 11.5, "avg_package_lpa": 6,
        "specializations": ["Advanced Automotive Labs", "EV Powertrain", "Autonomous Driving"],
        "highlights": ["Dedicated automobile labs", "Tata Motors MoU", "Formula Student racing team"],
        "entrance": "SRMJEEE",
        "website": "https://www.srmist.edu.in"
    },
    {
        "name": "PSG College of Technology", "city": "Coimbatore, Tamil Nadu", "type": "Private (Autonomous)",
        "nirf_rank": 40, "rating": 4.4, "tier": "top",
        "courses": ["B.E Automobile Engineering", "M.E Automotive Engineering", "Diploma Auto Engineering"],
        "fee_lakh": 4.5, "avg_package_lpa": 6,
        "specializations": ["Emission Control", "IC Engines", "Hybrid Vehicles"],
        "highlights": ["Oldest auto eng. dept in South India", "PSG-BOSCH Center of Excellence", "98% placement rate"],
        "entrance": "TNEA",
        "website": "https://www.psgtech.edu"
    },
    {
        "name": "Chandigarh University", "city": "Mohali, Punjab", "type": "Private",
        "nirf_rank": 20, "rating": 4.2, "tier": "top",
        "courses": ["B.E Automobile Engineering", "M.Tech Automotive Systems", "B.Tech Mechatronics"],
        "fee_lakh": 6.0, "avg_package_lpa": 5.5,
        "specializations": ["EV & Hybrid Vehicles", "Automotive Electronics", "Green Manufacturing"],
        "highlights": ["25+ patents filed by dept", "6.1x ROI – highest in region", "200+ research publications", "NAAC A+"],
        "entrance": "CUCET / JEE Main",
        "website": "https://www.cuchd.in"
    },
    {
        "name": "MIT Manipal", "city": "Manipal, Karnataka", "type": "Private (Deemed)",
        "nirf_rank": 35, "rating": 4.2, "tier": "top",
        "courses": ["B.Tech Automobile Engineering", "M.Tech Vehicle Engineering", "B.Tech Mechatronics"],
        "fee_lakh": 10.0, "avg_package_lpa": 6,
        "specializations": ["Alternative Fuels", "Vehicle Dynamics", "Hybrid Technology"],
        "highlights": ["Dedicated automobile workshop", "Collaboration with Toyota & Honda", "Strong alumni network"],
        "entrance": "MET / JEE Main",
        "website": "https://www.manipal.edu"
    },
    {
        "name": "College of Engineering Pune (COEP)", "city": "Pune, Maharashtra", "type": "Government (Autonomous)",
        "nirf_rank": 45, "rating": 4.3, "tier": "top",
        "courses": ["B.Tech Mechanical (Auto Electives)", "M.Tech Automotive Engineering", "B.Tech Mechatronics"],
        "fee_lakh": 1.5, "avg_package_lpa": 8,
        "specializations": ["Vehicle Design", "Pune Auto Cluster Projects", "Powertrain Eng."],
        "highlights": ["Located in India's Detroit – Pune", "ARAI collaboration", "Formula Bharat participants"],
        "entrance": "JEE Main / MHT-CET",
        "website": "https://www.coep.org.in"
    },
    {
        "name": "BITS Pilani", "city": "Pilani, Rajasthan", "type": "Private (Deemed)",
        "nirf_rank": 25, "rating": 4.6, "tier": "premium",
        "courses": ["B.E Mechanical + Automotive minor", "M.Tech Automotive Electronics (Online)", "Ph.D. Programs"],
        "fee_lakh": 15.7, "avg_package_lpa": 14,
        "specializations": ["Automotive Electronics", "Connected & Autonomous Vehicles", "EV Systems"],
        "highlights": ["BITS Practice School (work-integrated)", "Rs 2.54L affordable M.Tech fees", "Industry-sponsored research"],
        "entrance": "BITSAT",
        "website": "https://www.bits-pilani.ac.in"
    },
]

COMPANIES = [
    {"name": "Tata Motors", "emoji": "🚗", "color": "#1E3A5F", "roles": ["Design Engineer", "R&D Engineer", "Quality Engineer", "EV Systems Eng."], "salary": "₹5–18 LPA", "hq": "Mumbai"},
    {"name": "Maruti Suzuki", "emoji": "🔧", "color": "#C41E3A", "roles": ["Production Engineer", "Testing Engineer", "Vehicle Dynamics Eng.", "Embedded Systems"], "salary": "₹5–16 LPA", "hq": "New Delhi"},
    {"name": "Mahindra & Mahindra", "emoji": "🏭", "color": "#C75000", "roles": ["Automotive Design Eng.", "EV Powertrain Eng.", "Systems Integration", "R&D Lead"], "salary": "₹6–20 LPA", "hq": "Mumbai"},
    {"name": "Hyundai India", "emoji": "🇰🇷", "color": "#002C5F", "roles": ["CAE Engineer", "NVH Specialist", "Chassis Eng.", "Infotainment Systems"], "salary": "₹7–20 LPA", "hq": "Chennai"},
    {"name": "Bosch India", "emoji": "⚙️", "color": "#E20015", "roles": ["Automotive Electronics", "ADAS Engineer", "Fuel Systems Eng.", "IoT-Automotive"], "salary": "₹7–22 LPA", "hq": "Bengaluru"},
    {"name": "Bajaj Auto", "emoji": "🏍️", "color": "#0033A0", "roles": ["Powertrain Engineer", "Design & Styling Eng.", "Vehicle Testing", "EV R&D Eng."], "salary": "₹5–15 LPA", "hq": "Pune"},
    {"name": "Honda Cars India", "emoji": "🏎️", "color": "#CC0000", "roles": ["Production Engineer", "Quality Assurance", "R&D Engineer", "Vehicle Dynamics"], "salary": "₹5–16 LPA", "hq": "Greater Noida"},
    {"name": "TVS Motor Company", "emoji": "🛵", "color": "#004B87", "roles": ["Engine Design Eng.", "Manufacturing Eng.", "EV Systems Eng.", "Testing Specialist"], "salary": "₹5–15 LPA", "hq": "Chennai"},
    {"name": "ARAI (Govt. Research)", "emoji": "🔬", "color": "#2D7D46", "roles": ["Research Scientist", "Certification Eng.", "Emission Testing", "Vehicle Safety Eng."], "salary": "₹8–18 LPA", "hq": "Pune"},
    {"name": "Renault-Nissan Alliance", "emoji": "🌐", "color": "#EFCD00", "roles": ["Product Development", "Platform Engineer", "Embedded SW Eng.", "Styling Design"], "salary": "₹7–22 LPA", "hq": "Chennai"},
]

COURSES = [
    {
        "level": "Undergraduate", "degree": "B.Tech / B.E. Automobile Engineering",
        "duration": "4 Years", "entrance": "JEE Main / JEE Advanced / State CETs",
        "topics": ["Engineering Mechanics", "Thermodynamics", "IC Engines", "Vehicle Dynamics", "Automotive Electrical Systems", "CAD/CAM", "Manufacturing Processes", "Emission Control"],
        "avg_fee_range": "₹1.5L – ₹12L total", "career_paths": ["Design Engineer", "Quality Engineer", "R&D Engineer"]
    },
    {
        "level": "Undergraduate", "degree": "B.Tech Mechanical Engineering (Automotive Specialization)",
        "duration": "4 Years", "entrance": "JEE Advanced (IITs) / JEE Main (NITs)",
        "topics": ["Advanced Thermodynamics", "Fluid Mechanics", "Vehicle Powertrain", "Automotive Electronics", "Finite Element Analysis", "Robotics & Mechatronics"],
        "avg_fee_range": "₹2L – ₹15L total", "career_paths": ["Powertrain Engineer", "Simulation Engineer", "Product Development"]
    },
    {
        "level": "Postgraduate", "degree": "M.Tech / M.E. Automotive Engineering",
        "duration": "2 Years", "entrance": "GATE (Mechanical / Production Eng.)",
        "topics": ["Advanced Vehicle Dynamics", "Automotive Embedded Systems", "EV & Hybrid Powertrain", "ADAS & Autonomous Systems", "Crash Safety Engineering", "Vehicle NVH"],
        "avg_fee_range": "₹1L – ₹5L total", "career_paths": ["Senior R&D Engineer", "ADAS Specialist", "EV Systems Lead"]
    },
    {
        "level": "Postgraduate", "degree": "M.Tech Automotive Electronics (BITS Pilani Online)",
        "duration": "2 Years (Part-time)", "entrance": "GATE / Work Experience",
        "topics": ["Automotive Embedded Systems", "CAN/LIN/FlexRay Protocols", "AUTOSAR", "Connected Vehicles", "Battery Management Systems"],
        "avg_fee_range": "₹2.54L total (affordable)", "career_paths": ["Automotive Software Eng.", "ECU Developer", "IoT Specialist"]
    },
    {
        "level": "Diploma", "degree": "Diploma in Automobile Engineering",
        "duration": "3 Years", "entrance": "10th Pass + State Polytechnic Exam",
        "topics": ["Engine Overhaul", "Vehicle Body Repair", "Electrical Systems", "Fuel Systems", "Chassis & Transmission"],
        "avg_fee_range": "₹20K – ₹1L total", "career_paths": ["Auto Technician", "Workshop Supervisor", "Service Advisor"]
    },
    {
        "level": "Certification", "degree": "NSDC / ASDC Certification Courses",
        "duration": "3–6 Months", "entrance": "10th / 12th Pass",
        "topics": ["EV Servicing & Repair", "ADAS Calibration", "Connected Car Tech", "Diagnostics (OBD)", "Hybrid Vehicle Systems"],
        "avg_fee_range": "₹10K – ₹50K", "career_paths": ["EV Service Tech", "Diagnostics Expert", "Dealership Specialist"]
    },
]

# ═══════════════════════════════ SIDEBAR ════════════════════════════════════

with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 16px 0 8px 0;">
        <div style="font-family: 'Rajdhani'; font-size: 1.5rem; font-weight: 700; color: #FF8C00; letter-spacing: 2px;">🏎️ CAR ENG. INDIA</div>
        <div style="font-size: 0.75rem; color: #5a7a94; margin-top: 4px;">Career Intelligence Hub</div>
    </div>
    <hr style="border-color: rgba(255,140,0,0.2); margin: 8px 0 16px 0;"/>
    """, unsafe_allow_html=True)

    section = st.radio(
        "📍 Navigate",
        ["🏠 Overview", "🏛️ Institutes", "📚 Courses", "🏢 Companies & Careers", "📊 Analytics"],
        label_visibility="collapsed"
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.78rem; color: #4a6a84; font-weight:600; letter-spacing:1px; text-transform: uppercase;">Quick Filters</div>', unsafe_allow_html=True)

    filter_type = st.multiselect("Institution Type", ["Government/IIT", "Government (Autonomous)", "Private (Deemed)", "Private"], default=["Government/IIT", "Government (Autonomous)", "Private (Deemed)", "Private"])
    min_rating = st.slider("Minimum Rating", 3.5, 5.0, 4.0, 0.1)
    budget = st.slider("Max Fee (₹ Lakhs)", 1, 20, 20)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background: rgba(255,140,0,0.06); border: 1px solid rgba(255,140,0,0.15); border-radius: 8px; padding: 12px; font-size: 0.78rem; color: #8ab4cc;">
    💡 <b style="color:#FFB347">India's Auto Industry</b> is expected to reach <b style="color:#FFB347">$300B by 2026</b>. Over <b style="color:#FFB347">1.5 lakh engineers</b> are employed in this sector!
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════ MAIN CONTENT ════════════════════════════════

# HERO
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">🏎️ CAR ENGINEERING IN INDIA</div>
    <div class="hero-subtitle">Your Complete Career Intelligence Hub — Institutes • Courses • Companies • Salaries</div>
    <br>
    <div style="display: flex; gap: 30px; flex-wrap: wrap; margin-top: 8px;">
        <div style="text-align: center;">
            <div style="font-family: 'Rajdhani'; font-size: 2rem; font-weight: 700; color: #FF8C00;">39+</div>
            <div style="font-size: 0.72rem; color: #7a9bb8; letter-spacing: 1px;">INSTITUTES</div>
        </div>
        <div style="text-align: center;">
            <div style="font-family: 'Rajdhani'; font-size: 2rem; font-weight: 700; color: #5bc8f5;">$300B</div>
            <div style="font-size: 0.72rem; color: #7a9bb8; letter-spacing: 1px;">INDUSTRY BY 2026</div>
        </div>
        <div style="text-align: center;">
            <div style="font-family: 'Rajdhani'; font-size: 2rem; font-weight: 700; color: #7ddf7d;">₹22 LPA</div>
            <div style="font-size: 0.72rem; color: #7a9bb8; letter-spacing: 1px;">TOP PACKAGE</div>
        </div>
        <div style="text-align: center;">
            <div style="font-family: 'Rajdhani'; font-size: 2rem; font-weight: 700; color: #FFD700;">1.5L+</div>
            <div style="font-size: 0.72rem; color: #7a9bb8; letter-spacing: 1px;">ENGINEERS EMPLOYED</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ─── FILTER DATA ─────────────────────────────────────────────────────────────
filtered = [i for i in INSTITUTES
            if i["type"] in filter_type
            and i["rating"] >= min_rating
            and i["fee_lakh"] <= budget]


# ════════════════ SECTION: OVERVIEW ══════════════════════════════════════════
if "Overview" in section:
    st.markdown('<div class="section-header">📌 Industry Overview</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #111d2b, #0e1a28); border: 1px solid rgba(255,140,0,0.2); border-radius: 12px; padding: 20px;">
            <div style="font-family: 'Rajdhani'; font-size: 1.1rem; font-weight: 700; color: #FFB347; margin-bottom: 10px;">🎓 Education Paths</div>
            <div style="font-size: 0.85rem; color: #8ab4cc; line-height: 1.8;">
            • Diploma (3 yrs)<br>
            • B.Tech / B.E. (4 yrs)<br>
            • M.Tech / M.E. (2 yrs)<br>
            • Ph.D. Research (3–5 yrs)<br>
            • NSDC Certification (3–6 mo)
            </div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #111d2b, #0e1a28); border: 1px solid rgba(0,162,255,0.2); border-radius: 12px; padding: 20px;">
            <div style="font-family: 'Rajdhani'; font-size: 1.1rem; font-weight: 700; color: #5bc8f5; margin-bottom: 10px;">🔥 Hot Specializations</div>
            <div style="font-size: 0.85rem; color: #8ab4cc; line-height: 1.8;">
            • Electric Vehicle (EV) Systems<br>
            • ADAS & Autonomous Driving<br>
            • Automotive Embedded SW<br>
            • Vehicle Dynamics & NVH<br>
            • Hydrogen & Alternative Fuels
            </div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #111d2b, #0e1a28); border: 1px solid rgba(50,205,50,0.2); border-radius: 12px; padding: 20px;">
            <div style="font-family: 'Rajdhani'; font-size: 1.1rem; font-weight: 700; color: #7ddf7d; margin-bottom: 10px;">📈 Salary Ranges</div>
            <div style="font-size: 0.85rem; color: #8ab4cc; line-height: 1.8;">
            • Fresher: ₹4.5 – ₹8 LPA<br>
            • 3–5 yrs exp: ₹10 – ₹18 LPA<br>
            • Senior (7+ yrs): ₹18 – ₹30 LPA<br>
            • R&D Lead: ₹25 – ₹45 LPA<br>
            • IIT Graduates: up to ₹22 LPA start
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">🗺️ Key Automotive Hubs in India</div>', unsafe_allow_html=True)

    hubs = [
        ("Chennai", "India's Detroit – Hyundai, Ford, BMW, Renault-Nissan", "#FF6B35"),
        ("Pune", "ARAI Headquarters, Bajaj Auto, Tata Motors, Fiat", "#00A2FF"),
        ("NCR Delhi", "Maruti Suzuki, Honda Cars, Hero MotoCorp, Yamaha", "#FFD700"),
        ("Bengaluru", "Bosch, Toyota, TVS, R&D centres of MNCs", "#7ddf7d"),
        ("Mumbai", "Tata Motors HQ, Mahindra, Ashok Leyland", "#C084FC"),
        ("Rajkot/Ahmedabad", "Auto components hub, SME cluster", "#F97316"),
    ]
    cols = st.columns(3)
    for i, (city, desc, color) in enumerate(hubs):
        with cols[i % 3]:
            st.markdown(f"""
            <div style="background: #0e1822; border-left: 4px solid {color}; border-radius: 0 8px 8px 0; padding: 12px 16px; margin-bottom: 12px;">
                <div style="font-family: 'Rajdhani'; font-size: 1rem; font-weight: 700; color: {color};">📍 {city}</div>
                <div style="font-size: 0.78rem; color: #7a9bb8; margin-top: 4px;">{desc}</div>
            </div>""", unsafe_allow_html=True)


# ════════════════ SECTION: INSTITUTES ════════════════════════════════════════
elif "Institutes" in section:
    st.markdown(f'<div class="section-header">🏛️ Top Automobile Engineering Institutes ({len(filtered)} found)</div>', unsafe_allow_html=True)

    sort_by = st.selectbox("Sort by", ["Rating (High→Low)", "NIRF Rank", "Fee (Low→High)", "Avg Package (High→Low)"], label_visibility="visible")

    if sort_by == "Rating (High→Low)":
        filtered.sort(key=lambda x: -x["rating"])
    elif sort_by == "NIRF Rank":
        filtered.sort(key=lambda x: x["nirf_rank"])
    elif sort_by == "Fee (Low→High)":
        filtered.sort(key=lambda x: x["fee_lakh"])
    else:
        filtered.sort(key=lambda x: -x["avg_package_lpa"])

    for inst in filtered:
        stars = "⭐" * int(inst["rating"]) + ("½" if inst["rating"] % 1 >= 0.5 else "")
        tier_class = f"tier-{inst['tier']}"
        tier_label = {"premium": "🥇 PREMIUM", "top": "🥈 TOP TIER", "good": "🥉 GOOD"}[inst["tier"]]

        with st.expander(f"{'🏆' if inst['tier']=='premium' else '🎓'} {inst['name']} — {inst['city']}", expanded=False):
            c1, c2, c3 = st.columns([2, 1, 1])
            with c1:
                st.markdown(f"""
                <span class="institute-tier {tier_class}">{tier_label}</span>
                <span style="margin-left:10px; font-size:0.85rem; color:#5bc8f5;">⭐ {inst['rating']}/5.0</span>
                <span style="margin-left:10px; font-size:0.85rem; color:#8ab4cc;">NIRF #{inst['nirf_rank']}</span>
                """, unsafe_allow_html=True)
                st.markdown(f"<div style='font-size:0.82rem; color:#7a9bb8; margin-top:6px;'>📍 {inst['city']} &nbsp;|&nbsp; 🏛️ {inst['type']} &nbsp;|&nbsp; 📝 {inst['entrance']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='font-size:0.82rem; color:#5a9478; margin-top:4px;'>💰 Total Fee: ~₹{inst['fee_lakh']}L &nbsp;|&nbsp; 📈 Avg Package: ₹{inst['avg_package_lpa']} LPA</div>", unsafe_allow_html=True)
            with c2:
                st.markdown("**🎯 Specializations**")
                for s in inst["specializations"]:
                    st.markdown(f'<span class="badge">{s}</span>', unsafe_allow_html=True)
            with c3:
                st.markdown("**✨ Highlights**")
                for h in inst["highlights"]:
                    st.markdown(f"<div style='font-size:0.78rem; color:#8ab4cc; padding: 2px 0;'>▸ {h}</div>", unsafe_allow_html=True)

            st.markdown("**📚 Courses Offered:**")
            for course in inst["courses"]:
                st.markdown(f'<span class="badge" style="background:rgba(0,162,255,0.1); border-color:rgba(0,162,255,0.3); color:#5bc8f5;">{course}</span>', unsafe_allow_html=True)


# ════════════════ SECTION: COURSES ═══════════════════════════════════════════
elif "Courses" in section:
    st.markdown('<div class="section-header">📚 Courses & Programs in Automobile Engineering</div>', unsafe_allow_html=True)

    level_filter = st.multiselect("Filter by Level", ["Undergraduate", "Postgraduate", "Diploma", "Certification"],
                                   default=["Undergraduate", "Postgraduate", "Diploma", "Certification"])

    for course in COURSES:
        if course["level"] not in level_filter:
            continue
        level_color = {"Undergraduate": "#00a2ff", "Postgraduate": "#FF8C00", "Diploma": "#7ddf7d", "Certification": "#C084FC"}[course["level"]]
        with st.expander(f"📖 {course['degree']} ({course['duration']})", expanded=False):
            col1, col2 = st.columns([3, 2])
            with col1:
                st.markdown(f"""
                <div style="display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 12px;">
                    <span style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius:6px; padding: 4px 10px; font-size:0.8rem; color: {level_color};">📋 {course['level']}</span>
                    <span style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius:6px; padding: 4px 10px; font-size:0.8rem; color: #8ab4cc;">⏱️ {course['duration']}</span>
                    <span style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius:6px; padding: 4px 10px; font-size:0.8rem; color: #7ddf7d;">💰 {course['avg_fee_range']}</span>
                </div>
                <div style="font-size:0.85rem; color:#8ab4cc; margin-bottom:6px;">📝 <b>Entrance Exam:</b> {course['entrance']}</div>
                """, unsafe_allow_html=True)
                st.markdown("**🔬 Key Topics:**")
                topic_html = " ".join([f'<span class="badge">{t}</span>' for t in course["topics"]])
                st.markdown(topic_html, unsafe_allow_html=True)
            with col2:
                st.markdown("**🚀 Career Paths:**")
                for cp in course["career_paths"]:
                    st.markdown(f"<div style='font-size:0.85rem; color:#7ddf7d; padding: 3px 0;'>✅ {cp}</div>", unsafe_allow_html=True)


# ════════════════ SECTION: COMPANIES ═════════════════════════════════════════
elif "Companies" in section:
    st.markdown('<div class="section-header">🏢 Top Recruiters & Career Opportunities</div>', unsafe_allow_html=True)

    st.markdown("""<div class="info-strip">💼 India's automobile sector employs over 37 million people directly and indirectly. 
    Engineering graduates from IITs & NITs command starting packages of ₹10–22 LPA, while private college grads average ₹5–8 LPA.</div>""", unsafe_allow_html=True)

    for company in COMPANIES:
        roles_html = " ".join([f'<span class="badge">{r}</span>' for r in company["roles"]])
        st.markdown(f"""
        <div class="company-card">
            <div class="company-logo" style="background: {company['color']}22; border: 1px solid {company['color']}44; color: {company['color']};">
                {company['emoji']}
            </div>
            <div style="flex: 1;">
                <div class="company-name">{company['name']}</div>
                <div class="company-role">📍 HQ: {company['hq']}</div>
                <div style="margin-top: 6px;">{roles_html}</div>
            </div>
            <div class="salary-badge">{company['salary']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">🌍 Global OEM Presence in India</div>', unsafe_allow_html=True)

    global_companies = [
        ("Hyundai Motor India", "Chennai", "Korean OEM, 2nd largest carmaker in India"),
        ("Toyota Kirloskar", "Bidadi, Karnataka", "Japanese OEM, RAV4 & Innova production"),
        ("BMW India", "Chennai", "German luxury brand, local assembly unit"),
        ("Mercedes-Benz India", "Pune", "German luxury, India's largest luxury OEM"),
        ("Ford India (R&D)", "Chennai", "Major R&D and engineering hub"),
        ("Volkswagen India", "Pune", "German OEM, Skoda-VW India tech centre"),
    ]
    cols = st.columns(2)
    for i, (name, loc, desc) in enumerate(global_companies):
        with cols[i % 2]:
            st.markdown(f"""
            <div style="background: #0e1822; border: 1px solid rgba(255,255,255,0.06); border-radius: 8px; padding: 12px 16px; margin-bottom: 10px;">
                <div style="font-family: 'Rajdhani'; font-size: 0.95rem; font-weight: 700; color: #5bc8f5;">{name}</div>
                <div style="font-size: 0.78rem; color: #4a7a9b;">📍 {loc}</div>
                <div style="font-size: 0.78rem; color: #8ab4cc; margin-top: 4px;">{desc}</div>
            </div>""", unsafe_allow_html=True)


# ════════════════ SECTION: ANALYTICS ═════════════════════════════════════════
elif "Analytics" in section:
    st.markdown('<div class="section-header">📊 Analytics & Insights</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        df_inst = pd.DataFrame(INSTITUTES)
        fig1 = px.scatter(
            df_inst, x="fee_lakh", y="avg_package_lpa",
            size="rating", color="type", hover_name="name",
            title="Fee vs Avg Package (bubble = rating)",
            labels={"fee_lakh": "Total Fee (₹ Lakhs)", "avg_package_lpa": "Avg Package (LPA)"},
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        fig1.update_layout(
            paper_bgcolor="#0d1b2a", plot_bgcolor="#0d1b2a",
            font_color="#c0d4e8", title_font_color="#FFB347",
            legend=dict(bgcolor="rgba(0,0,0,0.3)", bordercolor="rgba(255,255,255,0.1)")
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = px.bar(
            df_inst.sort_values("rating", ascending=True),
            x="rating", y="name", orientation="h",
            title="Institute Ratings Comparison",
            color="rating",
            color_continuous_scale=["#1a3050", "#FF8C00", "#FFD700"],
        )
        fig2.update_layout(
            paper_bgcolor="#0d1b2a", plot_bgcolor="#0d1b2a",
            font_color="#c0d4e8", title_font_color="#FFB347",
            coloraxis_showscale=False, height=420,
            yaxis=dict(tickfont=dict(size=10))
        )
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        type_counts = df_inst["type"].value_counts().reset_index()
        type_counts.columns = ["Type", "Count"]
        fig3 = px.pie(type_counts, values="Count", names="Type",
                      title="Distribution by Institution Type",
                      color_discrete_sequence=["#FF8C00", "#00A2FF", "#7ddf7d", "#C084FC"])
        fig3.update_layout(paper_bgcolor="#0d1b2a", font_color="#c0d4e8", title_font_color="#FFB347")
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        salary_data = pd.DataFrame({
            "Experience": ["Fresher", "1–3 Years", "3–5 Years", "5–8 Years", "8–12 Years", "12+ Years"],
            "Min LPA": [4.5, 6, 10, 14, 20, 28],
            "Max LPA": [8, 12, 18, 24, 35, 50]
        })
        fig4 = go.Figure()
        fig4.add_trace(go.Bar(name="Min", x=salary_data["Experience"], y=salary_data["Min LPA"],
                              marker_color="#1a5276"))
        fig4.add_trace(go.Bar(name="Max", x=salary_data["Experience"], y=salary_data["Max LPA"],
                              marker_color="#FF8C00"))
        fig4.update_layout(
            title="Salary Growth by Experience (LPA)",
            barmode="group", paper_bgcolor="#0d1b2a", plot_bgcolor="#0d1b2a",
            font_color="#c0d4e8", title_font_color="#FFB347",
            legend=dict(bgcolor="rgba(0,0,0,0.3)")
        )
        st.plotly_chart(fig4, use_container_width=True)

    # Skills radar
    st.markdown('<div class="section-header">🎯 Most In-Demand Skills (2024–2026)</div>', unsafe_allow_html=True)
    skills_df = pd.DataFrame({
        "Skill": ["EV Systems", "ADAS/AV", "Embedded SW", "CAD/CAE", "Vehicle Dynamics", "NVH Eng.", "Alt. Fuels", "Manufacturing"],
        "Demand Score": [95, 90, 88, 82, 78, 72, 68, 75],
        "Avg Salary Premium": [30, 35, 28, 15, 18, 14, 20, 10]
    })
    fig5 = px.bar(skills_df, x="Demand Score", y="Skill", orientation="h",
                  color="Avg Salary Premium",
                  color_continuous_scale=["#1a3050", "#FF8C00", "#FFD700"],
                  title="Skill Demand vs Salary Premium (%)",
                  labels={"Avg Salary Premium": "Salary Premium %"})
    fig5.update_layout(paper_bgcolor="#0d1b2a", plot_bgcolor="#0d1b2a",
                       font_color="#c0d4e8", title_font_color="#FFB347")
    st.plotly_chart(fig5, use_container_width=True)


# ─── FOOTER ────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; padding: 20px; border-top: 1px solid rgba(255,140,0,0.15); margin-top: 20px;">
    <div style="font-family: 'Rajdhani'; color: #FFB347; font-size: 0.9rem; letter-spacing: 2px;">🏎️ CAR ENGINEERING INDIA · CAREER INTELLIGENCE HUB</div>
    <div style="font-size: 0.72rem; color: #4a6a84; margin-top: 6px;">Data sourced from NIRF Rankings 2024 · Careers360 · Shiksha.com · AICTE</div>
</div>
""", unsafe_allow_html=True)
