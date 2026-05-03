import streamlit as st
from datetime import datetime
from utils import load_data

st.markdown("## 📋 Données brutes")

df = load_data()

if df is not None and len(df) > 0:
    st.dataframe(df, use_container_width=True)
    
    st.download_button(
        label="📥 Télécharger CSV",
        data=df.to_csv(index=False),
        file_name=f"bowa_coupures_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )
else:
    st.info("Aucune donnée disponible")