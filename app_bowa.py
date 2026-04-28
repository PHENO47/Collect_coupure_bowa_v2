import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from datetime import datetime
import os
from sklearn.linear_model import LinearRegression
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# ==================== CONFIGURATION ====================
st.set_page_config(
    page_title="BOWA · Coupures Électriques",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CSS GLOBAL ====================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ---- BASE ---- */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Fond principal */
.stApp {
    background: #0A0E1A;
    color: #E8EAF0;
}

/* ---- SIDEBAR ---- */
[data-testid="stSidebar"] {
    background: #0D1220 !important;
    border-right: 1px solid #1E2640;
}

[data-testid="stSidebar"] * {
    color: #C5CAE0 !important;
}

/* Radio buttons dans la sidebar */
[data-testid="stSidebar"] .stRadio label {
    background: transparent;
    padding: 10px 14px;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s;
    display: block;
    font-size: 0.9rem;
}

[data-testid="stSidebar"] .stRadio label:hover {
    background: #1A2040 !important;
    color: #FF6B35 !important;
}

/* Metric */
[data-testid="metric-container"] {
    background: #111827;
    border: 1px solid #1E2A45;
    border-radius: 14px;
    padding: 18px 22px !important;
    transition: border-color 0.2s;
}

[data-testid="metric-container"]:hover {
    border-color: #FF6B35;
}

[data-testid="stMetricLabel"] {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.78rem !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #7A8099 !important;
}

[data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
    color: #FF6B35 !important;
}

/* ---- BOUTONS ---- */
.stButton > button {
    background: linear-gradient(135deg, #FF6B35 0%, #FF4500 100%);
    color: white !important;
    border: none;
    border-radius: 10px;
    font-family: 'Syne', sans-serif;
    font-weight: 600;
    letter-spacing: 0.03em;
    padding: 12px 24px;
    transition: all 0.25s ease;
    box-shadow: 0 4px 20px rgba(255, 107, 53, 0.25);
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(255, 107, 53, 0.4);
}

/* Download button */
.stDownloadButton > button {
    background: #1A2040;
    color: #E8EAF0 !important;
    border: 1px solid #2A3560;
    border-radius: 10px;
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
    transition: all 0.2s;
}

.stDownloadButton > button:hover {
    background: #222B50;
    border-color: #FF6B35;
}

/* ---- INPUTS ---- */
.stTextInput input, .stTextArea textarea, .stSelectbox > div > div {
    background: #111827 !important;
    border: 1px solid #1E2A45 !important;
    border-radius: 10px !important;
    color: #E8EAF0 !important;
    font-family: 'DM Sans', sans-serif !important;
}

.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #FF6B35 !important;
    box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.15) !important;
}

/* ---- FORM ---- */
[data-testid="stForm"] {
    background: #111827;
    border: 1px solid #1E2A45;
    border-radius: 16px;
    padding: 28px;
}

/* ---- TABS ---- */
.stTabs [data-baseweb="tab-list"] {
    background: #111827;
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
    border: 1px solid #1E2A45;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 9px;
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
    color: #7A8099;
    transition: all 0.2s;
}

.stTabs [aria-selected="true"] {
    background: #FF6B35 !important;
    color: white !important;
}

/* ---- DATAFRAME ---- */
[data-testid="stDataFrame"] {
    border: 1px solid #1E2A45;
    border-radius: 12px;
    overflow: hidden;
}

/* ---- INFO BOX ---- */
.stAlert {
    border-radius: 12px;
    border: none;
    background: #111827;
}

/* Separateurs */
hr {
    border-color: #1E2A45 !important;
    margin: 24px 0 !important;
}

/* Slider */
.stSlider [data-baseweb="slider"] {
    accent-color: #FF6B35;
}

/* Caption */
.stCaption {
    color: #7A8099 !important;
    font-style: italic;
}

/* ---- CUSTOM CARDS ---- */
.bowa-card {
    background: #111827;
    border: 1px solid #1E2A45;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 16px;
    transition: border-color 0.2s, box-shadow 0.2s;
}

.bowa-card:hover {
    border-color: #FF6B35;
    box-shadow: 0 0 30px rgba(255,107,53,0.1);
}

.bowa-section-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: #E8EAF0;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 16px;
}

