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
    page_icon="🎯",
    layout="wide"
)

# CSS ultra-moderne avec nouveau design
st.markdown("""
<style>
    /* Fond moderne avec dégradé et image explicative */
    .stApp {
        background: linear-gradient(135deg, rgba(15, 32, 39, 0.95) 0%, rgba(32, 58, 67, 0.95) 50%, rgba(44, 83, 100, 0.95) 100%),
                    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1600 900'%3E%3Cdefs%3E%3ClinearGradient id='bg' x1='0%25' y1='0%25' x2='100%25' y2='100%25'%3E%3Cstop offset='0%25' style='stop-color:%23667eea;stop-opacity:0.1'/%3E%3Cstop offset='100%25' style='stop-color:%23764ba2;stop-opacity:0.1'/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='1600' height='900' fill='url(%23bg)'/%3E%3C!-- Google Maps Icon --%3E%3Cg opacity='0.15'%3E%3Ccircle cx='300' cy='200' r='80' fill='%23EA4335'/%3E%3Cpath d='M300 140 L300 200 L340 230 Z' fill='white'/%3E%3C/g%3E%3C!-- AI Brain --%3E%3Cg opacity='0.15'%3E%3Ccircle cx='800' cy='450' r='100' fill='none' stroke='%23667eea' stroke-width='4'/%3E%3Ccircle cx='780' cy='430' r='15' fill='%23667eea'/%3E%3Ccircle cx='820' cy='430' r='15' fill='%23667eea'/%3E%3Ccircle cx='780' cy='470' r='15' fill='%23667eea'/%3E%3Ccircle cx='820' cy='470' r='15' fill='%23667eea'/%3E%3Cline x1='780' y1='430' x2='820' y2='470' stroke='%23667eea' stroke-width='2'/%3E%3Cline x1='820' y1='430' x2='780' y2='470' stroke='%23667eea' stroke-width='2'/%3E%3C/g%3E%3C!-- Email Icons --%3E%3Cg opacity='0.12'%3E%3Crect x='1200' y='250' width='120' height='80' rx='10' fill='none' stroke='%2310b981' stroke-width='3'/%3E%3Cpath d='M1200 250 L1260 290 L1320 250' fill='none' stroke='%2310b981' stroke-width='3'/%3E%3C/g%3E%3C!-- Database --%3E%3Cg opacity='0.12'%3E%3Cellipse cx='400' cy='700' rx='80' ry='30' fill='none' stroke='%23f59e0b' stroke-width='3'/%3E%3Cpath d='M320 700 L320 750 Q400 780 480 750 L480 700' fill='none' stroke='%23f59e0b' stroke-width='3'/%3E%3C/g%3E%3C!-- Arrows --%3E%3Cg opacity='0.1'%3E%3Cpath d='M400 200 L700 450' stroke='%23667eea' stroke-width='3' stroke-dasharray='10,5'/%3E%3Cpath d='M900 450 L1150 280' stroke='%2310b981' stroke-width='3' stroke-dasharray='10,5'/%3E%3C/g%3E%3C/svg%3E");
        background-attachment: fixed;
        background-size: cover;
        background-position: center;
    }
    
    /* Hero Section */
    .hero-section {
        text-align: center;
        padding: 5rem 2rem 3rem 2rem;
        position: relative;
    }
    
    .hero-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1.5rem;
        border-radius: 50px;
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .hero-title {
        color: white;
        font-size: 4rem;
        font-weight: 900;
        margin: 1rem 0;
        line-height: 1.2;
        background: linear-gradient(135deg, #ffffff 0%, #a8edea 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .hero-subtitle {
        color: rgba(255, 255, 255, 0.85);
        font-size: 1.4rem;
        margin: 1.5rem auto;
        max-width: 700px;
        font-weight: 400;
        line-height: 1.6;
    }
    
    /* Image Hero */
    .hero-image-container {
        margin: 3rem auto;
        max-width: 1000px;
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 30px 80px rgba(0, 0, 0, 0.4);
        position: relative;
    }
    
    .hero-image {
        width: 100%;
        height: auto;
        display: block;
        object-fit: cover;
    }
    
    /* Stats Bar moderne */
    .stats-bar {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 2rem;
        margin: 4rem 2rem;
        max-width: 1200px;
        margin-left: auto;
        margin-right: auto;
    }
    
    .stat-item {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(20px);
        padding: 2rem;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.4s ease;
        text-align: center;
    }
    
    .stat-item:hover {
        transform: translateY(-10px);
        background: rgba(255, 255, 255, 0.12);
        border-color: rgba(102, 126, 234, 0.5);
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.2);
    }
    
    .stat-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        filter: drop-shadow(0 5px 15px rgba(102, 126, 234, 0.5));
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        display: block;
        margin: 0.5rem 0;
    }
    
    .stat-label {
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.8);
        font-weight: 500;
    }
    
    /* Login Card */
    .login-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(20px);
        border-radius: 25px;
        padding: 3rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        margin: 2rem 0;
    }
    
    .login-title {
        color: white;
        font-size: 1.8rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Features Grid avec images */
    .features-section {
        padding: 5rem 2rem;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    .section-title {
        text-align: center;
        color: white;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 1rem;
    }
    
    .section-subtitle {
        text-align: center;
        color: rgba(255, 255, 255, 0.7);
        font-size: 1.2rem;
        margin-bottom: 4rem;
    }
    
    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
        gap: 2.5rem;
    }
    
    .feature-card {
        background: white;
        backdrop-filter: blur(10px);
        border-radius: 25px;
        overflow: hidden;
        border: 1px solid rgba(102, 126, 234, 0.2);
        transition: all 0.4s ease;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
    }
    
    .feature-card:hover {
        transform: translateY(-15px);
        box-shadow: 0 30px 60px rgba(102, 126, 234, 0.3);
    }
    
    .feature-image {
        width: 100%;
        height: 200px;
        object-fit: cover;
        border-bottom: 3px solid rgba(102, 126, 234, 0.5);
    }
    
    .feature-content {
        padding: 2rem;
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    .feature-title {
        font-size: 1.6rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 1rem;
    }
    
    .feature-description {
        color: #4b5563;
        font-size: 1rem;
        line-height: 1.7;
        margin-bottom: 1.5rem;
    }
    
    /* CTA Section */
    .cta-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 5rem 2rem;
        border-radius: 30px;
        margin: 5rem 2rem;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .cta-section::before {
        content: "";
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: pulse 15s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
    
    .cta-title {
        font-size: 2.8rem;
        font-weight: 900;
        color: white;
        margin-bottom: 1.5rem;
        position: relative;
        z-index: 1;
    }
    
    .cta-text {
        font-size: 1.3rem;
        color: rgba(255, 255, 255, 0.95);
        margin-bottom: 3rem;
        position: relative;
        z-index: 1;
    }
    
    /* Testimonials */
    .testimonials-section {
        padding: 5rem 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .testimonials-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
    }
    
    .testimonial-card {
        background: white;
        backdrop-filter: blur(10px);
        padding: 2.5rem;
        border-radius: 20px;
        border: 1px solid rgba(102, 126, 234, 0.2);
        transition: all 0.3s ease;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
    }
    
    .testimonial-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
    }
    
    .testimonial-stars {
        color: #fbbf24;
        font-size: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .testimonial-text {
        color: #374151;
        font-size: 1.05rem;
        font-style: italic;
        margin-bottom: 1.5rem;
        line-height: 1.7;
    }
    
    .testimonial-author {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .author-avatar {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        color: white;
    }
    
    .author-info {
        flex: 1;
    }
    
    .author-name {
        color: #1f2937;
        font-weight: 700;
        font-size: 1.1rem;
    }
    
    .author-role {
        color: #6b7280;
        font-size: 0.9rem;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 3rem 2rem;
        color: rgba(255, 255, 255, 0.6);
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        margin-top: 5rem;
    }
    
    .footer-links {
        margin: 1.5rem 0;
    }
    
    .footer-link {
        color: rgba(255, 255, 255, 0.7);
        text-decoration: none;
        margin: 0 1.5rem;
        transition: color 0.3s ease;
    }
    
    .footer-link:hover {
        color: #667eea;
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
        <div class="hero-badge">🚀 Intelligence Artificielle & Data</div>
        <h1 class="hero-title">{APP_NAME}</h1>
        <p class="hero-subtitle">
            Trouvez, enrichissez et contactez des milliers de prospects qualifiés grâce à l'IA. 
            Transformez Google Maps en machine à leads.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Image Hero avec vraie photo
    st.markdown("""
    <div class="hero-image-container">
        <img src="https://images.unsplash.com/photo-1551434678-e076c223a692?w=1200&h=600&fit=crop" 
             alt="Business Analytics and AI" 
             class="hero-image"
             style="width: 100%; height: auto; display: block; border-radius: 20px;">
    </div>
    """, unsafe_allow_html=True)
    
    # Stats Bar
    st.markdown("""
    <div class="stats-bar">
        <div class="stat-item">
            <div class="stat-icon">🎯</div>
            <span class="stat-number">50K+</span>
            <span class="stat-label">Businesses Trouvés</span>
        </div>
        <div class="stat-item">
            <div class="stat-icon">⚡</div>
            <span class="stat-number">98%</span>
            <span class="stat-label">Précision IA</span>
        </div>
        <div class="stat-item">
            <div class="stat-icon">⏱️</div>
            <span class="stat-number">2min</span>
            <span class="stat-label">Setup Rapide</span>
        </div>
        <div class="stat-item">
            <div class="stat-icon">💼</div>
            <span class="stat-number">500+</span>
            <span class="stat-label">Utilisateurs Actifs</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Formulaire de connexion avec meilleure lisibilité
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="background: white; padding: 3rem 2.5rem; border-radius: 25px; box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);">
            <h2 style="text-align: center; color: #1f2937; font-size: 2rem; font-weight: 800; margin-bottom: 2rem;">
                🔐 Connexion
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("quick_login"):
            username = st.text_input("👤 Nom d'utilisateur", placeholder="Votre identifiant", key="username_login")
            password = st.text_input("🔒 Mot de passe", type="password", placeholder="Votre mot de passe", key="password_login")
            
            col_a, col_b = st.columns(2)
            with col_a:
                submit = st.form_submit_button("✨ SE CONNECTER", use_container_width=True)
            with col_b:
                if st.form_submit_button("📝 S'inscrire", use_container_width=True):
                    st.info("💬 Contactez l'administrateur pour créer un compte")
            
            if submit:
                from services.auth import verify_user
                if verify_user(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success(f"✅ Bienvenue {username} !")
                    st.rerun()
                else:
                    st.error("❌ Identifiants incorrects")
    
    # Features Section
    st.markdown("""
    <div class="features-section">
        <h2 class="section-title">Fonctionnalités Puissantes</h2>
        <p class="section-subtitle">Tous les outils dont vous avez besoin en un seul endroit</p>
        <div class="features-grid">
    """, unsafe_allow_html=True)
    
    # Feature 1 - Recherche Google Maps
    st.markdown("""
    <div class="feature-card">
        <img src="https://images.unsplash.com/photo-1524661135-423995f22d0b?w=800&h=400&fit=crop" 
             class="feature-image" alt="Google Maps Search" 
             style="width: 100%; height: 200px; object-fit: cover; border-bottom: 3px solid #667eea;">
        <div class="feature-content">
            <span class="feature-icon">🗺️</span>
            <h3 class="feature-title">Recherche Google Maps</h3>
            <p class="feature-description">
                Explorez des milliers de businesses locaux en temps réel. 
                Recherche par activité, zone géographique et critères avancés.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature 2 - Enrichissement IA
    st.markdown("""
    <div class="feature-card">
        <img src="https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800&h=400&fit=crop" 
             class="feature-image" alt="AI Technology" 
             style="width: 100%; height: 200px; object-fit: cover; border-bottom: 3px solid #764ba2;">
        <div class="feature-content">
            <span class="feature-icon">✨</span>
            <h3 class="feature-title">Enrichissement IA</h3>
            <p class="feature-description">
                Notre IA extrait automatiquement emails, téléphones et sites web. 
                Score de qualité pour chaque prospect.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature 3 - Analytics
    st.markdown("""
    <div class="feature-card">
        <img src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&h=400&fit=crop" 
             class="feature-image" alt="Analytics Dashboard" 
             style="width: 100%; height: 200px; object-fit: cover; border-bottom: 3px solid #f093fb;">
        <div class="feature-content">
            <span class="feature-icon">📈</span>
            <h3 class="feature-title">Analytics Temps Réel</h3>
            <p class="feature-description">
                Visualisez vos données avec des graphiques interactifs. 
                Insights pour optimiser votre stratégie.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature 4 - Campagnes Email
    st.markdown("""
    <div class="feature-card">
        <img src="https://images.unsplash.com/photo-1596526131083-e8c633c948d2?w=800&h=400&fit=crop" 
             class="feature-image" alt="Email Marketing" 
             style="width: 100%; height: 200px; object-fit: cover; border-bottom: 3px solid #4facfe;">
        <div class="feature-content">
            <span class="feature-icon">🚀</span>
            <h3 class="feature-title">Campagnes Automatisées</h3>
            <p class="feature-description">
                Emails personnalisés en masse avec IA. 
                Templates intelligents et suivi des performances.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature 5 - Filtrage
    st.markdown("""
    <div class="feature-card">
        <img src="https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&h=400&fit=crop" 
             class="feature-image" alt="Data Filtering" 
             style="width: 100%; height: 200px; object-fit: cover; border-bottom: 3px solid #43e97b;">
        <div class="feature-content">
            <span class="feature-icon">🔬</span>
            <h3 class="feature-title">Filtrage Intelligent</h3>
            <p class="feature-description">
                Trouvez exactement ce que vous cherchez. 
                Filtres par ville, secteur, note et disponibilité.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature 6 - Export
    st.markdown("""
    <div class="feature-card">
        <img src="https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=800&h=400&fit=crop" 
             class="feature-image" alt="Data Export" 
             style="width: 100%; height: 200px; object-fit: cover; border-bottom: 3px solid #fa709a;">
        <div class="feature-content">
            <span class="feature-icon">📤</span>
            <h3 class="feature-title">Export Multi-formats</h3>
            <p class="feature-description">
                CSV, Excel, JSON... Intégration facile avec vos outils CRM. 
                API disponible pour les développeurs.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    # Testimonials
    st.markdown("""
    <div class="testimonials-section">
        <h2 class="section-title">Ce Qu'ils Disent</h2>
        <p class="section-subtitle">Des milliers d'entreprises nous font confiance</p>
        <div class="testimonials-grid">
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="testimonial-card">
        <div class="testimonial-stars">⭐⭐⭐⭐⭐</div>
        <p class="testimonial-text">
            "J'ai trouvé 2000 leads qualifiés en 30 minutes. L'enrichissement IA est bluffant, 
            95% des emails sont valides. Un game-changer !"
        </p>
        <div class="testimonial-author">
            <div class="author-avatar">SM</div>
            <div class="author-info">
                <div class="author-name">Sophie Martin</div>
                <div class="author-role">CEO, Digital Agency</div>
            </div>
        </div>
    </div>
    
    <div class="testimonial-card">
        <div class="testimonial-stars">⭐⭐⭐⭐⭐</div>
        <p class="testimonial-text">
            "Le ROI est incroyable. En 2 semaines, j'ai généré plus de leads qu'en 6 mois 
            avec mes anciennes méthodes. Interface intuitive !"
        </p>
        <div class="testimonial-author">
            <div class="author-avatar">TL</div>
            <div class="author-info">
                <div class="author-name">Thomas Leblanc</div>
                <div class="author-role">Fondateur, SaaS Startup</div>
            </div>
        </div>
    </div>
    
    <div class="testimonial-card">
        <div class="testimonial-stars">⭐⭐⭐⭐⭐</div>
        <p class="testimonial-text">
            "Les campagnes email automatisées ont triplé notre taux de conversion. 
            L'IA génère des messages hyper personnalisés. Impressionnant !"
        </p>
        <div class="testimonial-author">
            <div class="author-avatar">MD</div>
            <div class="author-info">
                <div class="author-name">Marie Dubois</div>
                <div class="author-role">Dir. Marketing, Tech Corp</div>
            </div>
        </div>
    </div>
    </div></div>
    """, unsafe_allow_html=True)
    
    # CTA Section
    st.markdown("""
    <div class="cta-section">
        <h2 class="cta-title">Prêt à Révolutionner Votre Prospection ?</h2>
        <p class="cta-text">
            Rejoignez des centaines d'entreprises qui génèrent des leads qualifiés en automatique
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown(f"""
    <div class="footer">
        <div class="footer-links">
            <a href="#" class="footer-link">À propos</a>
            <a href="#" class="footer-link">Fonctionnalités</a>
            <a href="#" class="footer-link">Tarifs</a>
            <a href="#" class="footer-link">Contact</a>
            <a href="#" class="footer-link">Documentation</a>
        </div>
        <p><strong>{APP_NAME}</strong> v{APP_VERSION}</p>
        <p>Propulsé par l'Intelligence Artificielle • Fait avec ❤️ au Maroc</p>
        <p style="margin-top: 1rem; font-size: 0.85rem;">© 2024 {APP_NAME}. Tous droits réservés.</p>
    </div>
    """, unsafe_allow_html=True)

# Si connecté, afficher le dashboard principal
else:
    # Header connecté
    st.markdown(f"""
    <div class="hero-section" style="padding: 3rem 2rem;">
        <div class="hero-badge">👋 Bienvenue de retour</div>
        <h1 class="hero-title" style="font-size: 3rem;">Hey {st.session_state.username} !</h1>
        <p class="hero-subtitle">Votre tableau de bord de prospection intelligente</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Bouton de déconnexion
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("🔓 Déconnexion", use_container_width=True, type="secondary"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()
    
    # Statistiques rapides
    leads = get_all_business()
    total_leads = len(leads) if leads else 0
    emails_count = sum(1 for lead in leads if lead.get('email')) if leads else 0
    phones_count = sum(1 for lead in leads if lead.get('phone')) if leads else 0
    
    st.markdown(f"""
    <div class="stats-bar">
        <div class="stat-item">
            <div class="stat-icon">👥</div>
            <span class="stat-number">{total_leads}</span>
            <span class="stat-label">Leads Total</span>
        </div>
        <div class="stat-item">
            <div class="stat-icon">📧</div>
            <span class="stat-number">{emails_count}</span>
            <span class="stat-label">Avec Email</span>
        </div>
        <div class="stat-item">
            <div class="stat-icon">📱</div>
            <span class="stat-number">{phones_count}</span>
            <span class="stat-label">Avec Téléphone</span>
        </div>
        <div class="stat-item">
            <div class="stat-icon">⚡</div>
            <span class="stat-number">{(emails_count/total_leads*100) if total_leads > 0 else 0:.0f}%</span>
            <span class="stat-label">Taux Enrichissement</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation rapide avec images
    st.markdown('<div class="features-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Actions Rapides</h2>', unsafe_allow_html=True)
    st.markdown('<div class="features-grid">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <img src="https://images.unsplash.com/photo-1526628953301-3e589a6a8b74?w=800&h=400&fit=crop" 
                 alt="Search" style="width: 100%; height: 200px; object-fit: cover; border-bottom: 3px solid #667eea;">
            <div class="feature-content">
                <span class="feature-icon">🔍</span>
                <h3 class="feature-title">Recherche</h3>
                <p class="feature-description">
                    Lancer une nouvelle recherche de prospects
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚀 Démarrer", key="search_btn", use_container_width=True):
            st.switch_page("pages/1_🔍_Recherche.py")
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <img src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&h=400&fit=crop" 
                 alt="Dashboard" style="width: 100%; height: 200px; object-fit: cover; border-bottom: 3px solid #764ba2;">
            <div class="feature-content">
                <span class="feature-icon">📊</span>
                <h3 class="feature-title">Dashboard</h3>
                <p class="feature-description">
                    Gérer et analyser vos leads
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("📈 Accéder", key="dash_btn", use_container_width=True):
            st.switch_page("pages/2_📊_Dashboard.py")
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <img src="https://images.unsplash.com/photo-1557804506-669a67965ba0?w=800&h=400&fit=crop" 
                 alt="Email Campaign" style="width: 100%; height: 200px; object-fit: cover; border-bottom: 3px solid #f093fb;">
            <div class="feature-content">
                <span class="feature-icon">📧</span>
                <h3 class="feature-title">Campagnes</h3>
                <p class="feature-description">
                    Envoyer des emails personnalisés
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("✉️ Créer", key="campaign_btn", use_container_width=True):
            st.switch_page("pages/3_📧_Campagnes.py")
    
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    # Activité récente
    if leads:
        import pandas as pd
        st.markdown('<div class="cta-section" style="margin-top: 3rem;">', unsafe_allow_html=True)
        st.markdown('<h2 class="cta-title" style="font-size: 2rem;">📈 Activité Récente</h2>', unsafe_allow_html=True)
        
        df = pd.DataFrame(leads[-10:])  # 10 derniers leads
        st.dataframe(
            df[["name", "category", "city", "email", "phone"]],
            use_container_width=True,
            hide_index=True
        )
        
        st.markdown('</div>', unsafe_allow_html=True)