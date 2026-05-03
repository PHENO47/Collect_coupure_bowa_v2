import streamlit as st
from utils import load_data

# Configuration de la page
st.set_page_config(
    page_title="BOWA · Coupures Électriques",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar commune
with st.sidebar:
    st.markdown("""
    <div style='padding: 20px 0 10px;'>
        <div style='display:flex; align-items:center; gap:10px;'>
            <span style='font-size:1.6rem;'>⚡</span>
            <span style='font-family: Syne; font-size:1.5rem; font-weight:800; color:#FF6B35;'>BOWA</span>
        </div>
        <span style='font-size:0.7rem; color:#7A8099;'>Collecte Coupure · Dashboard</span>
    </div>
    <hr>
    """, unsafe_allow_html=True)
    
    # Menu de navigation
    page = st.radio(
        "Navigation",
        ["📝 Nouveau signalement", "📋 Données brutes", "📊 Tableau de bord", "📈 Analyses", "⚙️ À propos"],
        label_visibility="collapsed"
    )
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Stats dans sidebar
    df = load_data()
    if df is not None and not df.empty:
        st.markdown(f"""
        <div style='background:#1A2040; border-radius:12px; padding:16px;'>
            <p style='font-size:0.7rem; color:#7A8099;'>Signalements totaux</p>
            <p style='font-family:Syne; font-size:2rem; font-weight:800; color:#FF6B35;'>{len(df)}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='margin-top:30px; background:#0D1220; border-radius:10px; padding:12px;'>
        <p style='font-weight:600;'>👤 Gov BOWA</p>
        <p style='font-size:0.7rem; color:#7A8099;'>Supervision · Admin</p>
    </div>
    """, unsafe_allow_html=True)

# Navigation sans exec()
if page == "📝 Nouveau signalement":
    exec(open("pages/1_nouveau_signalement.py").read())
elif page == "📋 Données brutes":
    exec(open("pages/2_donnees_brutes.py").read())
elif page == "📊 Tableau de bord":
    exec(open("pages/3_tableau_de_bord.py").read())
elif page == "📈 Analyses":
    exec(open("pages/4_analyses.py").read())
elif page == "⚙️ À propos":
    exec(open("pages/5_a_propos.py").read())
