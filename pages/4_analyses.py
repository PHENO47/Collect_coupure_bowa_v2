import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import load_data

st.title("📈 Analyses avancées")
st.markdown("---")

# Charger les données
df = load_data()

if df is not None and not df.empty:
    # Analyse temporelle
    st.subheader("⏰ Analyse temporelle")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Heures de pointe
        df['heure'] = df['heure_debut'].str[:2].astype(int)
        heure_counts = df['heure'].value_counts().sort_index()
        fig_heures = px.bar(
            x=heure_counts.index,
            y=heure_counts.values,
            title="Distribution par heure de début",
            labels={'x': 'Heure', 'y': 'Nombre de coupures'}
        )
        st.plotly_chart(fig_heures, use_container_width=True)
    
    with col2:
        # Jours de semaine
        df['jour_semaine'] = pd.to_datetime(df['date_signalement']).dt.day_name()
        jour_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        jour_counts = df['jour_semaine'].value_counts().reindex(jour_order)
        fig_jours = px.bar(
            x=jour_counts.index,
            y=jour_counts.values,
            title="Coupures par jour de semaine",
            labels={'x': 'Jour', 'y': 'Nombre'}
        )
        st.plotly_chart(fig_jours, use_container_width=True)
    
    st.markdown("---")
    
    # Analyse géographique
    st.subheader("📍 Analyse géographique")
    
    # Heatmap des quartiers
    quartier_impact = df.groupby(['zone', 'quartier']).size().reset_index(name='nombre')
    fig_heat = px.density_heatmap(
        quartier_impact,
        x='zone',
        y='quartier',
        z='nombre',
        title="Intensité des coupures par zone/quartier"
    )
    st.plotly_chart(fig_heat, use_container_width=True)
    
    # Top quartiers touchés
    top_quartiers = df['quartier'].value_counts().head(10)
    fig_top = px.bar(
        x=top_quartiers.values,
        y=top_quartiers.index,
        orientation='h',
        title="Top 10 des quartiers les plus touchés"
    )
    st.plotly_chart(fig_top, use_container_width=True)
    
    st.markdown("---")
    
    # Corrélations
    st.subheader("🔍 Corrélations")
    
    # Tableau croisé impact vs type
    impact_type = pd.crosstab(df['impact'], df['type_coupure'])
    fig_cross = px.imshow(
        impact_type,
        text_auto=True,
        aspect="auto",
        title="Corrélation entre type et impact des coupures"
    )
    st.plotly_chart(fig_cross, use_container_width=True)
    
    # Durée moyenne par type
    duree_type = df.groupby('type_coupure')['duree'].mean().reset_index()
    fig_duree_type = px.bar(
        duree_type,
        x='type_coupure',
        y='duree',
        title="Durée moyenne par type de coupure"
    )
    st.plotly_chart(fig_duree_type, use_container_width=True)
    
else:
    st.warning("⚠️ Données insuffisantes pour les analyses")
    st.info("Ajoutez plus de signalements pour voir les analyses")
