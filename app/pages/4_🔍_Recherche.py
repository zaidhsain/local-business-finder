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
    /* Fond dégradé */
    .stApp {
        background: linear-gradient(to bottom right, #f0f4ff, #e6f2ff);
    }
    
    /* Header avec icône 3D */
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        text-align: center;
    }
    
    .header-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
    
    .header-title {
        color: white;
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .header-subtitle {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.2rem;
        margin-top: 0.5rem;
    }
    
    /* Cards pour les inputs */
    .input-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
    }
    
    .card-header {
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
    }
    
    .card-icon {
        font-size: 2rem;
        margin-right: 1rem;
    }
    
    .card-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #1f2937;
    }
    
    /* Bouton principal */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 1.2rem 2rem;
        font-size: 1.2rem;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 10px 25px rgba(16, 185, 129, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 35px rgba(16, 185, 129, 0.5);
    }
    
    /* Stats cards */
    .stats-container {
        display: flex;
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .stat-card {
        flex: 1;
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
    
    .stat-value {
        font-size: 2rem;
        font-weight: 800;
        color: #667eea;
    }
    
    .stat-label {
        color: #6b7280;
        font-size: 0.9rem;
        margin-top: 0.3rem;
    }
    
    /* Tableau stylisé */
    .dataframe {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
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
    <div class="header-icon">🔍</div>
    <h1 class="header-title">Recherche Business Locale</h1>
    <p class="header-subtitle">Trouvez et enrichissez vos prospects en quelques clics</p>
</div>
""", unsafe_allow_html=True)

# Section de recherche
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="input-card">
        <div class="card-header">
            <span class="card-icon">🏢</span>
            <h3 class="card-title">Type d'activité</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)
    query = st.text_input("", placeholder="Ex: Restaurant, Coiffeur, Plombier...", label_visibility="collapsed")

with col2:
    st.markdown("""
    <div class="input-card">
        <div class="card-header">
            <span class="card-icon">📍</span>
            <h3 class="card-title">Localisation</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)
    city = st.text_input("", placeholder="Ex: Paris, Lyon, Marseille...", label_visibility="collapsed", key="city")

# Slider pour le nombre de résultats
st.markdown("""
<div class="input-card">
    <div class="card-header">
        <span class="card-icon">🎯</span>
        <h3 class="card-title">Nombre de résultats souhaités</h3>
    </div>
</div>
""", unsafe_allow_html=True)
max_results = st.slider("", 1, 25, 10, label_visibility="collapsed")

# Bouton de recherche
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🚀 LANCER LA RECHERCHE"):
        if not query or not city:
            st.warning("⚠️ Veuillez remplir tous les champs !")
        else:
            with st.spinner("🔄 Recherche en cours..."):
                try:
                    businesses = search_local_business_full(query, city, max_results)
                    
                    # Affichage des statistiques
                    st.markdown(f"""
                    <div class="stats-container">
                        <div class="stat-card">
                            <div class="stat-icon">✅</div>
                            <div class="stat-value">{len(businesses)}</div>
                            <div class="stat-label">Leads trouvés</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-icon">📧</div>
                            <div class="stat-value">{sum(1 for b in businesses if b.get('email'))}</div>
                            <div class="stat-label">Avec email</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-icon">📱</div>
                            <div class="stat-value">{sum(1 for b in businesses if b.get('phone'))}</div>
                            <div class="stat-label">Avec téléphone</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-icon">⭐</div>
                            <div class="stat-value">{sum(b.get('rating', 0) for b in businesses) / len(businesses) if businesses else 0:.1f}</div>
                            <div class="stat-label">Note moyenne</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Affichage du tableau
                    if businesses:
                        st.success(f"✅ {len(businesses)} business enrichis et ajoutés à la base de données !")
                        df = pd.DataFrame(businesses)[["name", "category", "city", "email", "phone", "rating", "reviews_count"]]
                        st.dataframe(df, use_container_width=True, height=400)
                        
                        # Bouton de téléchargement
                        csv = df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="📥 Télécharger les résultats (CSV)",
                            data=csv,
                            file_name=f"leads_{query}_{city}.csv",
                            mime="text/csv"
                        )
                    
                except Exception as e:
                    st.error(f"❌ Erreur : {e}")

# Section informative
st.markdown("""
<div class="input-card" style="margin-top: 3rem;">
    <div class="card-header">
        <span class="card-icon">💡</span>
        <h3 class="card-title">Comment ça marche ?</h3>
    </div>
    <ol style="color: #4b5563; font-size: 1rem; line-height: 1.8;">
        <li><strong>Recherche intelligente</strong> : Nous scannons Google Maps et autres sources</li>
        <li><strong>Enrichissement automatique</strong> : Emails, téléphones et infos détaillées</li>
        <li><strong>Stockage sécurisé</strong> : Vos leads sont sauvegardés dans votre base</li>
        <li><strong>Prêt à contacter</strong> : Utilisez les données pour vos campagnes</li>
    </ol>
</div>
""", unsafe_allow_html=True)