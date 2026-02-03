import streamlit as st
from services.auth import verify_user, create_user

# Créer admin par défaut si pas existant
create_user("admin", "admin123")

st.title("🔐 Connexion")
username = st.text_input("Nom d'utilisateur")
password = st.text_input("Mot de passe", type="password")

if st.button("Se connecter"):
    if verify_user(username, password):
        st.success(f"Bienvenue {username} !")
        st.session_state['user'] = username
        st.experimental_rerun()
    else:
        st.error("Nom d'utilisateur ou mot de passe incorrect")

# Bouton logout
if st.session_state.get('user'):
    if st.button("Se déconnecter"):
        st.session_state['user'] = None
        st.success("Vous êtes déconnecté")
        st.experimental_rerun()
