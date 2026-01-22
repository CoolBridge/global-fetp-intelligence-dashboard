import streamlit as st
import pandas as pd

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(layout="wide")

st.header("🎓 Credentialing Readiness Explorer")

st.markdown(
    """
This module evaluates **program-level readiness** for participation in a future
**Global Professional Credentialing Mechanism for Field Epidemiologists**.

The logic reflects **objective eligibility thresholds** aligned with TWG discussions
and can be refined during pilots.
"""
)

# ==================================================
# LOAD DATA
# ==================================================
programs = pd.read_csv("data/programs.csv")
modalities = pd.read_csv("data/modalities.csv")
institutions = pd.read_csv("data/institutions.csv")

# ==================================================
# MODALITY LOOKUP (SCHEMA SAFE)
# ==================================================
modality_lookup = {
    row["modality_id"]: {
        "name": row["name"],
        "duration_months": row["duration_months"],
        "field_based_percent": row["field_based_percent"]
    }
    for _, row in modalities.iterrows()
}

# ==================================================
# ELIGIBILITY EVALUATION LOGIC
# ==================================================
def evaluate_program_eligibility(row):
    reasons = []
    actions = []

    modality = row["modality"]
    accredited = row["accredited"]
    host = row["host_institution"]

    # Rule 1 — Modality existence
    if modality not in modality_lookup:
        return "Not Eligible", ["Unrecognized training modality"], ["Standardize modality classification"]

    modality_meta = modality_lookup[modality]

    # Rule 2 — Training depth
    if modality_meta["duration_months"] < 18:
        reasons.append("Training duration below professional credentialing threshold")
        actions.append("Upgrade to advanced-level training")

    # Rule 3 — Field exposure
    if modality_meta["field_based_percent"] < 60:
        return "Not Eligible", ["Insufficient field-based training"], ["Increase supervised field deployment"]
    elif modality_meta["field_based_percent"] < 70:
        reasons.append("Field exposure below optimal threshold")
        actions.append("Strengthen field mentorship structure")

    # Rule 4 — Accreditation
    if accredited != "Yes":
        reasons.append("Program not formally accredited")
        actions.append("Pursue FETP/FELTP accreditation")

    # Rule 5 — Host institution
    if pd.isna(host) or host.strip() == "":
        return "Not Eligible", ["No accountable host institution"], ["Establish institutional oversight"]

    # Final decision
    if len(reasons) == 0:
        status = "Eligible"
    else:
        status = "Conditionally Eligible"

    return status, reasons, actions

# ==================================================
# APPLY LOGIC
# ==================================================
results = programs.apply(evaluate_program_eligibility, axis=1)

programs["Eligibility Status"] = results.apply(lambda x: x[0])
programs["Eligibility Reasons"] = results.apply(lambda x: "; ".join(x[1]))
programs["Recommended Actions"] = results.apply(lambda x: "; ".join(x[2]))

# ==================================================
# FILTERS
# ==================================================
st.markdown("### 🌍 Filter Programs")

region = st.selectbox(
    "Select WHO Region",
    sorted(programs["who_region"].unique())
)

filtered = programs[programs["who_region"] == region]

# ==================================================
# SUMMARY METRICS
# ==================================================
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Eligible Programs", (filtered["Eligibility Status"] == "Eligible").sum())

with col2:
    st.metric("Conditionally Eligible", (filtered["Eligibility Status"] == "Conditionally Eligible").sum())

with col3:
    st.metric("Not Eligible", (filtered["Eligibility Status"] == "Not Eligible").sum())

# ==================================================
# TABLE VIEW
# ==================================================
st.subheader(f"📋 Credentialing Readiness — {region}")

st.dataframe(
    filtered[
        [
            "program_name",
            "country",
            "modality",
            "accredited",
            "Eligibility Status",
            "Eligibility Reasons",
            "Recommended Actions"
        ]
    ],
    use_container_width=True
)

# ==================================================
# TWG INTERPRETATION
# ==================================================
st.markdown(
    """
### 🧠 TWG Interpretation

**Eligible Programs**
- Can participate immediately in pilot credentialing
- Suitable for early endorsement and benchmarking

**Conditionally Eligible Programs**
- Require targeted system strengthening
- Ideal candidates for phased inclusion

**Not Eligible Programs**
- Structural gaps must be addressed before participation
- Important for long-term workforce planning

This evidence-based classification supports **transparent decision-making**
and aligns with GFEP principles of equity, quality, and feasibility.
"""
)
