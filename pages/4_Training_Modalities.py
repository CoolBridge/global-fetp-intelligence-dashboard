import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# Page config
# --------------------------------------------------
st.set_page_config(
    page_title="Training Modalities",
    layout="wide"
)

st.title("Training Modalities & System Readiness")

st.markdown(
    """
    This view compares **Field Epidemiology Training modalities**
    using duration and field intensity to assess **system readiness**
    and credentialing suitability.
    """
)

# --------------------------------------------------
# Load data
# --------------------------------------------------
modalities = pd.read_csv("data/modalities.csv")
programs = pd.read_csv("data/programs.csv")

modalities.columns = modalities.columns.str.strip()
programs.columns = programs.columns.str.strip()

# --------------------------------------------------
# Validate schema (STRICT)
# --------------------------------------------------
required_modality_cols = {
    "name",
    "duration_months",
    "field_based_percent",
    "description"
}

missing = required_modality_cols - set(modalities.columns)

if missing:
    st.error(f"modalities.csv schema mismatch. Missing columns: {missing}")
    st.stop()

# --------------------------------------------------
# SECTION 1 — Readiness Heatmap (Correct & Honest)
# --------------------------------------------------
st.subheader("System Readiness Overview")

st.caption(
    """
    Readiness is derived from **training duration** and **field-based intensity**.
    Higher values indicate greater suitability for outbreak leadership and
    professional credentialing.
    """
)

# Normalize metrics for fair comparison
heatmap_df = modalities.copy()

heatmap_df["Duration Score"] = (
    heatmap_df["duration_months"] /
    heatmap_df["duration_months"].max()
) * 100

heatmap_df["Field Intensity Score"] = heatmap_df["field_based_percent"]

heatmap_long = heatmap_df.melt(
    id_vars=["name"],
    value_vars=["Duration Score", "Field Intensity Score"],
    var_name="Readiness Dimension",
    value_name="Score"
)

fig = px.density_heatmap(
    heatmap_long,
    x="Readiness Dimension",
    y="name",
    z="Score",
    color_continuous_scale=["red", "yellow", "green"],
    labels={
        "name": "Training Modality",
        "Score": "Readiness Score"
    }
)

fig.update_layout(height=420)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# SECTION 2 — Programs by Modality (CORRECT LINKAGE)
# --------------------------------------------------
st.subheader("Programs Implementing Each Modality")

selected_modality = st.selectbox(
    "Select Training Modality",
    sorted(modalities["name"].unique())
)

filtered_programs = programs[
    programs["modality"].str.upper() == selected_modality.upper()
]

if filtered_programs.empty:
    st.warning("No programs mapped to this modality.")
else:
    st.dataframe(
        filtered_programs[
            [
                "program_name",
                "country",
                "discipline",
                "network",
                "established",
                "accredited"
            ]
        ].sort_values("established"),
        use_container_width=True,
        hide_index=True
    )

# --------------------------------------------------
# SECTION 3 — Interpretation
# --------------------------------------------------
st.markdown("### Interpretation for Decision-Makers")

st.markdown(
    """
    **Short-Duration Modalities**
    - Rapid surveillance coverage
    - Entry-level workforce development
    - Limited leadership depth

    **Advanced & FELTP Modalities**
    - Backbone of outbreak leadership
    - Appropriate for professional credentialing
    - Higher field immersion improves readiness

    **Credentialing Insight**
    - Duration + field exposure are necessary (but not sufficient)
    - Governance and assessment mechanisms complete readiness
    """
)
