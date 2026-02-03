import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.settings import APP_NAME, APP_VERSION
from services.database import create_tables
from services.crud import get_all_business

# Initialisation DB
create_tables()

# Configuration page
st.set_page_config(
    page_title=f"{APP_NAME} - Accueil",
    page_icon="🚀",
    layout="wide"
)

# CSS ultra-moderne pour la page d'accueil
st.markdown("""
<style>
    /* Fond animé avec gradient */
    .stApp {
        background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #4facfe);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Hero Section */
    .hero-section {
        text-align: center;
        padding: 4rem 2rem;
        margin-bottom: 3rem;
    }
    
    .logo-3d {
        font-size: 8rem;
        margin-bottom: 1rem;
        animation: float 4s ease-in-out infinite;
        filter: drop-shadow(0 20px 40px rgba(0,0,0,0.3));
        display: inline-block;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-30px) rotate(5deg); }
    }
    
    .hero-title {
        color: white;
        font-size: 4.5rem;
        font-weight: 900;
        margin: 1rem 0;
        text-shadow: 3px 3px 10px rgba(0,0,0,0.3);
        letter-spacing: -2px;
    }
    
    .hero-subtitle {
        color: rgba(255, 255, 255, 0.95);
        font-size: 1.8rem;
        margin: 1rem 0 2rem 0;
        font-weight: 300;
        text-shadow: 2px 2px 5px rgba(0,0,0,0.2);
    }
    
    .hero-description {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.2rem;
        max-width: 700px;
        margin: 0 auto 3rem auto;
        line-height: 1.8;
    }
    
    /* Stats Bar */
    .stats-bar {
        display: flex;
        justify-content: center;
        gap: 3rem;
        margin: 3rem 0;
        flex-wrap: wrap;
    }
    
    .stat-item {
        text-align: center;
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        padding: 1.5rem 2.5rem;
        border-radius: 20px;
        border: 2px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
    }
    
    .stat-item:hover {
        transform: translateY(-10px);
        background: rgba(255, 255, 255, 0.25);
    }
    
    .stat-number {
        font-size: 3rem;
        font-weight: 900;
        color: white;
        display: block;
    }
    
    .stat-label {
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.9);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.5rem;
    }
    
    /* Features Grid */
    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
        gap: 2rem;
        margin: 3rem 0;
        padding: 0 2rem;
    }
    
    .feature-card {
        background: white;
        padding: 3rem 2rem;
        border-radius: 25px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
        text-align: center;
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 5px;
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    
    .feature-card:hover {
        transform: translateY(-15px) scale(1.02);
        box-shadow: 0 30px 80px rgba(0, 0, 0, 0.3);
    }
    
    .feature-icon {
        font-size: 5rem;
        margin-bottom: 1.5rem;
        display: inline-block;
        animation: bounce 2s infinite;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    .feature-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 1rem;
    }
    
    .feature-description {
        color: #6b7280;
        font-size: 1.1rem;
        line-height: 1.7;
        margin-bottom: 1.5rem;
    }
    
    .feature-link {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.8rem 2rem;
        border-radius: 25px;
        text-decoration: none;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .feature-link:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* CTA Section */
    .cta-section {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(15px);
        padding: 4rem 2rem;
        border-radius: 30px;
        margin: 4rem 2rem;
        text-align: center;
        border: 2px solid rgba(255, 255, 255, 0.2);
    }
    
    .cta-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: white;
        margin-bottom: 1rem;
    }
    
    .cta-text {
        font-size: 1.3rem;
        color: rgba(255, 255, 255, 0.9);
        margin-bottom: 2rem;
    }
    
    .cta-button {
        display: inline-block;
        background: white;
        color: #667eea;
        padding: 1.2rem 3rem;
        border-radius: 30px;
        font-size: 1.3rem;
        font-weight: 700;
        text-decoration: none;
        transition: all 0.3s ease;
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2);
    }
    
    .cta-button:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
    }
    
    /* Testimonials */
    .testimonials {
        display: flex;
        gap: 2rem;
        margin: 3rem 2rem;
        flex-wrap: wrap;
        justify-content: center;
    }
    
    .testimonial-card {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 20px;
        max-width: 400px;
        border: 2px solid rgba(255, 255, 255, 0.3);
    }
    
    .testimonial-text {
        color: white;
        font-size: 1.1rem;
        font-style: italic;
        margin-bottom: 1rem;
        line-height: 1.6;
    }
    
    .testimonial-author {
        color: rgba(255, 255, 255, 0.9);
        font-weight: 600;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: rgba(255, 255, 255, 0.8);
        margin-top: 4rem;
    }
</style>
""", unsafe_allow_html=True)

