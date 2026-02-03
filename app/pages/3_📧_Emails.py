import streamlit as st
import sys
import os
import pandas as pd

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

# CSS moderne pour campagnes email
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #fdfcfb 0%, #e2d1c3 100%);
    }
    
    /* Header Email Campaign */
    .email-header {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 3rem;
        border-radius: 25px;
        margin-bottom: 2rem;
        box-shadow: 0 20px 50px rgba(240, 147, 251, 0.4);
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .email-header::before {
        content: "✉️";
        position: absolute;
        right: -2rem;
        top: 50%;
        transform: translateY(-50%) rotate(15deg);
        font-size: 12rem;
        opacity: 0.1;
    }
    
    .email-title {
        color: white;
        font-size: 3rem;
        font-weight: 900;
        margin: 0;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.2);
    }
    
    .email-subtitle {
        color: rgba(255, 255, 255, 0.95);
        font-size: 1.3rem;
        margin-top: 0.8rem;
    }
    
    /* Steps Indicator */
    .steps-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 2rem;
        margin: 2rem 0;
        padding: 2rem;
        background: white;
        border-radius: 20px;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
    }
    
    .step {
        display: flex;
        flex-direction: column;
        align-items: center;
        position: relative;
    }
    
    .step-number {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        font-weight: 800;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    }
    
    .step-label {
        margin-top: 0.8rem;
        font-weight: 600;
        color: #4b5563;
    }
    
    .step-arrow {
        font-size: 2rem;
        color: #d1d5db;
    }
    
    /* Email Builder Cards */
    .builder-card {
        background: white;
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
        border-left: 5px solid #f093fb;
    }
    
    .card-header {
        display: flex;
        align-items: center;
        margin-bottom: 1.5rem;
    }
    
    .card-icon {
        font-size: 2.5rem;
        margin-right: 1rem;
    }
    
    .card-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1f2937;
    }
    
    /* Email Preview */
    .email-preview {
        background: #f9fafb;
        border: 2px dashed #d1d5db;
        border-radius: 15px;
        padding: 2rem;
        margin: 1.5rem 0;
    }
    
    .preview-label {
        font-size: 0.9rem;
        color: #6b7280;
        font-weight: 600;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .preview-content {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-top: 0.5rem;
        border: 1px solid #e5e7eb;
    }
    
    /* Recipient List */
    .recipient-item {
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        display: flex;
        align-items: center;
        transition: all 0.3s ease;
    }
    
    .recipient-item:hover {
        transform: translateX(5px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.2);
    }
    
    .recipient-icon {
        font-size: 1.5rem;
        margin-right: 1rem;
    }
    
    /* Send Button */
    .send-button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 1.5rem 3rem;
        border-radius: 15px;
        font-size: 1.3rem;
        font-weight: 700;
        border: none;
        cursor: pointer;
        width: 100%;
        box-shadow: 0 10px 30px rgba(16, 185, 129, 0.4);
        transition: all 0.3s ease;
    }
    
    .send-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 40px rgba(16, 185, 129, 0.5);
    }
    
    /* Stats */
    .email-stats {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .stat-box {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    }
    
    .stat-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 800;
        color: #f5576c;
    }
    
    .stat-text {
        color: #6b7280;
        font-size: 0.9rem;
        margin-top: 0.3rem;
    }
</style>
""", unsafe_allow_html=True)

# Vérification connexion
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("🔐 Veuillez vous connecter pour accéder à cette page.")
    st.stop()

# Header
st.markdown("""
<div class="email-header">
    <h1 class="email-title">📧 Campagnes Email</h1>
    <p class="email-subtitle">Créez et envoyez des emails personnalisés à vos prospects</p>
</div>
""", unsafe_allow_html=True)

# Steps
st.markdown("""
<div class="steps-container">
    <div class="step">
        <div class="step-number">1</div>
        <div class="step-label">Sélection</div>
    </div>
    <div class="step-arrow">→</div>
    <div class="step">
        <div class="step-number">2</div>
        <div class="step-label">Personnalisation</div>
    </div>
    <div class="step-arrow">→</div>
    <div class="step">
        <div class="step-number">3</div>
        <div class="step-label">Envoi</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Récupération des leads
leads = get_all_business()

if not leads:
    st.warning("📭 Aucun lead disponible. Effectuez d'abord une recherche !")
    st.stop()

df = pd.DataFrame(leads)
df_emails = df[df['email'].notna() & (df['email'] != "")]

# Statistiques
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="stat-box">
        <div class="stat-icon">👥</div>
        <div class="stat-number">{len(df)}</div>
        <div class="stat-text">Total Leads</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-box">
        <div class="stat-icon">✅</div>
        <div class="stat-number">{len(df_emails)}</div>
        <div class="stat-text">Avec Email</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    percentage = (len(df_emails) / len(df) * 100) if len(df) > 0 else 0
    st.markdown(f"""
    <div class="stat-box">
        <div class="stat-icon">📊</div>
        <div class="stat-number">{percentage:.0f}%</div>
        <div class="stat-text">Taux de contact</div>
    </div>
    """, unsafe_allow_html=True)

