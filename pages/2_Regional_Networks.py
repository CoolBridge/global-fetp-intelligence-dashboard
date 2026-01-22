import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("🌐 Regional & Global FETP Networks")
st.markdown(
    """
    Explore global and regional Field Epidemiology Training Program (FETP) networks,
    their headquarters, scope, and supported national programs.
    """
)

# -----------------------------
# Load data
# -----------------------------
networks = pd.read_csv("data/networks.csv")
programs = pd.read_csv("data/programs.csv")

# -----------------------------
# Sidebar filter
# -----------------------------
st.sidebar.header("Filter Networks")

network_options = ["All Networks"] + sorted(networks["name"].unique().tolist())
selected_network = st.sidebar.selectbox("Select Network", network_options)

# -----------------------------
# Filter data
# -----------------------------
map_df = networks.copy()

if selected_network != "All Networks":
    map_df = map_df[map_df["name"] == selected_network]

# -----------------------------
# Map: Network HQs
# -----------------------------
fig = px.scatter_geo(
    map_df,
    lat="latitude",
    lon="longitude",
    hover_name="name",
    hover_data={
        "level": True,
        "established": True,
        "headquarters": True,
        "description": True,
    },
    projection="natural earth",
    height=600
)

fig.update_layout(
    margin=dict(r=0, t=0, l=0, b=0)
)




st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Network details
# -----------------------------
if selected_network != "All Networks":
    st.subheader(f"📍 {selected_network} — Network Overview")

    net = map_df.iloc[0]

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Level:** {net['level']}")
        st.markdown(f"**Established:** {net['established']}")
    with col2:
        st.markdown(f"**Headquarters:** {net['headquarters']}")

    st.markdown("### 🌍 Supported National Programs")

    supported_programs = programs[programs["network"] == selected_network]

    if supported_programs.empty:
        st.info("No linked national programs found.")
    else:
        st.dataframe(
            supported_programs[
                [
                    "program_name",
                    "country",
                    "modality",
                    "discipline",
                    "established",
                    "accredited"
                ]
            ],
            use_container_width=True
        )

    st.markdown("### 📌 Strategic Interpretation")
    st.markdown(
        """
        **Strengths**
        - Regional coordination and technical leadership  
        - Rapid outbreak surge capacity  

        **Gaps**
        - Uneven geographic penetration  
        - Dependence on donor funding  

        **Opportunities**
        - Network-led credential harmonization  
        - Joint accreditation and fellowship pipelines  
        """
    )
