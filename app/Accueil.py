import streamlit as st
import sys
import os
import pandas as pd

# Ajouter le dossier parent au path pour que config et services soient trouvés
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.settings import APP_NAME, APP_VERSION
from services.database import create_table
from services.crud import get_all_business
from services.discovery import search_local_business_full

# Initialisation DB (si nécessaire)
create_table()

# Configuration page Streamlit
st.set_page_config(
    page_title=APP_NAME,
    layout="wide"
)

st.title("🗺️ Local Business Finder AI")
st.caption(f"Version {APP_VERSION}")

# --------------------------
# Formulaire de recherche
# --------------------------
st.header("🔍 Rechercher et enrichir les business locaux")

query = st.text_input("Activité (ex: Salon de coiffure, Agence marketing)")
city = st.text_input("Ville (ex: Rabat, Paris)")
max_results = st.slider("Nombre de résultats", 1, 25, 5)

if st.button("🚀 Lancer la recherche complète"):
    if not query or not city:
        st.warning("Veuillez saisir l'activité et la ville !")
    else:
        with st.spinner("Recherche et enrichissement en cours... ⏳"):
            # Appel pipeline complet
            businesses = search_local_business_full(query, city, max_results)

        st.success(f"{len(businesses)} business enrichis et ajoutés à la DB !")

        # Affichage DataFrame
        import pandas as pd
        df = pd.DataFrame(businesses)
        st.dataframe(df)

        # Export CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Télécharger CSV",
            data=csv,
            file_name=f"leads_{query}_{city}.csv",
            mime="text/csv"
        )

# --------------------------
# Affichage de tous les leads existants dans la DB
# --------------------------
st.header("📊 Tous les leads enregistrés")

all_businesses = get_all_business()
if all_businesses:
    df_all = pd.DataFrame(all_businesses)
    st.dataframe(df_all)
else:
    st.info("Aucun lead trouvé dans la base de données.")
