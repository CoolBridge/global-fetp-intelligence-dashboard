import pandas as pd
import streamlit as st

@st.cache_data(show_spinner="Loading core datasets...")
def load_all_data():
    return {
        "countries": pd.read_csv("data/countries.csv"),
        "programs": pd.read_csv("data/programs.csv"),
        "networks": pd.read_csv("data/networks.csv"),
        "partners": pd.read_csv("data/partners.csv"),
        "institutions": pd.read_csv("data/institutions.csv"),
        "modalities": pd.read_csv("data/modalities.csv"),
        "governance": pd.read_csv("data/governance_models.csv"),
        "metrics": pd.read_csv("data/global_metrics.csv"),
    }



