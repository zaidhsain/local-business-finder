import streamlit as st
import sys
import os
import pandas as pd

# Ajouter le dossier parent au path pour que config et services soient trouvés
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.settings import APP_NAME, APP_VERSION
from services.database import create_tables
from services.crud import get_all_business
from services.discovery import search_local_business_full

# Initialisation DB (si nécessaire)
create_tables()

# Configuration page Streamlit
st.set_page_config(
    page_title=APP_NAME,
    layout="wide"
)

# -------------------------------
# Initialisation session
# -------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# -------------------------------
# Connexion
# -------------------------------
# Connexion
if not st.session_state.logged_in:
    st.title("🔐 Connexion")
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    
    if st.button("Se connecter"):
        from services.auth import verify_user
        if verify_user(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Bienvenue {username} !")
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect")

# Contenu après connexion
else:
    st.sidebar.success(f"Connecté en tant que {st.session_state.username}")
    if st.sidebar.button("🔓 Déconnexion"):
        st.session_state.logged_in = False
        st.session_state.username = ""

    st.header("🔍 Rechercher et enrichir les business locaux")
    query = st.text_input("Activité")
    city = st.text_input("Ville")
    max_results = st.slider("Nombre de résultats", 1, 25, 5)

    if st.button("🚀 Lancer la recherche complète"):
        if not query or not city:
            st.warning("Veuillez saisir l'activité et la ville !")
        else:
            try:
                businesses = search_local_business_full(query, city, max_results)
                st.success(f"{len(businesses)} business enrichis et ajoutés à la DB !")
                df = pd.DataFrame(businesses)[["name","category","city","email","phone","rating","reviews_count"]]
                st.dataframe(df)
            except Exception as e:
                st.error(f"Erreur : {e}")

    st.header("📊 Tous les leads enregistrés")
    all_businesses = get_all_business()
    if all_businesses:
        df_all = pd.DataFrame(all_businesses)[["name","category","city","email","phone","rating","reviews_count"]]
        st.dataframe(df_all)
    else:
        st.info("Aucun lead trouvé dans la base de données.")