# Section 1: Sélection des destinataires
st.markdown("""
<div class="builder-card">
    <div class="card-header">
        <span class="card-icon">👥</span>
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
    st.success(f"✅ {len(selected_leads)} destinataires sélectionnés")
else:
    # Filtres personnalisés
    col1, col2 = st.columns(2)
    with col1:
        city_filter = st.multiselect("Filtrer par ville", df_emails['city'].unique())
    with col2:
        category_filter = st.multiselect("Filtrer par catégorie", df_emails['category'].unique())
    
    df_filtered = df_emails.copy()
    if city_filter:
        df_filtered = df_filtered[df_filtered['city'].isin(city_filter)]
    if category_filter:
        df_filtered = df_filtered[df_filtered['category'].isin(category_filter)]
    
    selected_leads = df_filtered.to_dict('records')
    st.info(f"📊 {len(selected_leads)} destinataires après filtrage")

# Affichage des destinataires
if selected_leads:
    with st.expander(f"👀 Voir les {len(selected_leads)} destinataires", expanded=False):
        for lead in selected_leads[:10]:  # Afficher max 10
            st.markdown(f"""
            <div class="recipient-item">
                <span class="recipient-icon">👤</span>
                <div>
                    <strong>{lead['name']}</strong><br>
                    <small>{lead['email']} • {lead.get('city', 'N/A')}</small>
                </div>
            </div>
            """, unsafe_allow_html=True)
        if len(selected_leads) > 10:
            st.info(f"... et {len(selected_leads) - 10} autres destinataires")

# Section 2: Création du contenu
st.markdown("""
<div class="builder-card">
    <div class="card-header">
        <span class="card-icon">✍️</span>
        <h3 class="card-title">Étape 2 : Créez votre message</h3>
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    subject = st.text_input(
        "📌 Objet de l'email",
        value="🚀 Développez votre activité locale avec nos solutions",
        help="Un bon objet incite à l'ouverture"
    )

with col2:
    if st.button("🤖 Générer avec IA", use_container_width=True):
        if selected_leads:
            sample_lead = selected_leads[0]
            ai_content = generate_email_content(sample_lead['name'], sample_lead.get('category', 'business'))
            st.session_state['ai_subject'] = ai_content.get('subject', subject)
            st.session_state['ai_body'] = ai_content.get('body', '')
            st.success("✨ Contenu généré par IA !")

# Corps du message
body = st.text_area(
    "✉️ Corps du message",
    value=st.session_state.get('ai_body', """Bonjour {name},

Nous avons remarqué votre entreprise {category} et pensons que notre solution pourrait vous intéresser.

Nos services vous permettent de :
• Automatiser votre prospection locale
• Obtenir des leads qualifiés
• Économiser du temps précieux

Souhaitez-vous en discuter ?

Cordialement,
Votre équipe"""),
    height=300,
    help="Utilisez {name} et {category} pour personnaliser"
)

# Prévisualisation
st.markdown('<div class="email-preview">', unsafe_allow_html=True)
st.markdown('<div class="preview-label">👁️ Prévisualisation</div>', unsafe_allow_html=True)

if selected_leads:
    sample = selected_leads[0]
    preview_subject = subject.format(name=sample['name'], category=sample.get('category', ''))
    preview_body = body.format(name=sample['name'], category=sample.get('category', ''))
    
    st.markdown(f"""
    <div class="preview-content">
        <strong>De :</strong> votre-email@entreprise.com<br>
        <strong>À :</strong> {sample['email']}<br>
        <strong>Objet :</strong> {preview_subject}<br><br>
        <div style="white-space: pre-wrap;">{preview_body}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Section 3: Envoi
st.markdown("""
<div class="builder-card">
    <div class="card-header">
        <span class="card-icon">🚀</span>
        <h3 class="card-title">Étape 3 : Lancez votre campagne</h3>
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    if st.button("📤 ENVOYER LA CAMPAGNE", use_container_width=True, type="primary"):
        if not subject or not body:
            st.error("❌ Veuillez remplir l'objet et le corps de l'email")
        elif not selected_leads:
            st.error("❌ Aucun destinataire sélectionné")
        else:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            sent_count = 0
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
                    
                    progress = (idx + 1) / total
                    progress_bar.progress(progress)
                    status_text.text(f"Envoi en cours... {idx + 1}/{total}")
                    
                except Exception as e:
                    st.warning(f"⚠️ Erreur pour {lead['name']}: {e}")
            
            progress_bar.empty()
            status_text.empty()
            
            st.success(f"""
            🎉 **Campagne terminée !**
            
            ✅ {sent_count} emails envoyés avec succès sur {total} destinataires
            """)
            
            # Confettis d'effet
            st.balloons()