.bowa-badge {
    display: inline-block;
    background: rgba(255,107,53,0.15);
    color: #FF6B35;
    border: 1px solid rgba(255,107,53,0.3);
    border-radius: 6px;
    padding: 2px 10px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.06em;
}
</style>
""", unsafe_allow_html=True)

# ==================== MATPLOTLIB THEME ====================
plt.rcParams.update({
    'figure.facecolor': '#111827',
    'axes.facecolor': '#111827',
    'axes.edgecolor': '#1E2A45',
    'axes.labelcolor': '#C5CAE0',
    'xtick.color': '#7A8099',
    'ytick.color': '#7A8099',
    'text.color': '#E8EAF0',
    'grid.color': '#1E2A45',
    'grid.linewidth': 0.6,
    'axes.grid': True,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'font.family': 'DejaVu Sans',
    'axes.titlesize': 13,
    'axes.titleweight': 'bold',
    'axes.labelsize': 11,
})

ORANGE = '#FF6B35'
BLUE = '#3D7FFF'
PALETTE = ['#FF6B35', '#3D7FFF', '#FFB347', '#5EE7B5', '#C084FC']

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("""
    <div style='padding: 20px 0 10px;'>
        <div style='display:flex; align-items:center; gap:10px; margin-bottom:4px;'>
            <span style='font-size:1.6rem;'>⚡</span>
            <span style='font-family: Syne, sans-serif; font-size:1.5rem; font-weight:800; color:#FF6B35; letter-spacing:0.05em;'>BOWA</span>
        </div>
        <span style='font-size:0.72rem; color:#7A8099; text-transform:uppercase; letter-spacing:0.12em;'>Collecte Coupure · Dashboard</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='margin:12px 0 20px;'>", unsafe_allow_html=True)

    st.markdown("<p style='font-size:0.7rem; text-transform:uppercase; letter-spacing:0.14em; color:#7A8099; margin-bottom:8px;'>Navigation</p>", unsafe_allow_html=True)

    menu = st.radio(
        "",
        ["📝 Nouveau signalement", "📋 Données brutes", "📊 Tableau de bord", "📈 Analyses", "⚙️ À propos"],
        label_visibility="collapsed"
    )

    st.markdown("<hr style='margin:20px 0;'>", unsafe_allow_html=True)

    fichier_data = "data/coupures.csv"
    if os.path.exists(fichier_data):
        df_temp = pd.read_csv(fichier_data)
        total = len(df_temp)
        st.markdown(f"""
        <div style='background:#1A2040; border:1px solid #2A3560; border-radius:12px; padding:16px;'>
            <p style='font-size:0.7rem; text-transform:uppercase; letter-spacing:0.12em; color:#7A8099; margin:0 0 8px;'>Signalements totaux</p>
            <p style='font-family:Syne,sans-serif; font-size:2rem; font-weight:800; color:#FF6B35; margin:0;'>{total}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:auto; padding-top:30px;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background:#0D1220; border:1px solid #1E2640; border-radius:10px; padding:12px;'>
        <p style='font-size:0.8rem; font-weight:600; color:#E8EAF0; margin:0;'>👤 Gov BOWA</p>
        <p style='font-size:0.7rem; color:#7A8099; margin:2px 0 0;'>Supervision · Admin</p>
    </div>
    """, unsafe_allow_html=True)

# ==================== EN-TÊTE PRINCIPAL ====================
st.markdown(f"""
<div style='padding: 8px 0 24px;'>
    <div style='display:flex; align-items:center; gap:14px; margin-bottom:8px;'>
        <h1 style='font-family:Syne,sans-serif; font-size:2rem; font-weight:800; color:#E8EAF0; margin:0; letter-spacing:-0.01em;'>
            {menu.split(" ", 1)[1] if " " in menu else menu}
        </h1>
        <span class='bowa-badge'>BOWA v1.0</span>
    </div>
    <p style='color:#7A8099; margin:0; font-size:0.88rem;'>Système de collecte et analyse des coupures d'électricité au Cameroun</p>
</div>
""", unsafe_allow_html=True)

