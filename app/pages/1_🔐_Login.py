import streamlit as st
from services.auth import verify_user, create_user

# Créer admin par défaut si pas existant
create_user("admin", "admin123")

if not st.session_state.get("user"):
    st.title("🔐 Connexion")
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    
    if st.button("Se connecter"):
        from services.auth import verify_user
        if verify_user(username, password):
            st.session_state["user"] = username
            st.success(f"Bienvenue {username} !")
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect")

# -------------------------------
# Déconnexion
# -------------------------------
else:
    st.sidebar.success(f"Connecté en tant que {st.session_state['user']}")
    
    if st.sidebar.button("🔓 Se déconnecter"):
        st.session_state["user"] = None
        st.success("Vous êtes déconnecté")