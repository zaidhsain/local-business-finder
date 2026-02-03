import streamlit as st
import sys
import os
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from services.discovery import search_local_business_full

# Configuration
st.set_page_config(
    page_title="Recherche Business",
    page_icon="🔍",
    layout="wide"
)

# CSS moderne avec illustrations

st.markdown("""
<style>
/* ==============================
   CORRECTION LISIBILITÉ GLOBALE
   ============================== */

/* Texte global */
html, body, [class*="css"] {
    color: #111827 !important; /* quasi noir */
}

/* Fond principal */
.stApp {
    background: linear-gradient(135deg, #f9fafb 0%, #e5e7eb 100%);
}

/* Titres */
h1, h2, h3, h4, h5, h6 {
    color: #111827 !important;
}

/* Paragraphes & labels */
p, label, span, li {
    color: #1f2937 !important;
}

/* Inputs */
.stTextInput input,
.stSelectbox select,
.stTextArea textarea {
    background-color: #ffffff !important;
    color: #111827 !important;
    border: 2px solid #d1d5db !important;
}

/* Placeholder */
.stTextInput input::placeholder {
    color: #6b7280 !important;
}

/* Slider */
.stSlider label {
    color: #111827 !important;
}

/* DataFrame */
[data-testid="stDataFrame"] {
    background-color: white !important;
}

[data-testid="stDataFrame"] th {
    background-color: #f3f4f6 !important;
    color: #111827 !important;
    font-weight: 700;
}

[data-testid="stDataFrame"] td {
    color: #111827 !important;
}

/* Messages Streamlit */
.stAlert {
    color: #111827 !important;
}

/* Warning / error / success */
.stAlert p {
    color: #111827 !important;
}

/* Boutons */
.stButton > button {
    color: white !important;
}

/* Card titles */
.card-title,
.info-title {
    color: #111827 !important;
}

/* Stats labels */
.stat-label {
    color: #374151 !important;
}

/* Info text */
.info-text {
    color: #374151 !important;
}
</style>
""", unsafe_allow_html=True)


# Vérification connexion
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("🔐 Veuillez vous connecter pour accéder à cette page.")
    st.stop()