# ==================== TABLEAU DE BORD ====================
if menu == "📊 Tableau de bord":
    fichier_data = "data/coupures.csv"

    if os.path.exists(fichier_data):
        df = pd.read_csv(fichier_data)
        df["duree_heures"] = pd.to_numeric(df["duree_heures"], errors="coerce")
        df["impact_numerique"] = pd.to_numeric(df["impact_numerique"], errors="coerce")
        df_clean = df.dropna(subset=["duree_heures"])

        # KPI Cards
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📊 Total incidents", len(df_clean))
        with col2:
            st.metric("⏱️ Durée moyenne", f"{df_clean['duree_heures'].mean():.1f} h")
        with col3:
            st.metric("⚠️ Cause principale", df_clean['cause'].mode().iloc[0] if len(df_clean) > 0 else "N/A")
        with col4:
            st.metric("📍 Zone la plus touchée", df_clean['zone'].mode().iloc[0] if len(df_clean) > 0 else "N/A")

        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns(2, gap="large")

        with col1:
            st.markdown("<div class='bowa-card'>", unsafe_allow_html=True)
            st.markdown("<p class='bowa-section-title'>📈 Évolution des signalements</p>", unsafe_allow_html=True)
            if 'timestamp' in df_clean.columns:
                df_clean['date'] = pd.to_datetime(df_clean['timestamp']).dt.date
            signalements_par_jour = df_clean.groupby(df_clean['date']).size() if 'date' in df_clean.columns else pd.Series()
            if len(signalements_par_jour) > 0:
                fig, ax = plt.subplots(figsize=(7, 3.5))
                ax.fill_between(range(len(signalements_par_jour)), signalements_par_jour.values, alpha=0.15, color=ORANGE)
                ax.plot(range(len(signalements_par_jour)), signalements_par_jour.values, marker='o',
                        color=ORANGE, linewidth=2.5, markersize=7, markerfacecolor='white', markeredgewidth=2)
                ax.set_xticks(range(len(signalements_par_jour)))
                ax.set_xticklabels([str(d) for d in signalements_par_jour.index], rotation=30, ha='right', fontsize=8)
                ax.set_ylabel("Signalements", fontsize=10)
                ax.set_title("", fontsize=0)
                fig.tight_layout()
                st.pyplot(fig)
            else:
                st.info("Pas assez de données")
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='bowa-card'>", unsafe_allow_html=True)
            st.markdown("<p class='bowa-section-title'>🎯 Répartition par zone</p>", unsafe_allow_html=True)
            zone_counts = df_clean['zone'].value_counts().head(6)
            if len(zone_counts) > 0:
                fig, ax = plt.subplots(figsize=(7, 3.5))
                bars = ax.barh(zone_counts.index[::-1], zone_counts.values[::-1],
                               color=ORANGE, alpha=0.85, height=0.6, edgecolor='none')
                for bar, val in zip(bars, zone_counts.values[::-1]):
                    ax.text(val + 0.05, bar.get_y() + bar.get_height()/2,
                            str(int(val)), va='center', fontsize=9, color='#C5CAE0')
                ax.set_xlabel("Incidents", fontsize=10)
                ax.set_title("", fontsize=0)
                fig.tight_layout()
                st.pyplot(fig)
            st.markdown("</div>", unsafe_allow_html=True)

        col1, col2 = st.columns(2, gap="large")

        with col1:
            st.markdown("<div class='bowa-card'>", unsafe_allow_html=True)
            st.markdown("<p class='bowa-section-title'>⚡ Causes des coupures</p>", unsafe_allow_html=True)
            cause_counts = df_clean['cause'].value_counts()
            if len(cause_counts) > 0:
                fig, ax = plt.subplots(figsize=(7, 3.8))
                wedges, texts, autotexts = ax.pie(
                    cause_counts.values,
                    labels=cause_counts.index,
                    autopct='%1.0f%%',
                    startangle=90,
                    colors=PALETTE[:len(cause_counts)],
                    wedgeprops={'edgecolor': '#0A0E1A', 'linewidth': 3},
                    textprops={'fontsize': 9, 'color': '#C5CAE0'}
                )
                for autotext in autotexts:
                    autotext.set_fontsize(8)
                    autotext.set_color('white')
                ax.set_facecolor('#111827')
                fig.patch.set_facecolor('#111827')
                fig.tight_layout()
                st.pyplot(fig)
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='bowa-card'>", unsafe_allow_html=True)
            st.markdown("<p class='bowa-section-title'>📊 Types de zones touchées</p>", unsafe_allow_html=True)
            type_counts = df_clean['type_zone'].value_counts()
            if len(type_counts) > 0:
                fig, ax = plt.subplots(figsize=(7, 3.8))
                colors_bar = [ORANGE, BLUE, '#FFB347'][:len(type_counts)]
                bars = ax.bar(type_counts.index, type_counts.values,
                              color=colors_bar, alpha=0.9, width=0.5, edgecolor='none')
                for bar, val in zip(bars, type_counts.values):
                    ax.text(bar.get_x() + bar.get_width()/2, val + 0.05,
                            str(int(val)), ha='center', fontsize=10, color='#C5CAE0', fontweight='bold')
                ax.set_xlabel("Type de zone", fontsize=10)
                ax.set_title("", fontsize=0)
                fig.tight_layout()
                st.pyplot(fig)
            st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class='bowa-card' style='text-align:center; padding:48px;'>
            <span style='font-size:3rem;'>⚡</span>
            <p style='font-family:Syne,sans-serif; font-size:1.1rem; color:#E8EAF0; margin:16px 0 8px;'>Aucune donnée disponible</p>
            <p style='color:#7A8099;'>Commencez par enregistrer un signalement via le menu <strong style='color:#FF6B35;'>Nouveau signalement</strong>.</p>
        </div>
        """, unsafe_allow_html=True)

# ==================== DONNÉES BRUTES ====================
elif menu == "📋 Données brutes":
    fichier_data = "data/coupures.csv"

    if os.path.exists(fichier_data):
        df = pd.read_csv(fichier_data)

        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            st.metric("Lignes", len(df))
        with col2:
            st.metric("Colonnes", len(df.columns))

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("<div class='bowa-card'>", unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True, height=460)
        st.markdown("</div>", unsafe_allow_html=True)

        st.download_button(
            label="📥 Télécharger les données (CSV)",
            data=df.to_csv(index=False),
            file_name=f"bowa_coupures_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:
        st.markdown("""
        <div class='bowa-card' style='text-align:center; padding:48px;'>
            <p style='font-family:Syne,sans-serif; font-size:1.1rem; color:#E8EAF0;'>Aucune donnée disponible</p>
        </div>
        """, unsafe_allow_html=True)

# ==================== NOUVEAU SIGNALEMENT ====================
elif menu == "📝 Nouveau signalement":

    st.markdown("""
    <div class='bowa-card' style='margin-bottom:24px;'>
        <p style='color:#7A8099; margin:0; font-size:0.88rem;'>Renseignez les informations de la coupure observée. Les champs marqués <span style='color:#FF6B35;'>*</span> sont obligatoires.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("signalement_form"):
        col1, col2 = st.columns(2, gap="large")

        with col1:
            st.markdown("<p class='bowa-section-title'>📍 Localisation</p>", unsafe_allow_html=True)
            ville = st.text_input("Ville / Quartier *", placeholder="Ex: Douala, Yaoundé, Garoua...")
            zone = st.selectbox("Zone géographique", [
                "Centre", "Littoral", "Ouest", "Nord", "Extrême-Nord",
                "Sud", "Sud-Ouest", "Est", "Nord-Ouest", "Adamaoua"
            ])
            type_zone = st.selectbox("Type de zone", ["Urbaine", "Péri-urbaine", "Rurale"])
            duree_heures = st.slider("Durée de la coupure (heures)", 0.5, 48.0, 4.0, 0.5)

        with col2:
            st.markdown("<p class='bowa-section-title'>⚡ Incident</p>", unsafe_allow_html=True)
            cause_probable = st.selectbox("Cause probable", [
                "Pluie/orage", "Vent violent", "Surcharge réseau",
                "Travaux programmés", "Accident (véhicule/câble)",
                "Vol/câble volé", "Arbre tombé", "Inconnue"
            ])
            frequence = st.selectbox("Fréquence dans cette zone", [
                "Première fois", "Rare (1-2x/mois)", "Occasionnelle (1x/semaine)",
                "Fréquente (2-3x/semaine)", "Quotidienne"
            ])
            impact = st.select_slider("Personnes touchées estimées",
                options=["Moins de 50", "50-200", "200-500", "500-2000", "Plus de 2000"])
            commentaire = st.text_area("Observations", placeholder="Informations supplémentaires...", height=110)

        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("✅ Enregistrer le signalement", use_container_width=True)

        impact_map = {
            "Moins de 50": 25, "50-200": 125, "200-500": 350,
            "500-2000": 1250, "Plus de 2000": 3000
        }
        frequence_map = {
            "Première fois": 0.1, "Rare (1-2x/mois)": 1.5,
            "Occasionnelle (1x/semaine)": 4, "Fréquente (2-3x/semaine)": 10,
            "Quotidienne": 30
        }

        if submitted:
            if not ville:
                st.error("⚠️ Veuillez renseigner la ville ou le quartier.")
            else:
                fichier_data = "data/coupures.csv"
                os.makedirs("data", exist_ok=True)

                nouvelle_ligne = pd.DataFrame([{
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "ville": ville,
                    "zone": zone,
                    "type_zone": type_zone,
                    "duree_heures": duree_heures,
                    "cause": cause_probable,
                    "frequence": frequence,
                    "impact": impact,
                    "commentaire": commentaire,
                    "impact_numerique": impact_map[impact],
                    "frequence_numerique": frequence_map[frequence]
                }])

                if os.path.exists(fichier_data):
                    df_existant = pd.read_csv(fichier_data)
                    df_combine = pd.concat([df_existant, nouvelle_ligne], ignore_index=True)
                else:
                    df_combine = nouvelle_ligne

                df_combine.to_csv(fichier_data, index=False)
                st.success(f"✅ Signalement enregistré avec succès ! Total cumulé : **{len(df_combine)} incidents**")
                st.balloons()