# Vérification connexion
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# Si non connecté, afficher la page d'accueil publique
if not st.session_state.logged_in:
    # Hero Section
    st.markdown(f"""
    <div class="hero-section">
        <div class="logo-3d">🚀</div>
        <h1 class="hero-title">{APP_NAME}</h1>
        <p class="hero-subtitle">L'automatisation intelligente de votre prospection locale</p>
        <p class="hero-description">
            Découvrez, enrichissez et contactez des milliers de prospects qualifiés 
            en quelques clics. La solution complète pour booster votre business.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats Bar
    st.markdown("""
    <div class="stats-bar">
        <div class="stat-item">
            <span class="stat-number">10K+</span>
            <span class="stat-label">Leads trouvés</span>
        </div>
        <div class="stat-item">
            <span class="stat-number">95%</span>
            <span class="stat-label">Taux d'enrichissement</span>
        </div>
        <div class="stat-item">
            <span class="stat-number">5min</span>
            <span class="stat-label">Pour démarrer</span>
        </div>
        <div class="stat-item">
            <span class="stat-number">24/7</span>
            <span class="stat-label">Disponibilité</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Bouton de connexion principal
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div style="text-align: center; margin: 2rem 0;">', unsafe_allow_html=True)
        
        # Formulaire de connexion rapide
        with st.form("quick_login"):
            st.markdown("### 🔐 Connexion rapide")
            username = st.text_input("👤 Nom d'utilisateur", placeholder="Votre identifiant")
            password = st.text_input("🔒 Mot de passe", type="password", placeholder="Votre mot de passe")
            
            col_a, col_b = st.columns(2)
            with col_a:
                submit = st.form_submit_button("✨ SE CONNECTER", use_container_width=True)
            with col_b:
                if st.form_submit_button("📝 Créer un compte", use_container_width=True):
                    st.info("Contactez l'administrateur pour créer un compte")
            
            if submit:
                from services.auth import verify_user
                if verify_user(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success(f"✅ Bienvenue {username} !")
                    st.rerun()
                else:
                    st.error("❌ Identifiants incorrects")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Features Grid
    st.markdown('<div class="features-grid">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🔍</div>
        <h3 class="feature-title">Recherche Intelligente</h3>
        <p class="feature-description">
            Trouvez des milliers de prospects locaux en quelques secondes. 
            Recherche par activité, ville et critères personnalisés.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📧</div>
        <h3 class="feature-title">Enrichissement Auto</h3>
        <p class="feature-description">
            Emails, téléphones, sites web et réseaux sociaux automatiquement 
            récupérés pour chaque prospect.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📊</div>
        <h3 class="feature-title">Analytics Avancés</h3>
        <p class="feature-description">
            Visualisez vos données avec des graphiques interactifs. 
            Optimisez votre stratégie grâce aux insights.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">✉️</div>
        <h3 class="feature-title">Campagnes Email</h3>
        <p class="feature-description">
            Créez et envoyez des emails personnalisés en masse. 
            Générateur IA pour des messages percutants.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🎯</div>
        <h3 class="feature-title">Ciblage Précis</h3>
        <p class="feature-description">
            Filtrez par ville, secteur d'activité et note. 
            Trouvez exactement les prospects qu'il vous faut.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">💾</div>
        <h3 class="feature-title">Export Facile</h3>
        <p class="feature-description">
            Exportez vos données en CSV pour les utiliser 
            dans vos outils CRM préférés.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Testimonials
    st.markdown("""
    <div class="testimonials">
        <div class="testimonial-card">
            <p class="testimonial-text">
                "Incroyable ! J'ai trouvé 500 leads qualifiés en moins de 10 minutes. 
                Le gain de temps est phénoménal."
            </p>
            <p class="testimonial-author">— Sophie M., Consultante Marketing</p>
        </div>
        <div class="testimonial-card">
            <p class="testimonial-text">
                "L'enrichissement automatique des données est bluffant. 
                95% de mes prospects ont un email valide !"
            </p>
            <p class="testimonial-author">— Thomas L., Fondateur Startup</p>
        </div>
        <div class="testimonial-card">
            <p class="testimonial-text">
                "Les campagnes email automatisées ont multiplié mon taux de conversion par 3. 
                Un outil indispensable."
            </p>
            <p class="testimonial-author">— Marie D., Directrice Commerciale</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # CTA Section
    st.markdown("""
    <div class="cta-section">
        <h2 class="cta-title">Prêt à transformer votre prospection ?</h2>
        <p class="cta-text">Rejoignez des centaines d'entreprises qui font confiance à notre solution</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown(f"""
    <div class="footer">
        <p><strong>{APP_NAME}</strong> v{APP_VERSION}</p>
        <p>Propulsé par l'intelligence artificielle • Fait avec ❤️</p>
    </div>
    """, unsafe_allow_html=True)

# Si connecté, afficher le dashboard principal
else:
    # Header connecté
    st.markdown(f"""
    <div class="hero-section">
        <div class="logo-3d">🎯</div>
        <h1 class="hero-title">Bienvenue {st.session_state.username} !</h1>
        <p class="hero-subtitle">Votre tableau de bord de prospection intelligente</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Bouton de déconnexion
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("🔓 Déconnexion", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()
    
    # Statistiques rapides
    leads = get_all_business()
    total_leads = len(leads) if leads else 0
    emails_count = sum(1 for lead in leads if lead.get('email')) if leads else 0
    
    st.markdown(f"""
    <div class="stats-bar">
        <div class="stat-item">
            <span class="stat-number">{total_leads}</span>
            <span class="stat-label">Leads Total</span>
        </div>
        <div class="stat-item">
            <span class="stat-number">{emails_count}</span>
            <span class="stat-label">Avec Email</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation rapide vers les fonctionnalités
    st.markdown('<div class="features-grid">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🔍</div>
            <h3 class="feature-title">Recherche</h3>
            <p class="feature-description">
                Trouvez de nouveaux prospects qualifiés
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Lancer une recherche", key="search_btn", use_container_width=True):
            st.switch_page("pages/1_🔍_Recherche.py")
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <h3 class="feature-title">Dashboard</h3>
            <p class="feature-description">
                Gérez et analysez vos leads
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Voir le dashboard", key="dash_btn", use_container_width=True):
            st.switch_page("pages/2_📊_Dashboard.py")
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📧</div>
            <h3 class="feature-title">Campagnes</h3>
            <p class="feature-description">
                Envoyez des emails personnalisés
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Créer une campagne", key="campaign_btn", use_container_width=True):
            st.switch_page("pages/3_📧_Campagnes.py")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Activité récente
    if leads:
        st.markdown('<div class="cta-section">', unsafe_allow_html=True)
        st.markdown('<h2 class="cta-title">📈 Activité Récente</h2>', unsafe_allow_html=True)
        
        import pandas as pd
        df = pd.DataFrame(leads[-5:])  # 5 derniers leads
        
        st.dataframe(
            df[["name", "category", "city", "email"]],
            use_container_width=True,
            hide_index=True
        )
        
        st.markdown('</div>', unsafe_allow_html=True)