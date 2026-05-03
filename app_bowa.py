import streamlit as st
from utils import load_data

# Configuration de la page (une seule fois)
st.set_page_config(
    page_title="BOWA · Coupures Électriques",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar (commune à toutes les pages)
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
    page = st.radio("", [
        "📝 Nouveau signalement",
        "📋 Données brutes", 
        "📊 Tableau de bord",
        "📈 Analyses",
        "⚙️ À propos"
    ], label_visibility="collapsed")
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Stats rapides dans la sidebar
    df = load_data()
    if df is not None:
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

# Affichage du contenu selon la page sélectionnée
if page == "📝 Nouveau signalement":
    # Importer et exécuter la page
    import pages.page1_nouveau_signalement as page1
    page1.show()
    
elif page == "📋 Données brutes":
    import pages.page2_donnees_brutes as page2
    page2.show()
    
elif page == "📊 Tableau de bord":
    import pages.page3_tableau_de_bord as page3
    page3.show()
    
elif page == "📈 Analyses":
    import pages.page4_analyses as page4
    page4.show()
    
elif page == "⚙️ À propos":
    import pages.page5_a_propos as page5
    page5.show()