# Header avec illustration
st.markdown("""
<div class="header-container">
    <div class="header-content">
        <div class="header-icon">🔍</div>
        <h1 class="header-title">Recherche Business Locale</h1>
        <p class="header-subtitle">Trouvez et enrichissez vos prospects en quelques clics grâce à l'IA</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Section de recherche
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="input-card">
        <div class="card-header">
            <div class="card-icon">🏢</div>
            <h3 class="card-title">Type d'activité</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<p style="color: #1f2937; font-weight: 600; margin-bottom: 0.5rem; font-size: 1rem;">🔍 Que recherchez-vous ?</p>', unsafe_allow_html=True)
    query = st.text_input(
        "Rechercher",
        placeholder="Ex: Restaurant, Coiffeur, Plombier, Agence immobilière...",
        label_visibility="collapsed",
        key="query_input"
    )

with col2:
    st.markdown("""
    <div class="input-card">
        <div class="card-header">
            <div class="card-icon">📍</div>
            <h3 class="card-title">Localisation</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<p style="color: #1f2937; font-weight: 600; margin-bottom: 0.5rem; font-size: 1rem;">📍 Dans quelle ville ?</p>', unsafe_allow_html=True)
    city = st.text_input(
        "Ville",
        placeholder="Ex: Paris, Lyon, Marseille, Toulouse...",
        label_visibility="collapsed",
        key="city_input"
    )

# Slider pour le nombre de résultats
st.markdown("""
<div class="input-card">
    <div class="card-header">
        <div class="card-icon">🎯</div>
        <h3 class="card-title">Nombre de résultats souhaités</h3>
    </div>
</div>
""", unsafe_allow_html=True)
max_results = st.slider(
    "Résultats",
    min_value=1,
    max_value=50,
    value=10,
    label_visibility="collapsed"
)
st.markdown(f'<p style="background: #e0e7ff; border-left: 4px solid #667eea; padding: 1rem; border-radius: 8px; color: #1f2937; font-weight: 600; margin: 1rem 0;">📊 Vous allez rechercher <strong style="color: #667eea;">{max_results} businesses</strong> maximum</p>', unsafe_allow_html=True)

# Bouton de recherche
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    search_button = st.button("🚀 LANCER LA RECHERCHE", type="primary")
    
if search_button:
    if not query or not city:
        st.error("⚠️ Veuillez remplir tous les champs (activité et ville) !")
    else:
        # Conteneur de progression
        progress_container = st.container()
        
        with progress_container:
            st.markdown("""
            <div style="text-align: center; padding: 2rem; background: white; border-radius: 15px; margin: 2rem 0;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🔄</div>
                <div style="font-size: 1.3rem; font-weight: 700; color: #667eea;">
                    Recherche en cours...
                </div>
                <div style="color: #6b7280; margin-top: 0.5rem;">
                    Scan de Google Maps • Extraction des données • Enrichissement IA
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Simulation de progression
                for i in range(3):
                    progress_bar.progress((i + 1) * 33)
                    status_text.text(f"Étape {i+1}/3...")
                    
                # Recherche réelle
                businesses = search_local_business_full(query, city, max_results)
                progress_bar.progress(100)
                
                # Clear progression
                progress_container.empty()
                
                # Affichage des statistiques
                if businesses:
                    emails_count = sum(1 for b in businesses if b.get('email'))
                    phones_count = sum(1 for b in businesses if b.get('phone'))
                    avg_rating = sum(b.get('rating', 0) for b in businesses) / len(businesses) if businesses else 0
                    
                    st.markdown(f"""
                    <div class="stats-container">
                        <div class="stat-card">
                            <div class="stat-icon">✅</div>
                            <div class="stat-value">{len(businesses)}</div>
                            <div class="stat-label">Leads Trouvés</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-icon">📧</div>
                            <div class="stat-value">{emails_count}</div>
                            <div class="stat-label">Avec Email</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-icon">📱</div>
                            <div class="stat-value">{phones_count}</div>
                            <div class="stat-label">Avec Téléphone</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-icon">⭐</div>
                            <div class="stat-value">{avg_rating:.1f}</div>
                            <div class="stat-label">Note Moyenne</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Message de succès
                    st.markdown(f"""
                    <div class="success-box">
                        ✅ <strong>{len(businesses)} businesses</strong> enrichis et ajoutés à votre base de données !
                        <br>📊 Taux d'enrichissement : <strong>{(emails_count/len(businesses)*100):.0f}%</strong> emails
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Affichage du tableau
                    df = pd.DataFrame(businesses)[["name", "category", "city", "email", "phone", "rating", "reviews_count"]]
                    
                    st.markdown("""
                    <div style="background: white; padding: 2rem; border-radius: 20px; box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1); margin: 2rem 0;">
                        <h3 style="color: #1f2937; font-size: 1.5rem; font-weight: 700; margin-bottom: 1.5rem;">
                            📋 Résultats de la recherche
                        </h3>
                    """, unsafe_allow_html=True)
                    
                    st.dataframe(
                        df,
                        use_container_width=True,
                        height=400,
                        column_config={
                            "name": st.column_config.TextColumn("Nom", width="medium"),
                            "category": st.column_config.TextColumn("Catégorie", width="medium"),
                            "city": st.column_config.TextColumn("Ville", width="small"),
                            "email": st.column_config.TextColumn("Email", width="medium"),
                            "phone": st.column_config.TextColumn("Téléphone", width="small"),
                            "rating": st.column_config.NumberColumn("Note", format="⭐ %.1f"),
                            "reviews_count": st.column_config.NumberColumn("Avis", format="%d")
                        }
                    )
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Boutons d'action
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        csv = df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="📥 Télécharger CSV",
                            data=csv,
                            file_name=f"leads_{query}_{city}.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                    
                    with col2:
                        if st.button("📊 Voir le Dashboard", use_container_width=True):
                            st.switch_page("pages/2_📊_Dashboard.py")
                    
                    with col3:
                        if st.button("📧 Créer une Campagne", use_container_width=True):
                            st.switch_page("pages/3_📧_Campagnes.py")
                else:
                    st.warning("😕 Aucun résultat trouvé. Essayez avec d'autres mots-clés.")
                
            except Exception as e:
                progress_container.empty()
                st.error(f"❌ Erreur lors de la recherche : {str(e)}")
                st.info("💡 Conseil : Vérifiez votre connexion et réessayez")

# Section informative
st.markdown("""
<div class="info-section">
    <div class="card-header">
        <div class="card-icon">💡</div>
        <h3 class="card-title">Comment fonctionne notre système ?</h3>
    </div>
    <div class="info-grid">
        <div class="info-item">
            <div class="info-number">1</div>
            <div class="info-title">Recherche Intelligente</div>
            <div class="info-text">
                Notre IA scanne Google Maps et d'autres sources pour trouver 
                des businesses correspondant à vos critères
            </div>
        </div>
        <div class="info-item">
            <div class="info-number">2</div>
            <div class="info-title">Enrichissement Automatique</div>
            <div class="info-text">
                Extraction automatique des emails, téléphones, sites web 
                et réseaux sociaux pour chaque business
            </div>
        </div>
        <div class="info-item">
            <div class="info-number">3</div>
            <div class="info-title">Stockage Sécurisé</div>
            <div class="info-text">
                Tous vos leads sont sauvegardés dans votre base de données 
                personnelle et sécurisée
            </div>
        </div>
        <div class="info-item">
            <div class="info-number">4</div>
            <div class="info-title">Prêt à Contacter</div>
            <div class="info-text">
                Utilisez vos données pour créer des campagnes email 
                personnalisées et booster vos ventes
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Tips
st.markdown("""
<div style="background: linear-gradient(135deg, #667eea10 0%, #764ba210 100%); padding: 2rem; border-radius: 20px; margin-top: 2rem; border: 2px solid rgba(102, 126, 234, 0.2);">
    <h3 style="color: #1f2937; font-weight: 700; margin-bottom: 1rem;">💡 Conseils pour de meilleurs résultats</h3>
    <ul style="color: #4b5563; line-height: 1.8; font-size: 1rem;">
        <li><strong>Soyez précis</strong> : "Restaurant italien" plutôt que "Restaurant"</li>
        <li><strong>Testez plusieurs villes</strong> : Élargissez votre zone de recherche</li>
        <li><strong>Augmentez les résultats</strong> : Plus de leads = plus d'opportunités</li>
        <li><strong>Vérifiez les données</strong> : Tous les emails ne sont pas garantis à 100%</li>
    </ul>
</div>
""", unsafe_allow_html=True)