import streamlit as st
import sys
import os
import pandas as pd
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.crud import get_all_business
from services.email_generator import generate_email_content
from services.email_sender import send_email

# Configuration
st.set_page_config(
    page_title="Campagnes Email",
    page_icon="📧",
    layout="wide"
)

# CSS ultra-moderne pour campagnes email
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        background-attachment: fixed;
    }
    
    /* Email Header élégant */
    .email-hero {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 4rem 3rem;
        border-radius: 25px;
        margin-bottom: 2.5rem;
        box-shadow: 0 25px 70px rgba(102, 126, 234, 0.5);
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .email-hero::before {
        content: "";
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.15) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .hero-content {
        position: relative;
        z-index: 1;
    }
    
    .email-icon-large {
        font-size: 6rem;
        margin-bottom: 1.5rem;
        display: inline-block;
        animation: pulse 2s ease-in-out infinite;
        filter: drop-shadow(0 10px 30px rgba(0, 0, 0, 0.3));
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
    
    .email-title {
        color: white;
        font-size: 3.5rem;
        font-weight: 900;
        margin: 0;
        text-shadow: 3px 3px 10px rgba(0,0,0,0.3);
    }
    
    .email-subtitle {
        color: rgba(255, 255, 255, 0.95);
        font-size: 1.4rem;
        margin-top: 1rem;
    }
    
    /* Process Steps */
    .steps-wrapper {
        background: white;
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
        margin: 2.5rem 0;
    }
    
    .steps-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 2rem;
        position: relative;
    }
    
    .step {
        text-align: center;
        position: relative;
    }
    
    .step-number {
        width: 70px;
        height: 70px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.8rem;
        font-weight: 900;
        margin: 0 auto 1rem;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
    }
    
    .step:hover .step-number {
        transform: scale(1.15) rotate(5deg);
    }
    
    .step-label {
        font-weight: 700;
        color: #1f2937;
        font-size: 1.1rem;
    }
    
    .step-description {
        color: #6b7280;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    /* Builder Cards */
    .builder-card {
        background: white;
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
        margin-bottom: 2rem;
        border-left: 5px solid #667eea;
        transition: all 0.3s ease;
    }
    
    .builder-card:hover {
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.12);
        transform: translateY(-3px);
    }
    
    .card-header {
        display: flex;
        align-items: center;
        gap: 1.2rem;
        margin-bottom: 2rem;
        padding-bottom: 1.5rem;
        border-bottom: 2px solid #f3f4f6;
    }
    
    .card-icon {
        width: 60px;
        height: 60px;
        border-radius: 15px;
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
    }
    
    .card-title {
        font-size: 2rem;
        font-weight: 800;
        color: #1f2937;
    }
    
    /* Stats Boxes */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .stat-box {
        background: linear-gradient(135deg, #667eea10 0%, #764ba210 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        border: 2px solid rgba(102, 126, 234, 0.2);
        transition: all 0.3s ease;
    }
    
    .stat-box:hover {
        transform: translateY(-5px);
        border-color: rgba(102, 126, 234, 0.5);
    }
    
    .stat-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        display: block;
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
    
    .stat-text {
        color: #6b7280;
        font-size: 0.95rem;
        font-weight: 600;
        margin-top: 0.5rem;
    }
    
    /* Email Preview moderne */
    .email-preview-container {
        background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%);
        border: 2px solid #e5e7eb;
        border-radius: 20px;
        padding: 2.5rem;
        margin: 2rem 0;
        box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.05);
    }
    
    .preview-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid #d1d5db;
    }
    
    .preview-icon {
        width: 45px;
        height: 45px;
        border-radius: 12px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        color: white;
    }
    
    .preview-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #1f2937;
    }
    
    .preview-content {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    }
    
    .email-meta {
        margin-bottom: 1.5rem;
        padding-bottom: 1.5rem;
        border-bottom: 2px solid #f3f4f6;
    }
    
    .email-meta-item {
        display: flex;
        margin: 0.5rem 0;
        font-size: 0.95rem;
    }
    
    .email-meta-label {
        font-weight: 700;
        color: #6b7280;
        width: 80px;
    }
    
    .email-meta-value {
        color: #1f2937;
        flex: 1;
    }
    
    .email-body {
        color: #374151;
        line-height: 1.8;
        font-size: 1rem;
        white-space: pre-wrap;
    }
    
    /* Recipient List */
    .recipients-container {
        max-height: 400px;
        overflow-y: auto;
        padding-right: 1rem;
    }
    
    .recipient-item {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
        padding: 1.2rem;
        border-radius: 12px;
        margin: 0.8rem 0;
        display: flex;
        align-items: center;
        gap: 1rem;
        transition: all 0.3s ease;
        border: 1px solid rgba(102, 126, 234, 0.1);
    }
    
    .recipient-item:hover {
        transform: translateX(8px);
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border-color: rgba(102, 126, 234, 0.3);
    }
    
    .recipient-avatar {
        width: 45px;
        height: 45px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.3rem;
        color: white;
        font-weight: 700;
    }
    
    .recipient-info {
        flex: 1;
    }
    
    .recipient-name {
        font-weight: 700;
        color: #1f2937;
        font-size: 1.05rem;
    }
    
    .recipient-details {
        color: #6b7280;
        font-size: 0.9rem;
        margin-top: 0.2rem;
    }
    
    /* Send Button spectaculaire */
    .send-section {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        padding: 3rem;
        border-radius: 20px;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 15px 40px rgba(16, 185, 129, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .send-section::before {
        content: "";
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.2) 0%, transparent 70%);
        animation: pulse-slow 4s ease-in-out infinite;
    }
    
    @keyframes pulse-slow {
        0%, 100% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.1); opacity: 0.8; }
    }
    
    .send-title {
        color: white;
        font-size: 2.5rem;
        font-weight: 900;
        margin-bottom: 1rem;
        position: relative;
        z-index: 1;
    }
    
    .send-subtitle {
        color: rgba(255, 255, 255, 0.95);
        font-size: 1.2rem;
        margin-bottom: 2rem;
        position: relative;
        z-index: 1;
    }
    
    /* Progress Bar */
    .progress-container {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 50px;
        padding: 0.5rem;
        margin: 1rem 0;
    }
    
    .progress-bar {
        background: white;
        height: 30px;
        border-radius: 50px;
        transition: width 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        color: #10b981;
    }
    
    /* Success Animation */
    .success-message {
        background: linear-gradient(135deg, #10b98120 0%, #05966920 100%);
        border: 2px solid #10b981;
        border-radius: 20px;
        padding: 2.5rem;
        text-align: center;
        margin: 2rem 0;
    }
    
    .success-icon {
        font-size: 5rem;
        margin-bottom: 1rem;
        animation: bounce 1s ease-in-out;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-20px); }
    }
    
    .success-title {
        font-size: 2rem;
        font-weight: 800;
        color: #047857;
        margin-bottom: 1rem;
    }
    
    .success-details {
        color: #059669;
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

# Vérification connexion
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("🔐 Veuillez vous connecter pour accéder à cette page.")
    st.stop()

# Header
st.markdown("""
<div class="email-hero">
    <div class="hero-content">
        <div class="email-icon-large">✉️</div>
        <h1 class="email-title">Campagnes Email</h1>
        <p class="email-subtitle">Créez et envoyez des emails personnalisés en quelques clics</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Steps
st.markdown("""
<div class="steps-wrapper">
    <div class="steps-container">
        <div class="step">
            <div class="step-number">1</div>
            <div class="step-label">Sélection</div>
            <div class="step-description">Choisir les destinataires</div>
        </div>
        <div class="step">
            <div class="step-number">2</div>
            <div class="step-label">Création</div>
            <div class="step-description">Rédiger le message</div>
        </div>
        <div class="step">
            <div class="step-number">3</div>
            <div class="step-label">Prévisualisation</div>
            <div class="step-description">Vérifier le rendu</div>
        </div>
        <div class="step">
            <div class="step-number">4</div>
            <div class="step-label">Envoi</div>
            <div class="step-description">Lancer la campagne</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Récupération des leads
leads = get_all_business()

if not leads:
    st.markdown("""
    <div style="text-align: center; padding: 5rem 2rem;">
        <div style="font-size: 5rem; margin-bottom: 1rem;">📭</div>
        <h2 style="color: #6b7280; font-size: 2rem; margin-bottom: 1rem;">Aucun lead disponible</h2>
        <p style="color: #9ca3af; font-size: 1.1rem;">Effectuez d'abord une recherche pour obtenir des prospects</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🔍 Lancer une recherche", type="primary", use_container_width=True):
        st.switch_page("pages/1_🔍_Recherche.py")
    st.stop()

df = pd.DataFrame(leads)
df_emails = df[df['email'].notna() & (df['email'] != "")]

# Statistiques
st.markdown('<div class="stats-grid">', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="stat-box">
        <span class="stat-icon">👥</span>
        <div class="stat-number">{len(df)}</div>
        <div class="stat-text">Total Leads</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-box">
        <span class="stat-icon">✅</span>
        <div class="stat-number">{len(df_emails)}</div>
        <div class="stat-text">Avec Email</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    percentage = (len(df_emails) / len(df) * 100) if len(df) > 0 else 0
    st.markdown(f"""
    <div class="stat-box">
        <span class="stat-icon">📊</span>
        <div class="stat-number">{percentage:.0f}%</div>
        <div class="stat-text">Taux Contact</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="stat-box">
        <span class="stat-icon">🎯</span>
        <div class="stat-number">{df['city'].nunique() if 'city' in df.columns else 0}</div>
        <div class="stat-text">Villes Ciblées</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Section 1: Sélection
st.markdown("""
<div class="builder-card">
    <div class="card-header">
        <div class="card-icon">👥</div>
        <h3 class="card-title">Étape 1 : Sélectionnez vos destinataires</h3>
    </div>
</div>
""", unsafe_allow_html=True)

recipient_option = st.radio(
    "Mode de sélection",
    ("📬 Tous les leads avec email", "🎯 Sélection personnalisée"),
    horizontal=True
)

selected_leads = []

if recipient_option == "📬 Tous les leads avec email":
    selected_leads = df_emails.to_dict('records')
    st.success(f"✅ {len(selected_leads)} destinataires automatiquement sélectionnés")
else:
    col1, col2, col3 = st.columns(3)
    with col1:
        city_filter = st.multiselect("📍 Filtrer par ville", df_emails['city'].unique() if 'city' in df_emails.columns else [])
    with col2:
        category_filter = st.multiselect("🏢 Filtrer par catégorie", df_emails['category'].unique() if 'category' in df_emails.columns else [])
    with col3:
        min_rating = st.slider("⭐ Note minimale", 0.0, 5.0, 0.0, 0.5)
    
    df_filtered = df_emails.copy()
    if city_filter:
        df_filtered = df_filtered[df_filtered['city'].isin(city_filter)]
    if category_filter:
        df_filtered = df_filtered[df_filtered['category'].isin(category_filter)]
    if 'rating' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['rating'] >= min_rating]
    
    selected_leads = df_filtered.to_dict('records')
    st.info(f"📊 {len(selected_leads)} destinataires après filtrage")

# Affichage des destinataires
if selected_leads:
    with st.expander(f"👀 Voir les {len(selected_leads)} destinataires sélectionnés", expanded=False):
        st.markdown('<div class="recipients-container">', unsafe_allow_html=True)
        for lead in selected_leads[:20]:
            initials = ''.join([word[0].upper() for word in lead['name'].split()[:2]])
            st.markdown(f"""
            <div class="recipient-item">
                <div class="recipient-avatar">{initials}</div>
                <div class="recipient-info">
                    <div class="recipient-name">{lead['name']}</div>
                    <div class="recipient-details">
                        📧 {lead['email']} • 📍 {lead.get('city', 'N/A')} • 🏢 {lead.get('category', 'N/A')}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        if len(selected_leads) > 20:
            st.info(f"... et {len(selected_leads) - 20} autres destinataires")
        st.markdown('</div>', unsafe_allow_html=True)

# Section 2: Création
st.markdown("""
<div class="builder-card">
    <div class="card-header">
        <div class="card-icon">✍️</div>
        <h3 class="card-title">Étape 2 : Créez votre message</h3>
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])

with col1:
    subject = st.text_input(
        "📌 Objet de l'email",
        value="🚀 Développez votre activité avec nos solutions innovantes",
        help="Un objet accrocheur augmente le taux d'ouverture"
    )

with col2:
    if st.button("🤖 Générer avec IA", use_container_width=True, type="secondary"):
        if selected_leads:
            with st.spinner("✨ Génération en cours..."):
                sample_lead = selected_leads[0]
                ai_content = generate_email_content(
                    sample_lead['name'], 
                    sample_lead.get('category', 'business')
                )
                st.session_state['ai_subject'] = ai_content.get('subject', subject)
                st.session_state['ai_body'] = ai_content.get('body', '')
            st.success("✅ Contenu généré par IA !")
            st.rerun()

# Corps du message
body = st.text_area(
    "✉️ Corps du message (utilisez {name} et {category} pour personnaliser)",
    value=st.session_state.get('ai_body', """Bonjour {name},

Nous avons découvert votre activité {category} et pensons que nos solutions pourraient vous intéresser.

🎯 Nos services vous permettent de :
• Automatiser votre prospection locale
• Obtenir des leads qualifiés en masse
• Économiser un temps précieux
• Augmenter votre chiffre d'affaires

💡 Plus de 500 entreprises nous font déjà confiance.

Souhaitez-vous en discuter ? Répondez simplement à cet email.

Cordialement,
Votre équipe de prospection"""),
    height=350
)

# Section 3: Prévisualisation
st.markdown("""
<div class="builder-card">
    <div class="card-header">
        <div class="card-icon">👁️</div>
        <h3 class="card-title">Étape 3 : Prévisualisez votre email</h3>
    </div>
</div>
""", unsafe_allow_html=True)

if selected_leads:
    sample = selected_leads[0]
    preview_subject = subject.format(
        name=sample['name'],
        category=sample.get('category', '')
    )
    preview_body = body.format(
        name=sample['name'],
        category=sample.get('category', '')
    )
    
    st.markdown('<div class="email-preview-container">', unsafe_allow_html=True)
    st.markdown("""
    <div class="preview-header">
        <div class="preview-icon">✉️</div>
        <div class="preview-title">Aperçu de l'email</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="preview-content">
        <div class="email-meta">
            <div class="email-meta-item">
                <span class="email-meta-label">De :</span>
                <span class="email-meta-value">votre-email@entreprise.com</span>
            </div>
            <div class="email-meta-item">
                <span class="email-meta-label">À :</span>
                <span class="email-meta-value">{sample['email']}</span>
            </div>
            <div class="email-meta-item">
                <span class="email-meta-label">Objet :</span>
                <span class="email-meta-value"><strong>{preview_subject}</strong></span>
            </div>
        </div>
        <div class="email-body">{preview_body}</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Section 4: Envoi
st.markdown("""
<div class="send-section">
    <h2 class="send-title">🚀 Prêt à lancer votre campagne ?</h2>
    <p class="send-subtitle">Envoyez votre message à {len(selected_leads)} destinataires qualifiés</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    if st.button("📤 LANCER LA CAMPAGNE", use_container_width=True, type="primary"):
        if not subject or not body:
            st.error("❌ Veuillez remplir l'objet et le corps de l'email")
        elif not selected_leads:
            st.error("❌ Aucun destinataire sélectionné")
        else:
            # Progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            sent_count = 0
            failed_count = 0
            total = len(selected_leads)
            
            for idx, lead in enumerate(selected_leads):
                try:
                    personalized_subject = subject.format(
                        name=lead['name'],
                        category=lead.get('category', '')
                    )
                    personalized_body = body.format(
                        name=lead['name'],
                        category=lead.get('category', '')
                    )
                    
                    send_email(lead['email'], personalized_subject, personalized_body)
                    sent_count += 1
                    
                except Exception as e:
                    failed_count += 1
                    st.warning(f"⚠️ Échec pour {lead['name']}: {str(e)}")
                
                # Update progress
                progress = (idx + 1) / total
                progress_bar.progress(progress)
                status_text.markdown(f"""
                <div style="text-align: center; padding: 1rem;">
                    <div style="font-size: 1.2rem; font-weight: 700; color: #1f2937;">
                        Envoi en cours... {idx + 1}/{total}
                    </div>
                    <div style="color: #6b7280; margin-top: 0.5rem;">
                        ✅ {sent_count} envoyés • ❌ {failed_count} échecs
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                time.sleep(0.1)  # Petit délai pour éviter le spam
            
            # Clear progress
            progress_bar.empty()
            status_text.empty()
            
            # Success message
            st.markdown(f"""
            <div class="success-message">
                <div class="success-icon">🎉</div>
                <div class="success-title">Campagne Terminée !</div>
                <div class="success-details">
                    ✅ <strong>{sent_count}</strong> emails envoyés avec succès<br>
                    ❌ <strong>{failed_count}</strong> échecs<br>
                    📊 Taux de réussite : <strong>{(sent_count/total*100):.1f}%</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.balloons()

# Tips section
st.markdown("""
<div class="builder-card" style="margin-top: 3rem;">
    <div class="card-header">
        <div class="card-icon">💡</div>
        <h3 class="card-title">Conseils pour une campagne réussie</h3>
    </div>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem;">
        <div style="padding: 1.5rem; background: #f9fafb; border-radius: 12px;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">✍️</div>
            <div style="font-weight: 700; color: #1f2937; margin-bottom: 0.5rem;">Objet accrocheur</div>
            <div style="color: #6b7280; font-size: 0.95rem;">
                Utilisez des émojis et soyez concis (max 50 caractères)
            </div>
        </div>
        <div style="padding: 1.5rem; background: #f9fafb; border-radius: 12px;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🎯</div>
            <div style="font-weight: 700; color: #1f2937; margin-bottom: 0.5rem;">Personnalisation</div>
            <div style="color: #6b7280; font-size: 0.95rem;">
                Utilisez {name} et {category} pour un message sur mesure
            </div>
        </div>
        <div style="padding: 1.5rem; background: #f9fafb; border-radius: 12px;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">⏰</div>
            <div style="font-weight: 700; color: #1f2937; margin-bottom: 0.5rem;">Timing optimal</div>
            <div style="color: #6b7280; font-size: 0.95rem;">
                Envoyez entre 9h-11h ou 14h-16h pour plus d'ouvertures
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)