# ==================== ANALYSES ====================
elif menu == "📈 Analyses":
    fichier_data = "data/coupures.csv"

    if os.path.exists(fichier_data):
        df = pd.read_csv(fichier_data)
        df["duree_heures"] = pd.to_numeric(df["duree_heures"], errors="coerce")
        df["impact_numerique"] = pd.to_numeric(df["impact_numerique"], errors="coerce")
        df["frequence_numerique"] = pd.to_numeric(df["frequence_numerique"], errors="coerce")
        df_clean = df.dropna(subset=["duree_heures", "impact_numerique"])

        tab1, tab2, tab3 = st.tabs(["📐 Régression linéaire", "🔄 Analyse en Composantes", "📊 Statistiques"])

        with tab1:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<div class='bowa-card'>", unsafe_allow_html=True)
            st.markdown("<p class='bowa-section-title'>Relation durée / impact — Régression linéaire</p>", unsafe_allow_html=True)

            X = df_clean['duree_heures'].values.reshape(-1, 1)
            y = df_clean['impact_numerique'].values
            mask = ~(np.isnan(X.flatten()) | np.isnan(y))
            X_clean = X[mask].reshape(-1, 1)
            y_clean = y[mask]

            if len(X_clean) > 1:
                reg = LinearRegression()
                reg.fit(X_clean, y_clean)
                y_pred = reg.predict(X_clean)

                fig, ax = plt.subplots(figsize=(10, 5))
                ax.scatter(X_clean, y_clean, alpha=0.7, label="Données réelles",
                           color=ORANGE, s=80, edgecolors='white', linewidth=0.8, zorder=3)
                ax.plot(sorted(X_clean.flatten()), [reg.predict([[x]])[0] for x in sorted(X_clean.flatten())],
                        color=BLUE, linewidth=2.5, label="Tendance linéaire", zorder=2)
                ax.set_xlabel("Durée de la coupure (heures)")
                ax.set_ylabel("Personnes touchées (estimé)")
                ax.legend(facecolor='#1A2040', edgecolor='#2A3560')
                fig.tight_layout()
                st.pyplot(fig)

                c1, c2, c3 = st.columns(3)
                with c1:
                    st.metric("Coefficient directeur", f"{reg.coef_[0]:.2f}")
                with c2:
                    st.metric("Ordonnée à l'origine", f"{reg.intercept_:.2f}")
                with c3:
                    st.metric("R² (qualité du modèle)", f"{reg.score(X_clean, y_clean):.3f}")

                st.caption(f"📌 Chaque heure supplémentaire de coupure touche environ {reg.coef_[0]:.0f} personnes de plus.")
            st.markdown("</div>", unsafe_allow_html=True)

        with tab2:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<div class='bowa-card'>", unsafe_allow_html=True)
            st.markdown("<p class='bowa-section-title'>Projection multidimensionnelle — ACP</p>", unsafe_allow_html=True)

            features_acp = ['duree_heures', 'impact_numerique']
            if 'frequence_numerique' in df_clean.columns:
                features_acp.append('frequence_numerique')

            df_acp = df_clean[features_acp].dropna()

            if len(df_acp) > 2:
                scaler = StandardScaler()
                df_scaled = scaler.fit_transform(df_acp)
                pca = PCA(n_components=2)
                pca_result = pca.fit_transform(df_scaled)

                fig, ax = plt.subplots(figsize=(10, 5))
                scatter = ax.scatter(
                    pca_result[:, 0], pca_result[:, 1],
                    c=df_acp['duree_heures'],
                    cmap='YlOrRd', alpha=0.85, s=90,
                    edgecolors='#1E2A45', linewidth=0.5
                )
                cbar = plt.colorbar(scatter, ax=ax)
                cbar.set_label("Durée (heures)", color='#C5CAE0')
                cbar.ax.yaxis.set_tick_params(color='#C5CAE0')
                plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='#C5CAE0')
                ax.set_xlabel(f"Composante 1 ({pca.explained_variance_ratio_[0]:.1%})")
                ax.set_ylabel(f"Composante 2 ({pca.explained_variance_ratio_[1]:.1%})")
                fig.tight_layout()
                st.pyplot(fig)

                st.caption(f"📊 Les 2 composantes expliquent {pca.explained_variance_ratio_.sum():.1%} de la variance totale.")
            else:
                st.info("Pas assez de données pour l'ACP (minimum 3 observations).")
            st.markdown("</div>", unsafe_allow_html=True)

        with tab3:
            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2 = st.columns(2, gap="large")

            with col1:
                st.markdown("<div class='bowa-card'>", unsafe_allow_html=True)
                st.markdown("<p class='bowa-section-title'>Durée des coupures</p>", unsafe_allow_html=True)
                stats = df_clean['duree_heures']
                stats_df = pd.DataFrame({
                    'Statistique': ['Moyenne', 'Médiane', 'Écart-type', 'Minimum', 'Maximum', 'Q1 (25%)', 'Q3 (75%)'],
                    'Valeur (h)': [
                        f"{stats.mean():.1f}", f"{stats.median():.1f}",
                        f"{stats.std():.1f}", f"{stats.min():.1f}",
                        f"{stats.max():.1f}", f"{stats.quantile(0.25):.1f}",
                        f"{stats.quantile(0.75):.1f}"
                    ]
                })
                st.dataframe(stats_df, use_container_width=True, hide_index=True)
                st.markdown("</div>", unsafe_allow_html=True)

            with col2:
                st.markdown("<div class='bowa-card'>", unsafe_allow_html=True)
                st.markdown("<p class='bowa-section-title'>Top zones les plus touchées</p>", unsafe_allow_html=True)
                top_zones = df_clean['zone'].value_counts().head(5).reset_index()
                top_zones.columns = ['Zone', 'Incidents']
                st.dataframe(top_zones, use_container_width=True, hide_index=True)
                st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class='bowa-card' style='text-align:center; padding:48px;'>
            <p style='font-family:Syne,sans-serif; font-size:1.1rem; color:#E8EAF0;'>Aucune donnée disponible pour les analyses.</p>
        </div>
        """, unsafe_allow_html=True)

# ==================== À PROPOS ====================
elif menu == "⚙️ À propos":
    col1, col2 = st.columns([2, 1], gap="large")

    with col1:
        st.markdown("""
        <div class='bowa-card'>
            <p class='bowa-section-title'>📱 Collecte Coupure BOWA</p>
            <p style='color:#7A8099; line-height:1.7;'>Application de collecte et d'analyse des signalements de coupures d'électricité au Cameroun. Conçue pour faciliter la supervision terrain et la prise de décision basée sur les données.</p>
            <br>
            <p class='bowa-section-title'>🎯 Fonctionnalités</p>
            <ul style='color:#C5CAE0; line-height:2;'>
                <li>Collecte structurée des signalements de coupures</li>
                <li>Tableau de bord interactif avec KPIs temps réel</li>
                <li>Analyses statistiques avancées (régression, ACP)</li>
                <li>Export des données en CSV</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='bowa-card'>
            <p class='bowa-section-title'>📞 Contact</p>
            <p style='color:#C5CAE0; margin:0 0 12px;'>📧 samelphenomene@gmail.com</p>
            <p style='color:#C5CAE0; margin:0 0 24px;'>📞 +237 612 120 000</p>
            <hr style='border-color:#1E2A45; margin:16px 0;'>
            <p style='font-size:0.75rem; color:#7A8099;'>PHENO47 · Analyse de données</p>
            <span class='bowa-badge'>Version 1.0</span>
        </div>
        """, unsafe_allow_html=True)

# ==================== FOOTER ====================
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center; padding:20px 0; border-top:1px solid #1E2A45;'>
    <p style='font-size:0.75rem; color:#7A8099; margin:0; letter-spacing:0.06em;'>
        © 2026 <span style='color:#FF6B35; font-weight:600;'>BOWA</span> · Collecte Coupure · Analyse des coupures d'électricité au Cameroun
    </p>
</div>
""", unsafe_allow_html=True)
