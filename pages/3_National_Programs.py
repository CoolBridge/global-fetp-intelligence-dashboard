import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("🌍 National Field Epidemiology Training Programs (Africa)")

st.markdown("""
Click on a country or select from the dropdown to explore:

• FELTP programs  
• Accomplishments  
• Capacity gaps  
• Credentialing recommendations  
""")

# -----------------------------
# Load data
# -----------------------------
countries = pd.read_csv("data/countries.csv")
programs = pd.read_csv("data/programs.csv")

# Africa only
africa = countries[countries["who_region"] == "AFRO"]

# Merge programs with country coordinates
df = programs.merge(
    africa,
    on="country",
    how="inner"
)

# -----------------------------
# Sidebar selector
# -----------------------------
st.sidebar.header("Select Country")

country_list = ["All African Countries"] + sorted(df["country"].unique().tolist())
selected_country = st.sidebar.selectbox("Country", country_list)

# -----------------------------
# Map styling logic
# -----------------------------
df["highlight"] = "Normal"
df["size"] = 8

if selected_country != "All African Countries":
    df.loc[df["country"] == selected_country, "highlight"] = "Selected"
    df.loc[df["country"] == selected_country, "size"] = 18

# -----------------------------
# Africa FELTP Map
# -----------------------------
fig = px.scatter_geo(
    df,
    lat="lat",
    lon="lon",
    hover_name="country",
    hover_data={
        "program_name": True,
        "network": True,
        "modality": True,
        "accredited": True,
    },
    color="highlight",
    size="size",
    size_max=25,
    projection="natural earth",
    scope="africa",
    height=600
)

fig.update_layout(
    margin=dict(r=0, t=0, l=0, b=0),
    legend_title_text=""
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Country Detail Panel
# -----------------------------
if selected_country != "All African Countries":

    st.subheader(f"🇦🇫 {selected_country} — FELTP Profile")

    country_programs = df[df["country"] == selected_country]

    st.markdown("### 🏫 Programs")
    st.dataframe(
        country_programs[
            [
                "program_name",
                "modality",
                "discipline",
                "established",
                "accredited"
            ]
        ],
        use_container_width=True
    )

    st.markdown("### 🏆 Accomplishments")
    st.markdown("""
    • Sustained outbreak investigation capacity  
    • Contribution to national surveillance systems  
    • Workforce retention in public health agencies  
    """)

    st.markdown("### ⚠ Capacity Gaps")
    st.markdown("""
    • Limited formal credentialing pathways  
    • Inconsistent accreditation standards  
    • Faculty and mentorship shortages  
    """)

    st.markdown("### 🎯 Credentialing Recommendations")
    st.markdown("""
    • Introduce tiered credentialing aligned with FELTP modality  
    • Regional accreditation via AFENET / GFEP  
    • Continuous professional development tracking  
    """)
