import streamlit as st
import pandas as pd  # <---- DÉJÀ PRÉSENT, vérifiez
from datetime import datetime
from utils import save_signalement

st.markdown("## 📝 Nouveau signalement de coupure")

with st.form("signalement_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        ville = st.text_input("Ville / Quartier *")
        zone = st.selectbox("Zone géographique", [
            "Centre", "Littoral", "Ouest", "Nord", "Extrême-Nord",
            "Sud", "Sud-Ouest", "Est", "Nord-Ouest", "Adamaoua"
        ])
        type_zone = st.selectbox("Type de zone", ["Urbaine", "Péri-urbaine", "Rurale"])
        duree_heures = st.slider("Durée de la coupure (heures)", 0.5, 48.0, 4.0, 0.5)
    
    with col2:
        cause = st.selectbox("Cause probable", [
            "Pluie/orage", "Vent violent", "Surcharge réseau",
            "Travaux programmés", "Accident", "Vol/câble volé", "Arbre tombé", "Inconnue"
        ])
        frequence = st.selectbox("Fréquence", [
            "Première fois", "Rare (1-2x/mois)", "Occasionnelle (1x/semaine)",
            "Fréquente (2-3x/semaine)", "Quotidienne"
        ])
        impact = st.select_slider("Personnes touchées", 
            options=["Moins de 50", "50-200", "200-500", "500-2000", "Plus de 2000"])
        commentaire = st.text_area("Observations")
    
    submitted = st.form_submit_button("✅ Enregistrer", use_container_width=True)
    
    if submitted and ville:
        impact_map = {"Moins de 50": 25, "50-200": 125, "200-500": 350,
                      "500-2000": 1250, "Plus de 2000": 3000}
        frequence_map = {"Première fois": 0.1, "Rare (1-2x/mois)": 1.5,
                         "Occasionnelle (1x/semaine)": 4, "Fréquente (2-3x/semaine)": 10,
                         "Quotidienne": 30}
        
        new_row = pd.DataFrame([{
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "ville": ville, "zone": zone, "type_zone": type_zone,
            "duree_heures": duree_heures, "cause": cause, "frequence": frequence,
            "impact": impact, "commentaire": commentaire,
            "impact_numerique": impact_map[impact],
            "frequence_numerique": frequence_map[frequence]
        }])
        
        save_signalement(new_row)
        st.success(f"✅ Signalement enregistré !")
        st.balloons()
    elif submitted:
        st.error("Veuillez renseigner la ville")