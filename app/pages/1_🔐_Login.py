import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.settings import APP_NAME, APP_VERSION
from services.database import create_tables

# Initialisation DB
create_tables()

# Configuration page
st.set_page_config(
    page_title=f"{APP_NAME} - Connexion",
    page_icon="🚀",
    layout="centered"
)

# CSS personnalisé pour un design moderne
st.markdown("""
<style>
    /* Arrière-plan avec gradient animé */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Container principal */
    .login-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 30px;
        padding: 3rem 2.5rem;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        max-width: 450px;
        margin: 2rem auto;
    }
    
    /* Logo 3D */
    .logo-3d {
        text-align: center;
        font-size: 5rem;
        margin-bottom: 1rem;
        animation: float 3s ease-in-out infinite;
        filter: drop-shadow(0 10px 20px rgba(102, 126, 234, 0.4));
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }
    
    /* Titre principal */
    .main-title {
        text-align: center;
        color: #667eea;
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .subtitle {
        text-align: center;
        color: #6b7280;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Inputs stylisés */
    .stTextInput input {
        border-radius: 15px !important;
        border: 2px solid #e5e7eb !important;
        padding: 0.8rem 1rem !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    /* Bouton personnalisé */
    .stButton button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 0.9rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
    }
    
    .stButton button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.5);
    }
    
    /* Features icons */
    .features {
        display: flex;
        justify-content: space-around;
        margin-top: 2rem;
        padding-top: 2rem;
        border-top: 2px solid #e5e7eb;
    }
    
    .feature-item {
        text-align: center;
    }
    
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    
    .feature-text {
        font-size: 0.85rem;
        color: #6b7280;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# Initialisation session
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# Affichage de la page de connexion
if not st.session_state.logged_in:
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    # Logo et titre
    st.markdown('<div class="logo-3d">🚀</div>', unsafe_allow_html=True)
    st.markdown(f'<h1 class="main-title">{APP_NAME}</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Automatisation intelligente de prospection locale</p>', unsafe_allow_html=True)
    
    # Formulaire de connexion
    username = st.text_input("👤 Nom d'utilisateur", placeholder="Entrez votre nom d'utilisateur")
    password = st.text_input("🔒 Mot de passe", type="password", placeholder="Entrez votre mot de passe")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔓 SE CONNECTER"):
            from services.auth import verify_user
            if verify_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"✅ Bienvenue {username} !")
                st.rerun()
            else:
                st.error("❌ Identifiants incorrects")
    
    # Features
    st.markdown("""
    <div class="features">
        <div class="feature-item">
            <div class="feature-icon">🔍</div>
            <div class="feature-text">Recherche<br>Intelligente</div>
        </div>
        <div class="feature-item">
            <div class="feature-icon">📊</div>
            <div class="feature-text">Analytics<br>Avancés</div>
        </div>
        <div class="feature-item">
            <div class="feature-icon">📧</div>
            <div class="feature-text">Email<br>Automatisé</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
else:
    # Rediriger vers la page principale
    st.switch_page("pages/1_🔍_Recherche.py")