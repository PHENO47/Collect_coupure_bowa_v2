import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd  # <---- AJOUT
from utils import load_data

st.markdown("## 📊 Tableau de bord")

df = load_data()

if df is not None and len(df) > 0:
    df_clean = df.dropna(subset=["duree_heures"])
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📊 Total incidents", len(df_clean))
    with col2:
        st.metric("⏱️ Durée moyenne", f"{df_clean['duree_heures'].mean():.1f} h")
    with col3:
        cause = df_clean['cause'].mode().iloc[0] if 'cause' in df_clean else "N/A"
        st.metric("⚠️ Cause principale", cause)
    with col4:
        zone = df_clean['zone'].mode().iloc[0] if 'zone' in df_clean else "N/A"
        st.metric("📍 Zone la plus touchée", zone)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 Évolution")
        if 'timestamp' in df_clean.columns:
            df_clean['date'] = pd.to_datetime(df_clean['timestamp']).dt.date
            evol = df_clean.groupby('date').size()
            if len(evol) > 0:
                fig, ax = plt.subplots()
                ax.plot(range(len(evol)), evol.values, marker='o', color='#FF6B35')
                ax.set_xticks(range(len(evol)))
                ax.set_xticklabels([str(d) for d in evol.index], rotation=45, ha='right')
                st.pyplot(fig)
    
    with col2:
        st.markdown("#### 🎯 Répartition par zone")
        if 'zone' in df_clean.columns:
            zones = df_clean['zone'].value_counts().head(5)
            if len(zones) > 0:
                fig, ax = plt.subplots()
                ax.barh(zones.index, zones.values, color='#FF6B35')
                st.pyplot(fig)
else:
    st.info("Aucune donnée disponible")