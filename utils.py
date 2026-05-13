import streamlit as st
import pandas as pd
import os

@st.cache_data
def load_data():
    """Charge les données du fichier CSV"""
    fichier = "data/coupures.csv"
    if os.path.exists(fichier):
        df = pd.read_csv(fichier)
        df["duree_heures"] = pd.to_numeric(df["duree_heures"], errors="coerce")
        if "impact_numerique" in df.columns:
            df["impact_numerique"] = pd.to_numeric(df["impact_numerique"], errors="coerce")
        if "frequence_numerique" in df.columns:
            df["frequence_numerique"] = pd.to_numeric(df["frequence_numerique"], errors="coerce")
        return df
    return None

def save_signalement(new_row):
    """Sauvegarde un nouveau signalement"""
    os.makedirs("data", exist_ok=True)
    fichier = "data/coupures.csv"
    if os.path.exists(fichier):
        existing = pd.read_csv(fichier)
        new_row = pd.concat([existing, new_row], ignore_index=True)
    new_row.to_csv(fichier, index=False)
    st.cache_data.clear()