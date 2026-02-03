import streamlit as st
import sys
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from services.crud import get_all_business, update_business, delete_business

# Configuration
st.set_page_config(
    page_title="Dashboard Analytics",
    page_icon="📊",
    layout="wide"
)

# CSS moderne avec design dashbord
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Hero Section */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 25px;
        margin-bottom: 2rem;
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .hero-section::before {
        content: "📊";
        position: absolute;
        right: 2rem;
        top: 50%;
        transform: translateY(-50%);
        font-size: 8rem;
        opacity: 0.2;
    }
    
    .hero-title {
        color: white;
        font-size: 2.8rem;
        font-weight: 900;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .hero-subtitle {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.3rem;
        margin-top: 0.5rem;
    }
    
    /* Metric Cards */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .metric-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15);
    }
    
    .metric-card::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 5px;
        height: 100%;
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    .metric-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #1f2937;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        color: #6b7280;
        font-size: 1rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Filter Section */
    .filter-section {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
    }
    
    .filter-header {
        display: flex;
        align-items: center;
        margin-bottom: 1.5rem;
    }
    
    .filter-icon {
        font-size: 2rem;
        margin-right: 1rem;
    }
    
    .filter-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1f2937;
    }
    
    /* Data Table */
    .data-section {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
    }
    
    /* Action Buttons */
    .action-buttons {
        display: flex;
        gap: 1rem;
        margin-top: 2rem;
    }
    
    .stButton > button {
        border-radius: 12px;
        padding: 0.8rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    /* Charts */
    .chart-container {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
        margin: 1.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Vérification connexion
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("🔐 Veuillez vous connecter pour accéder à cette page.")
    st.stop()

# Hero Section
st.markdown(f"""
<div class="hero-section">
    <h1 class="hero-title">Dashboard Analytics</h1>
    <p class="hero-subtitle">Visualisez et gérez vos leads en temps réel</p>
</div>
""", unsafe_allow_html=True)

# Chargement des données
leads = get_all_business()

if not leads:
    st.info("📭 Aucun lead dans votre base. Commencez par une recherche !")
    st.stop()

df = pd.DataFrame(leads)

# Métriques principales
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <span class="metric-icon">👥</span>
        <div class="metric-value">{len(df)}</div>
        <div class="metric-label">Total Leads</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    emails_count = df['email'].notna().sum()
    st.markdown(f"""
    <div class="metric-card">
        <span class="metric-icon">📧</span>
        <div class="metric-value">{emails_count}</div>
        <div class="metric-label">Avec Email</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    phones_count = df['phone'].notna().sum()
    st.markdown(f"""
    <div class="metric-card">
        <span class="metric-icon">📱</span>
        <div class="metric-value">{phones_count}</div>
        <div class="metric-label">Avec Téléphone</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    avg_rating = df['rating'].mean() if 'rating' in df.columns else 0
    st.markdown(f"""
    <div class="metric-card">
        <span class="metric-icon">⭐</span>
        <div class="metric-value">{avg_rating:.1f}</div>
        <div class="metric-label">Note Moyenne</div>
    </div>
    """, unsafe_allow_html=True)

# Graphiques
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("🗺️ Répartition par ville")
    
    if 'city' in df.columns:
        city_counts = df['city'].value_counts().head(10)
        fig_city = px.bar(
            x=city_counts.values,
            y=city_counts.index,
            orientation='h',
            color=city_counts.values,
            color_continuous_scale='Viridis',
            labels={'x': 'Nombre de leads', 'y': 'Ville'}
        )
        fig_city.update_layout(
            showlegend=False,
            height=400,
            margin=dict(l=0, r=0, t=0, b=0)
        )
        st.plotly_chart(fig_city, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("🏢 Top catégories")
    
    if 'category' in df.columns:
        cat_counts = df['category'].value_counts().head(10)
        fig_cat = px.pie(
            values=cat_counts.values,
            names=cat_counts.index,
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        fig_cat.update_layout(
            height=400,
            margin=dict(l=0, r=0, t=0, b=0)
        )
        st.plotly_chart(fig_cat, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Section Filtres
st.markdown('<div class="filter-section">', unsafe_allow_html=True)
st.markdown("""
<div class="filter-header">
    <span class="filter-icon">🔍</span>
    <h3 class="filter-title">Filtres avancés</h3>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    cities = ["Toutes"] + sorted(df['city'].dropna().unique().tolist())
    city_filter = st.selectbox("📍 Ville", cities)

with col2:
    categories = ["Toutes"] + sorted(df['category'].dropna().unique().tolist())
    category_filter = st.selectbox("🏢 Catégorie", categories)

with col3:
    has_email = st.selectbox("📧 Avec email", ["Tous", "Oui", "Non"])

st.markdown('</div>', unsafe_allow_html=True)

# Application des filtres
df_filtered = df.copy()

if city_filter != "Toutes":
    df_filtered = df_filtered[df_filtered['city'] == city_filter]

if category_filter != "Toutes":
    df_filtered = df_filtered[df_filtered['category'] == category_filter]

if has_email == "Oui":
    df_filtered = df_filtered[df_filtered['email'].notna()]
elif has_email == "Non":
    df_filtered = df_filtered[df_filtered['email'].isna()]

# Tableau de données
st.markdown('<div class="data-section">', unsafe_allow_html=True)
st.subheader(f"📋 Leads ({len(df_filtered)} résultats)")

edited_df = st.data_editor(
    df_filtered,
    num_rows="dynamic",
    use_container_width=True,
    hide_index=True,
    column_config={
        "id": st.column_config.NumberColumn("ID", width="small"),
        "name": st.column_config.TextColumn("Nom", width="medium"),
        "email": st.column_config.TextColumn("Email", width="medium"),
        "phone": st.column_config.TextColumn("Téléphone", width="small"),
        "rating": st.column_config.NumberColumn("Note", format="⭐ %.1f"),
    }
)

# Actions
col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    if st.button("💾 Sauvegarder les modifications", use_container_width=True):
        for idx, row in edited_df.iterrows():
            update_business(row['id'], row.to_dict())
        st.success("✅ Modifications sauvegardées !")
        st.rerun()

with col2:
    csv = edited_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Exporter en CSV",
        data=csv,
        file_name="leads_export.csv",
        mime="text/csv",
        use_container_width=True
    )

with col3:
    delete_id = st.number_input("ID à supprimer", min_value=1, step=1)
    if st.button("🗑️ Supprimer"):
        delete_business(delete_id)
        st.success(f"Lead {delete_id} supprimé !")
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)