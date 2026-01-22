import streamlit as st
import pandas as pd
import plotly.express as px

if not st.session_state.get("entered", False):
    st.warning("Please return to the home page and click Proceed.")
    st.stop()


st.title("🌐 Global Overview")

# Load data
metrics = pd.read_csv("data/global_metrics.csv")
networks = pd.read_csv("data/networks.csv")
st.write("NETWORKS DATA PREVIEW")
st.write(networks.head())

#st.write("NETWORKS COLUMNS")
#st.write(networks.columns)

# ---- Metrics ----
st.subheader("📊 Global FETP Metrics")

cols = st.columns(3)
for i, row in metrics.iterrows():
    cols[i % 3].metric(row["metric"], row["value"])

# ---- Network Map ----
st.subheader("🗺️ Global & Regional Network Headquarters")

fig = px.scatter_geo(
    networks,
    lat="latitude",
    lon="longitude",
    hover_name="name",
    hover_data=["level", "established", "headquarters"],
    color="level",
    projection="natural earth",
    height=600
)

fig.update_layout(
    margin={"r":0,"t":0,"l":0,"b":0}
)

st.plotly_chart(fig, use_container_width=True)



