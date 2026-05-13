import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd  # <---- AJOUT OBLIGATOIRE
from sklearn.linear_model import LinearRegression
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from utils import load_data

st.markdown("## 📈 Analyses")

df = load_data()

if df is not None and len(df) >= 2:
    df["duree_heures"] = pd.to_numeric(df["duree_heures"], errors="coerce")
    df["impact_numerique"] = pd.to_numeric(df["impact_numerique"], errors="coerce")
    df_clean = df.dropna(subset=["duree_heures", "impact_numerique"])
    
    if len(df_clean) >= 2:
        tab1, tab2 = st.tabs(["📐 Régression", "🔄 ACP"])
        
        with tab1:
            X = df_clean['duree_heures'].values.reshape(-1, 1)
            y = df_clean['impact_numerique'].values
            
            reg = LinearRegression()
            reg.fit(X, y)
            
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.scatter(X, y, alpha=0.7, color='#FF6B35', s=60)
            ax.plot(sorted(X.flatten()), reg.predict(sorted(X)), color='#3D7FFF', linewidth=2)
            ax.set_xlabel("Durée (heures)")
            ax.set_ylabel("Personnes touchées")
            st.pyplot(fig)
            
            col1, col2 = st.columns(2)
            col1.metric("Coefficient", f"{reg.coef_[0]:.2f}")
            col2.metric("R²", f"{reg.score(X, y):.3f}")
        
        with tab2:
            if len(df_clean) >= 3:
                features = df_clean[['duree_heures', 'impact_numerique']].dropna()
                scaler = StandardScaler()
                scaled = scaler.fit_transform(features)
                pca = PCA(n_components=2)
                pca_result = pca.fit_transform(scaled)
                
                fig, ax = plt.subplots(figsize=(10, 5))
                scatter = ax.scatter(pca_result[:, 0], pca_result[:, 1], 
                                    c=features['duree_heures'], cmap='YlOrRd', s=80)
                plt.colorbar(scatter, label="Durée (h)")
                ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.1%})")
                ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.1%})")
                st.pyplot(fig)
            else:
                st.info("Ajoutez au moins 3 signalements pour l'ACP")
    else:
        st.warning("Ajoutez au moins 2 signalements pour la régression")
else:
    st.info("Aucune donnée disponible pour les analyses")