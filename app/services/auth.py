import streamlit as st
from services.auth import verify_user, create_user
from services.database import create_tables

# Crée les tables si elles n'existent pas encore
create_tables()

# Crée un compte admin par défaut (une seule fois)
create_user("admin", "admin123")

# --------------- SESSION LOGIN -----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# Si l'utilisateur n'est pas connecté
if not st.session_state.logged_in:
    st.title("🔐 Connexion")
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        if verify_user(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Bienvenue {username} !")
            st.experimental_rerun()
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect")
else:
    # ----------------- APP CONTENU -----------------
    st.sidebar.success(f"Connecté en tant que {st.session_state.username}")
    st.title("🗺️ Local Business Finder AI")
    st.caption("Version 1.0")

    # Bouton pour déconnexion
    if st.sidebar.button("🔓 Déconnexion"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.experimental_rerun()

    # Ici tu mets ton code de recherche / dashboard
    st.header("🔍 Recherche Local Business")
    from services.discovery import search_local_business_full
    import pandas as pd

    query = st.text_input("Activité (ex: Salon de coiffure)")
    city = st.text_input("Ville (ex: Rabat)")
    max_results = st.slider("Nombre de résultats", 1, 25, 5)

    if st.button("Lancer la recherche"):
        businesses = search_local_business_full(query, city, max_results)
        st.success(f"{len(businesses)} business trouvés et ajoutés à la DB !")
        st.write(pd.DataFrame(businesses))
