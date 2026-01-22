import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import time
from utils.data_loader import load_all_data



st.markdown("""
<style>
/* ===== MOBILE RESPONSIVENESS ===== */
@media (max-width: 768px) {

    .hero {
        padding: 2rem 1.5rem !important;
        border-radius: 16px !important;
    }

    .hero h1 {
        font-size: 1.6rem !important;
    }

    .hero p {
        font-size: 0.95rem !important;
    }

    .metric-card h2 {
        font-size: 1.5rem !important;
    }

    .metric-card {
        padding: 1rem !important;
    }

    /* Kill ticker on mobile */
    .ticker-wrapper {
        display: none !important;
    }
}
</style>
""", unsafe_allow_html=True)



st.set_page_config(
    page_title="Global Field Epidemiology Intelligence Platform",
    layout="wide" if st.session_state.get("is_desktop", True) else "centered",
    initial_sidebar_state="collapsed"
)
st.markdown("""
<style>
div[data-testid="stAlert"] {
    background-color: #b11226 !important;
    color: white !important;
    border-radius: 14px;
    border: none;
    font-weight: 700;
    box-shadow: 0 10px 30px rgba(177, 18, 38, 0.45);
}

div[data-testid="stAlert"] p {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)
# ==================================================
@st.cache_data
def load_countries():
    return pd.read_csv("data/countries.csv")

@st.cache_data
def load_programs():
    return pd.read_csv("data/programs.csv")

@st.cache_data
def load_metrics():
    return pd.read_csv("data/global_metrics.csv")

countries_df = load_countries()
programs_df = load_programs()
metrics_df = load_metrics()
#st.write("METRICS CSV COLUMNS 👉", metrics_df.columns.tolist())
#st.stop()

# ==================================================
# SESSION STATE
# ==================================================
if "entered" not in st.session_state:
    st.session_state.entered = False

if "selected_country" not in st.session_state:
    st.session_state.selected_country = "Nigeria"

if "role" not in st.session_state:
    st.session_state.role = None

if "user_role" not in st.session_state:
    st.session_state.user_role = "Visitor"

if "metrics_loaded" not in st.session_state:
    st.session_state.metrics_loaded = False

if "authorized" not in st.session_state:
    st.session_state.authorized = False


# ==================================================
# ROLE DEFINITIONS
# ==================================================
ROLES = {
    "Minister of Health": "National system oversight, workforce investment, outbreak readiness.",
    "Donor / Development Partner": "Funding alignment, ROI tracking, sustainability intelligence.",
    "WHO / CDC / Multilateral": "Global standards, credentialing, regional capacity coordination.",
    "National Secretariat / Analyst": "Operational monitoring, reporting, implementation support."
}


# ==================================================
# EXECUTIVE METRICS (STATIC MOCK – REPLACE LATER)
# ==================================================
METRICS = [
    ("🌍 Countries with FETPs", "102"),
    ("🎓 Active Training Programs", "320+"),
    ("🧑🏽‍⚕️ Trained Field Epidemiologists", "18,000+"),
    ("⚠️ Outbreaks Supported (5 yrs)", "1,450+")
]

def count_up(target, suffix="", duration=0.8):
    placeholder = st.empty()
    steps = 30
    delay = duration / steps

    for i in range(steps + 1):
        value = int(target * i / steps)
        placeholder.markdown(
            f"<h2 style='margin:0'>{value}{suffix}</h2>",
            unsafe_allow_html=True
        )
        time.sleep(delay)

    return placeholder

# ==================================================
# WELCOME PAGE
# ==================================================
def render_welcome_page():

    st.markdown("""
    <style>
    .hero {
        padding: 4.5rem 6rem 3.5rem;
        background: linear-gradient(135deg, #071a2b, #0c2d4a, #124b6b);
        border-radius: 28px;
        color: white;
        box-shadow: 0 30px 80px rgba(0,0,0,0.35);
    }

    .metric-card {
        background: #0e2238;
        padding: 1.8rem;
        border-radius: 18px;
        text-align: center;
        color: white;
        box-shadow: 0 12px 30px rgba(0,0,0,0.35);
    }

    .metric-card h2 {
        font-size: 2.4rem;
        margin-bottom: 0.4rem;
    }

    .metric-card p {
        font-size: 0.9rem;
        opacity: 0.85;
    }

    .enter-btn button {
        background: linear-gradient(135deg, #1fa84f, #1bc96b);
        font-weight: 800;
        padding: 0.9rem;
        border-radius: 14px;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

    # ---------------- HERO ----------------
    st.markdown("""
    <div class="hero">
        <h1>Global Field Epidemiology Intelligence Platform</h1>
        <p>
        Executive decision intelligence supporting global applied
        epidemiology workforce systems, credentialing readiness,
        and outbreak preparedness.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------- ROLE SELECT ----------------
    st.subheader("Select Access Profile")

    role = st.selectbox(
        "This tailors the intelligence briefing to your mandate",
        list(ROLES.keys())
    )

    st.info(ROLES[role])

    # ---------------- METRICS ----------------
    st.markdown("### Global System Snapshot")
    cols = st.columns(len(metrics_df))

    for col, (_, row) in zip(cols, metrics_df.iterrows()):
        with col:
            st.metric(
                label=row["metric"],
                value=row["value"]
            )

    # cols = st.columns(4)

    #metric_values = [
     #   ("🌍 Countries with FETPs", 102, ""),
      #  ("🎓 Active Training Programs", 320, "+"),
       # ("🧑🏽‍⚕️ Trained Field Epidemiologists", 18000, "+"),
        #("⚠️ Outbreaks Supported (5 yrs)", 1450, "+")
    #]

   # for col, (label, value, suffix) in zip(cols, metric_values):
     #   with col:
     #       st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
     #       count_up(value, suffix)
     #       st.markdown(f"<p>{label}</p>", unsafe_allow_html=True)
      #      st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- ENTER ----------------
    st.markdown('<div class="enter-btn">', unsafe_allow_html=True)
    if st.button("Proceed to Intelligence Briefing"):
        st.session_state.entered = True
        st.session_state.role = role
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)



    # ---------------- TICKER ----------------
    st.markdown("""
    <style>
    /* ---- GLOBAL TICKER FIX ---- */
    .ticker-wrapper {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100vw;
        background: #000;
        overflow: hidden;
        z-index: 9999;
        border-top: 1px solid #00ffd5;
    }

    .ticker-track {
        display: flex;
        width: max-content;
        animation: ticker-scroll 150s linear infinite;
        will-change: transform;
    }

    .ticker-item {
        color: #00ffd5;
        font-size: 0.92rem;
        font-weight: 700;
        white-space: nowrap;
        padding: 0.7rem 2rem;
    }

    @keyframes ticker-scroll {
        from {
            transform: translateX(0);
        }
        to {
            transform: translateX(-50%);
        }
    }
    </style>

    <div class="ticker-wrapper">
        <div class="ticker-track">
            <div class="ticker-item">
                🌍 Field Epidemiology Training Programs active in 100+ countries •
                TEPHINET coordinates global and regional FETP networks •
                WHO & CDC advancing applied epidemiology credentialing •
                One Health FETPs expanding zoonotic outbreak surveillance •
                Regional networks strengthening outbreak response capacity worldwide •
            </div>
            <div class="ticker-item">
                🌍 Field Epidemiology Training Programs active in 100+ countries •
                TEPHINET coordinates global and regional FETP networks •
                • Field Epidemiology Training Programs (FETPs) are competency‑based applied public health training programs designed to strengthen countries’ ability to detect, investigate, and respond to disease outbreaks and other public health threats • Trainees learn by doing — typically spending the majority of their time in real fieldwork rather than just classroom learning • FETPs have been established in more than 85 countries worldwide • They contribute directly to global health security and help countries meet International Health Regulations workforce capacity goals • FETPs are offered in three levels: Frontline (~3 months, basic outbreak detection and response) • Intermediate (~9–12 months, broader surveillance & analysis skills) • Advanced (~24 months, full epidemiologic field training and leadership) • Many countries structure their programs to include all three tiers; e.g., Nigeria’s NFETP has Integrated (Frontline), Intermediate, and Advanced tracks • FETP trainees and graduates support outbreak responses (Ebola, COVID‑19, cholera, etc.) • They strengthen surveillance systems and reporting quality • Graduates serve in leadership roles in ministries of health and international organizations • TEPHINET is the global professional network that connects FETPs and supports mentoring, quality improvement, and knowledge sharing • The Global Field Epidemiology Partnership (GFEP) coordinates investments and expansion of field epidemiology capacity worldwide • Relevant degrees for applicants: MPH, MSc/PhD in epidemiology, public health, or related fields make your application stronger • Gain experience or coursework in surveillance, outbreak investigation, and public health data analysis • Software skills like R, Python, SQL, or GIS are commonly used in epidemiology work • Start early: Many programs have annual application cycles • Tailor your application to how you can contribute to the specific country’s surveillance and response needs • Highlight any outbreak investigation, surveillance system work, or applied research experience — even internships/volunteer roles • A key FETP principle is fieldwork — expect to spend ~75 % of your time in real on‑the‑ground tasks • Build practical skills: real data analysis, outbreak response exercises, risk communication, and public health reporting are core activities • Networking with faculty, local health departments, and global peers enhances learning and career opportunities • Leverage your network: Field epidemiologists are well connected — TEPHINET and partners often help graduates find leadership roles • Keep learning: pursue short courses in areas like One Health epidemiology, lab surveillance, or emergency preparedness frameworks • Publish and share: contribute to outbreak reports or research publications — it builds credibility and impact • FETPs build a skilled epidemiologic workforce at the frontline of public health • Strengthen national and global outbreak response capacity • Improve surveillance, data quality, and health system resilience • Support career pathways in public health leadership
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ==================================================
# ROUTER
# ==================================================
if not st.session_state.entered:
    render_welcome_page()
    st.stop()




def render_dashboard():
    # SIDEBAR (only visible after entry)
    st.sidebar.markdown("## 🌍 Dashboard Controls")

    selected = st.sidebar.selectbox(
        "Select Country",
        options=sorted(countries_df["country"].unique()),
        index=sorted(countries_df["country"].unique()).index(
            st.session_state.selected_country
        )
    )

    # Update session state when user changes country
    st.session_state.selected_country = selected

    # MAIN CONTENT
    st.markdown(
        f"## 🇳🇬 Country Overview: {st.session_state.selected_country}"
    )

    country_programs = programs_df[
        programs_df["country"] == st.session_state.selected_country
        ]

    st.metric(
        "Active FETP Programs",
        len(country_programs)
    )


# ==================================================
# DASHBOARD CONTEXT (ROLE-AWARE)
# ==================================================
st.title("🌍 Global FETP Intelligence Dashboard")
st.caption(f"Access Profile: {st.session_state.role}")

st.success("Dashboard content now loads based on role permissions.")

render_dashboard()
# ==================================================
# WELCOME GATE ROUTER (STOP EXECUTION)
# ==================================================
if not st.session_state.entered:
    render_welcome_page()
    st.stop()


# ==================================================
# DASHBOARD STARTS BELOW THIS LINE
# ==================================================
#st.title("🌍 Global FETP Intelligence Dashboard")
#st.write("Main application content begins here.")

# ==================================================
# MAIN LANDING PAGE CONTENT
# ==================================================
st.image("assets/logo.png", width=120)
st.info(
    "Use the sidebar to navigate between sections. "
    "Your selected country remains active across all pages."
)
st.title("This is a Global Field Epidemiology Training & Credentialing Ecosystem by Daniel Onimisi(da.zx@outlook.com)")

st.markdown(
    """
This interactive platform supports the **Global Field Epidemiology Partnership (GFEP)**  
by mapping **Field Epidemiology Training Programs (FETPs/FELTPs)**, networks, institutions,  
and **credentialing readiness** across regions.

### What you can explore:
- Global metrics and geographic coverage  
- Regional epidemiology networks  
- National training programs and workforce gaps  
- Training modalities and pipelines  
- Credentialing governance and readiness  

All pages are synchronized using the **country selector on the left** to provide a  
**consultant-grade, decision-ready experience**.
"""
)



# ==================================================
# COUNTRY SNAPSHOT (EXECUTIVE SUMMARY)
# ==================================================
selected_country = st.session_state.selected_country

country_programs = programs_df[programs_df["country"] == selected_country]
country_meta = countries_df[countries_df["country"] == selected_country]

# --------------------------------------------------
# DERIVED METRICS
# --------------------------------------------------
num_programs = len(country_programs)
num_accredited = (country_programs["accredited"] == "Yes").sum()
modalities = country_programs["modality"].dropna().unique()

current_year = datetime.now().year

if not country_programs.empty:
    years_active = current_year - country_programs["established"].min()
else:
    years_active = 0

# ==================================================
# COUNTRY-SPECIFIC GOVERNANCE & READINESS METRICS
# (MUST BE DEFINED BEFORE FLOWCHART UI)
# ==================================================

# Defensive check
if country_programs.empty:
    host_institutions = []
    total_programs = 0
    accredited_programs = 0
    modalities_present = []
    network_membership = []
    years_active = 0
else:
    # Host institutions
    host_institutions = (
        country_programs["host_institution"]
        .dropna()
        .unique()
        .tolist()
    )

    # Program counts
    total_programs = len(country_programs)
    accredited_programs = (
        country_programs["accredited"].str.lower() == "yes"
    ).sum()

    # Modalities
    modalities_present = (
        country_programs["modality"]
        .dropna()
        .unique()
        .tolist()
    )

    # Network participation
    network_membership = (
        country_programs["network"]
        .dropna()
        .unique()
        .tolist()
    )

    # Institutional maturity proxy
    years_active = (
        2025 - country_programs["established"].min()
        if pd.notna(country_programs["established"].min())
        else 0
    )


# --------------------------------------------------
# CREDENTIALING READINESS SCORE (0–100)
# --------------------------------------------------

# 1. Program maturity (max 30)
maturity_score = min((years_active / 25) * 30, 30)

# 2. Accreditation strength (max 30)
accreditation_score = (
    (num_accredited / num_programs) * 30 if num_programs > 0 else 0
)

# 3. Modality breadth (max 20)
modality_score = min(len(modalities) / 3 * 20, 20)

# 4. Network integration (max 20)
network_score = (
    20 if country_programs["tephinet_member"].eq("Yes").any() else 0
)

# Final score
readiness_score = round(
    maturity_score + accreditation_score + modality_score + network_score
)

# Color & label
if readiness_score >= 75:
    readiness_color = "🟢"
    readiness_label = "High Readiness"
elif readiness_score >= 50:
    readiness_color = "🟠"
    readiness_label = "Moderate Readiness"
else:
    readiness_color = "🔴"
    readiness_label = "Emerging Readiness"

# ==================================================
# SNAPSHOT UI
# ==================================================
st.markdown(f"## 📍 Country Snapshot — **{selected_country}**")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="WHO Region",
        value=country_meta["who_region"].values[0]
    )

with col2:
    st.metric(
        label="Active Training Programs",
        value=num_programs
    )

with col3:
    st.metric(
        label="Accredited Programs",
        value=num_accredited
    )

with col4:
    st.metric(
        label="Readiness Score",
        value=f"{readiness_score}/100"
    )

# --------------------------------------------------
# READINESS DETAIL PANEL
# --------------------------------------------------
st.markdown("### 🧭 Credentialing Readiness Index")

left, right = st.columns([1, 3])

with left:
    st.markdown(
        f"""
        ## {readiness_color}  
        **{readiness_label}**
        """
    )

with right:
    st.markdown(
        f"""
        **Score breakdown**
        - 🏛 Program maturity: **{round(maturity_score,1)} / 30**
        - 🏅 Accreditation strength: **{round(accreditation_score,1)} / 30**
        - 🎓 Modality breadth: **{round(modality_score,1)} / 20**
        - 🌐 Network integration: **{round(network_score,1)} / 20**
        """
    )

# --------------------------------------------------
# MODALITIES SUMMARY
# --------------------------------------------------
if len(modalities) > 0:
    st.markdown(
        f"**Training modalities present:** {', '.join(modalities)}"
    )
else:
    st.markdown("**Training modalities present:** Not specified")

st.info(
    "This snapshot provides a high-level executive overview. "
    "Navigate to other sections for detailed maps, governance flows, "
    "and program-level diagnostics."
)
# ==================================================
# COUNTRY-SPECIFIC READINESS RECOMMENDATIONS
# ==================================================
st.markdown("## 🛠 Country-Specific Readiness Recommendations")

recommendations = []

# Accreditation gap
if num_programs > 0 and num_accredited == 0:
    recommendations.append(
        "🏅 **Expand accreditation**: No accredited programs detected. "
        "Prioritize accreditation pathways with regional or global bodies."
    )

elif num_programs > num_accredited:
    recommendations.append(
        "🏅 **Scale accreditation coverage**: Some programs remain unaccredited. "
        "Target these for phased accreditation."
    )

# Modality gap
if len(modalities) == 1:
    recommendations.append(
        "🎓 **Introduce additional training modalities**: "
        "Expand beyond a single modality (e.g., add Intermediate or Advanced levels)."
    )

elif len(modalities) == 2:
    recommendations.append(
        "🎓 **Complete modality ladder**: "
        "Introduce the missing training tier to ensure workforce progression."
    )

# Program maturity
if years_active < 5:
    recommendations.append(
        "🏛 **Strengthen program maturity**: "
        "Programs are relatively new. Focus on governance structures, faculty development, "
        "and curriculum standardization."
    )

# Network integration
if network_score == 0:
    recommendations.append(
        "🌐 **Strengthen regional integration**: "
        "Country programs are not currently linked to regional or global FETP networks "
        "(e.g., TEPHINET)."
    )

# High readiness refinement
if readiness_score >= 75:
    recommendations.append(
        "🚀 **Advance to regional leadership**: "
        "Position the country as a regional training hub and mentorship center."
    )

# --------------------------------------------------
# DISPLAY RECOMMENDATIONS
# --------------------------------------------------
if recommendations:
    for rec in recommendations:
        st.markdown(f"- {rec}")
else:
    st.success(
        "This country demonstrates strong readiness across all assessed dimensions. "
        "Focus on sustainability, innovation, and regional leadership."
    )

# ==================================================
# AUTO-GENERATED DONOR INVESTMENT PRIORITIES
# ==================================================
st.markdown("## 💰 Donor Investment Priorities")

investment_priorities = []

# Accreditation investment
if num_accredited == 0:
    investment_priorities.append(
        "**Accreditation systems strengthening** — Support accreditation fees, "
        "technical assistance, and quality assurance systems."
    )

elif num_accredited < num_programs:
    investment_priorities.append(
        "**Accreditation scale-up** — Fund phased accreditation of remaining programs."
    )

# Workforce pipeline
if len(modalities) < 3:
    investment_priorities.append(
        "**Workforce pipeline expansion** — Invest in Intermediate and Advanced training "
        "modalities to strengthen career progression."
    )

# Institutional maturity
if years_active < 5:
    investment_priorities.append(
        "**Institutional capacity building** — Support faculty development, "
        "program governance, and curriculum standardization."
    )

# Network & global integration
if network_score == 0:
    investment_priorities.append(
        "**Regional & global integration** — Enable participation in networks "
        "such as TEPHINET and GFEP initiatives."
    )

# High readiness countries
if readiness_score >= 75:
    investment_priorities.append(
        "**Regional leadership & south–south cooperation** — Fund the country "
        "to serve as a regional training hub and mentorship center."
    )

# --------------------------------------------------
# DISPLAY
# --------------------------------------------------
if investment_priorities:
    for item in investment_priorities:
        st.markdown(f"- {item}")
else:
    st.success(
        "This country is well-positioned for innovation-focused investments, "
        "including digital epidemiology, research translation, and regional leadership."
    )

    # ==================================================
    # COUNTRY-SPECIFIC GOVERNANCE METRICS
    # ==================================================

    # Host institutions
    host_institutions = country_programs["host_institution"].dropna().unique()

    # Accreditation metrics
    total_programs = len(country_programs)
    accredited_programs = (country_programs["accredited"] == "Yes").sum()

    # Modalities present
    modalities_present = sorted(country_programs["modality"].dropna().unique())

    # Network participation
    network_membership = country_programs["network"].dropna().unique()
    network_score = len(network_membership)

    # Institutional maturity proxy
    years_active = 2025 - country_programs["established"].min() if total_programs > 0 else 0

# ==================================================
# GOVERNANCE & ACCREDITATION PATHWAY (COUNTRY-AWARE)
# ==================================================
st.markdown("## 🏛 Governance & Accreditation Pathway")

# --------------------------------------------------
# NATIONAL GOVERNANCE
# --------------------------------------------------
with st.expander("📜 National Governance Structure"):
    st.markdown(f"""
    **Country:** {selected_country}

    **Lead Institutions:**
    - Ministry of Health  
    {"".join([f"- {inst}\n" for inst in host_institutions])}

    **Governance Status:**
    - Total programs: {total_programs}
    - Years active (approx.): {years_active}
    """)

# --------------------------------------------------
# TRAINING IMPLEMENTATION
# --------------------------------------------------
with st.expander("🎓 Training Program Implementation"):
    st.markdown(f"""
    **Training modalities currently implemented:**
    {", ".join(modalities_present) if modalities_present else "No formal modalities recorded"}

    **Coverage Assessment:**
    {"Full pipeline coverage" if len(modalities_present) >= 3 else "Partial training pipeline — expansion recommended"}
    """)

# --------------------------------------------------
# ACCREDITATION STATUS
# --------------------------------------------------
with st.expander("🏅 Accreditation & Quality Assurance"):
    st.markdown(f"""
    **Accreditation status:**
    - Accredited programs: {accredited_programs} / {total_programs}

    **Quality maturity:**
    {"Strong quality assurance systems in place" if accredited_programs >= 2 else
    "Accreditation strengthening required"}

    **Recommended next steps:**
    {"Maintain accreditation and mentor regional programs" if accredited_programs >= 2 else
    "Initiate accreditation readiness assessments"}
    """)

# --------------------------------------------------
# REGIONAL & GLOBAL INTEGRATION
# --------------------------------------------------
with st.expander("🌍 Regional & Global Integration"):
    st.markdown(f"""
    **Networks represented:**
    {", ".join(network_membership) if network_score > 0 else "No formal regional network affiliation"}

    **Integration level:**
    {"Well-integrated" if network_score >= 1 else "Limited integration — partnership support recommended"}
    """)

# --------------------------------------------------
# DONOR & PARTNER ENTRY POINTS
# --------------------------------------------------
with st.expander("💰 Donor & Partner Entry Points"):
    st.markdown("""
    **Priority investment levers derived from country metrics:**
    """)

    if accredited_programs == 0:
        st.markdown("- Accreditation readiness and external review support")
    if len(modalities_present) < 3:
        st.markdown("- Expansion of intermediate and advanced training modalities")
    if years_active < 5:
        st.markdown("- Institutional strengthening and faculty development")
    if network_score == 0:
        st.markdown("- Regional and global partnership integration")
