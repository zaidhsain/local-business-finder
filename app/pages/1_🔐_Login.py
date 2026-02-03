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
    page_icon="🎯",
    layout="centered"
)

# CSS moderne avec design élégant
st.markdown("""
<style>
    /* Arrière-plan moderne */
    .stApp {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        background-attachment: fixed;
    }
    
    /* Container principal */
    .login-wrapper {
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 2rem;
    }
    
    .login-container {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(20px);
        border-radius: 30px;
        padding: 3rem 2.5rem;
        box-shadow: 0 30px 80px rgba(0, 0, 0, 0.4);
        max-width: 480px;
        width: 100%;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Logo animé */
    .logo-container {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .logo-3d {
        font-size: 5rem;
        margin-bottom: 1rem;
        display: inline-block;
        animation: float 4s ease-in-out infinite;
        filter: drop-shadow(0 15px 30px rgba(102, 126, 234, 0.6));
    }
    
    @keyframes float {
        0%, 100% { 
            transform: translateY(0px) rotate(0deg); 
        }
        50% { 
            transform: translateY(-20px) rotate(5deg); 
        }
    }
    
    /* Titre */
    .main-title {
        text-align: center;
        color: white;
        font-size: 2.5rem;
        font-weight: 900;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #ffffff 0%, #a8edea 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .subtitle {
        text-align: center;
        color: rgba(255, 255, 255, 0.75);
        font-size: 1.1rem;
        margin-bottom: 2.5rem;
        line-height: 1.6;
    }
    
    /* Badge */
    .badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.4rem 1.2rem;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Inputs modernisés */
    .stTextInput input {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 15px !important;
        padding: 1rem 1.2rem !important;
        font-size: 1rem !important;
        color: white !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput input::placeholder {
        color: rgba(255, 255, 255, 0.5) !important;
    }
    
    .stTextInput input:focus {
        background: rgba(255, 255, 255, 0.15) !important;
        border-color: #667eea !important;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.2) !important;
    }
    
    .stTextInput label {
        color: rgba(255, 255, 255, 0.9) !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Boutons */
    .stButton button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 1rem 2rem;
        font-size: 1.1rem;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.5);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.6);
    }
    
    /* Divider */
    .divider {
        display: flex;
        align-items: center;
        margin: 2rem 0;
        color: rgba(255, 255, 255, 0.5);
        font-size: 0.9rem;
    }
    
    .divider::before,
    .divider::after {
        content: "";
        flex: 1;
        height: 1px;
        background: rgba(255, 255, 255, 0.2);
    }
    
    .divider span {
        padding: 0 1rem;
    }
    
    /* Features mini */
    .features-mini {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1.5rem;
        margin-top: 2.5rem;
        padding-top: 2rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .feature-mini-item {
        text-align: center;
    }
    
    .feature-mini-icon {
        font-size: 2.5rem;
        margin-bottom: 0.8rem;
        display: block;
        filter: drop-shadow(0 5px 15px rgba(102, 126, 234, 0.3));
    }
    
    .feature-mini-text {
        font-size: 0.85rem;
        color: rgba(255, 255, 255, 0.75);
        font-weight: 500;
        line-height: 1.4;
    }
    
    /* Background decoration */
    .bg-decoration {
        position: fixed;
        width: 500px;
        height: 500px;
        border-radius: 50%;
        filter: blur(100px);
        opacity: 0.15;
        z-index: -1;
    }
    
    .bg-decoration-1 {
        background: #667eea;
        top: -250px;
        left: -250px;
    }
    
    .bg-decoration-2 {
        background: #764ba2;
        bottom: -250px;
        right: -250px;
    }
    
    /* Image illustration */
    .login-illustration {
        margin: 2rem 0;
        text-align: center;
    }
    
    .illustration-svg {
        width: 100%;
        max-width: 300px;
        height: auto;
        filter: drop-shadow(0 10px 30px rgba(102, 126, 234, 0.3));
    }
    
    /* Info card */
    .info-card {
        background: rgba(102, 126, 234, 0.1);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        color: rgba(255, 255, 255, 0.85);
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    .info-icon {
        font-size: 1.5rem;
        margin-right: 0.8rem;
        vertical-align: middle;
    }
</style>
""", unsafe_allow_html=True)

# Initialisation session
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# Décorations background
st.markdown("""
<div class="bg-decoration bg-decoration-1"></div>
<div class="bg-decoration bg-decoration-2"></div>
""", unsafe_allow_html=True)

# Affichage de la page de connexion
if not st.session_state.logged_in:
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    # Logo et badge
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    st.markdown('<div class="badge">🚀 Powered by AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="logo-3d">🎯</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Titre
    st.markdown(f'<h1 class="main-title">{APP_NAME}</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Votre plateforme de prospection locale intelligente</p>', unsafe_allow_html=True)
    
    # Illustration
    st.markdown("""
    <div class="login-illustration">
        <svg class="illustration-svg" viewBox="0 0 300 200" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
                </linearGradient>
            </defs>
            <rect x="50" y="50" width="200" height="120" rx="15" fill="url(#grad1)" opacity="0.8"/>
            <circle cx="150" cy="80" r="20" fill="white" opacity="0.9"/>
            <text x="150" y="90" text-anchor="middle" fill="#667eea" font-size="20" font-weight="bold">AI</text>
            <rect x="80" y="120" width="140" height="8" rx="4" fill="white" opacity="0.6"/>
            <rect x="80" y="140" width="100" height="8" rx="4" fill="white" opacity="0.4"/>
        </svg>
    </div>
    """, unsafe_allow_html=True)
    
    # Formulaire de connexion
    username = st.text_input(
        "👤 Nom d'utilisateur",
        placeholder="Entrez votre identifiant",
        key="username_input"
    )
    
    password = st.text_input(
        "🔒 Mot de passe",
        type="password",
        placeholder="Entrez votre mot de passe",
        key="password_input"
    )
    
    # Bouton connexion
    col1, col2 = st.columns([3, 2])
    with col1:
        if st.button("🚀 SE CONNECTER", key="login_btn"):
            from services.auth import verify_user
            if verify_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"✅ Bienvenue {username} !")
                st.balloons()
                st.rerun()
            else:
                st.error("❌ Identifiants incorrects")
    
    with col2:
        if st.button("💬 Aide", key="help_btn"):
            st.info("📞 Contactez l'administrateur pour créer un compte ou récupérer votre mot de passe")
    
    # Divider
    st.markdown("""
    <div class="divider">
        <span>Pourquoi nous choisir ?</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Features mini
    st.markdown("""
    <div class="features-mini">
        <div class="feature-mini-item">
            <span class="feature-mini-icon">🤖</span>
            <div class="feature-mini-text">Intelligence<br>Artificielle</div>
        </div>
        <div class="feature-mini-item">
            <span class="feature-mini-icon">⚡</span>
            <div class="feature-mini-text">Automation<br>Complète</div>
        </div>
        <div class="feature-mini-item">
            <span class="feature-mini-icon">📊</span>
            <div class="feature-mini-text">Analytics<br>en Temps Réel</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Info card
    st.markdown("""
    <div class="info-card">
        <span class="info-icon">💡</span>
        <strong>Nouveau ?</strong> Découvrez comment nous utilisons l'IA pour extraire 
        automatiquement les coordonnées depuis Google Maps et enrichir vos prospects.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown(f"""
    <div style="text-align: center; margin-top: 3rem; color: rgba(255, 255, 255, 0.5); font-size: 0.85rem;">
        <p><strong>{APP_NAME}</strong> v{APP_VERSION}</p>
        <p>© 2024 - Propulsé par l'Intelligence Artificielle</p>
    </div>
    """, unsafe_allow_html=True)
    
else:
    # Rediriger vers la page principale
    st.switch_page("pages/1_🔍_Recherche.py")