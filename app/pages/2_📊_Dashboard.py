import streamlit as st
import sys
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import io

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from services.crud import get_all_business, update_business, delete_business

# Configuration
st.set_page_config(
    page_title="Dashboard Analytics",
    page_icon="📊",
    layout="wide"
)

# CSS moderne avec design pro
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        background-attachment: fixed;
    }
    
    /* Hero Section moderne */
    .dashboard-hero {
        background: linear-gradient(135deg, #8f2027 0%, #203a43 50%, #2c5364 100%);
        padding: 3rem 2.5rem;
        border-radius: 25px;
        margin-bottom: 2.5rem;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .dashboard-hero::before {
        content: "";
        position: absolute;
        top: -50%;
        right: -10%;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(102,126,234,0.3) 0%, transparent 70%);
        border-radius: 50%;
    }
    
    .hero-content {
        position: relative;
        z-index: 1;
    }
    
    .hero-title {
        color: white;
        font-size: 3rem;
        font-weight: 900;
        margin: 0;
        background: linear-gradient(135deg, #ffffff 0%, #a8edea 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .hero-subtitle {
        color: rgba(55, 255, 255, 0.85);
        font-size: 1.3rem;
        margin-top: 0.8rem;
    }
    
    .hero-badge {
        display: inline-block;
        background: rgba(102, 126, 234, 0.2);
        color: white;
        padding: 0.5rem 1.5rem;
        border-radius: 50px;
        font-size: 0.9rem;
        font-weight: 600;
        margin-top: 1rem;
        border: 1px solid rgba(102, 126, 234, 0.4);
    }
    
    /* Metric Cards élégantes */
    .metrics-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .metric-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 5px 20px rgba(590, 0, 0, 0.08);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 15px 40px rgba(300, 0, 0, 0.12);
    }
    
    .metric-card::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    .metric-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 1.5rem;
    }
    
    .metric-icon {
        width: 50px;
        height: 50px;
        border-radius: 15px;
        background: linear-gradient(135deg, #667eea15 0%, #F64ba215 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.8rem;
    }
    
    .metric-trend {
        background: #10b98115;
        color: #10b981;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    .metric-trend.down {
        background: #ef444415;
        color: #ef4444;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 900;
        color: #1f2937;
        margin: 0.5rem 0;
        line-height: 1;
    }
    
    .metric-label {
        color: #1b7280;
        font-size: 0.95rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-sublabel {
        color: #6ca3af;
        font-size: 0.85rem;
        margin-top: 0.5rem;
    }
    
    /* Chart Cards */
    .chart-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
        margin: 1.5rem 0;
    }
    
    .chart-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid #f3f4f6;
    }
    
    .chart-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #9f2937;
        display: flex;
        align-items: center;
        gap: 0.8rem;
    }
    
    .chart-icon {
        font-size: 1.8rem;
    }
    
    .chart-options {
        display: flex;
        gap: 0.5rem;
    }
    
    .chart-badge {
        background: #f3f4f6;
        padding: 0.5rem 1rem;
        border-radius: 10px;
        font-size: 0.85rem;
        font-weight: 600;
        color: #6b7280;
    }
    
    /* Filter Section moderne */
    .filter-section {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
        margin-bottom: 2rem;
    }
    
    .filter-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid #93f4f6;
    }
    
    .filter-icon {
        width: 45px;
        height: 45px;
        border-radius: 12px;
        background: linear-gradient(135deg, #667eea 0%, #F64ba2 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        color: white;
    }
    
    .filter-title {
        font-size: 1.6rem;
        font-weight: 700;
        color: #9f2937;
    }
    
    /* Data Table moderne */
    .data-section {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
    }
    
    .data-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
    }
    
    .data-title {
        font-size: 1.6rem;
        font-weight: 700;
        color: #0f2937;
    }
    
    .data-count {
        background: linear-gradient(135deg, #667eea 0%, #F64ba2 100%);
        color: white;
        padding: 0.5rem 1.2rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
    }
    
    /* Action Bar */
    .action-bar {
        display: flex;
        gap: 1rem;
        margin-top: 2rem;
        flex-wrap: wrap;
    }
    
    .action-btn {
        flex: 1;
        min-width: 200px;
    }
    
    /* Success/Warning messages */
    .custom-success {
        background: #10b98115;
        border-left: 4px solid #10b981;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        color: #047857;
        font-weight: 600;
        margin: 1rem 0;
    }
    
    .custom-warning {
        background: #f59e0b15;
        border-left: 4px solid #359e0b;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        color: #f59e0b;
        font-weight: 600;
        margin: 1rem 0;
    }
    
    /* Quick Stats Bar */
    .quick-stats {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 1rem;
        background: rgba(102, 126, 234, 0.05);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1.5rem 0;
    }
    
    .quick-stat-item {
        text-align: center;
    }
    
    .quick-stat-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: #667eea;
    }
    
    .quick-stat-label {
        font-size: 0.85rem;
        color: #6b7280;
        margin-top: 0.3rem;
    }
</style>
""", unsafe_allow_html=True)

# Vérification connexion
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("🔐 Veuillez vous connecter pour accéder à cette page.")
    st.stop()

# Hero Section
st.markdown(f"""
<div class="dashboard-hero">
    <div class="hero-content">
        <h1 class="hero-title">📊 Dashboard Analytics</h1>
        <p class="hero-subtitle">Vue d'ensemble complète de votre prospection</p>
        <span class="hero-badge">🔄 Mis à jour en temps réel</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Chargement des données
leads = get_all_business()

if not leads:
    st.markdown("""
    <div style="text-align: center; padding: 5rem 2rem;">
        <div style="font-size: 5rem; margin-bottom: 1rem;">📭</div>
        <h2 style="color: #8b7280; font-size: 2rem; margin-bottom: 1rem;">Aucun lead pour le moment</h2>
        <p style="color: #0ca3af; font-size: 1.1rem;">Commencez par effectuer une recherche pour remplir votre base de données</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🔍 Lancer une recherche", type="primary", use_container_width=True):
        st.switch_page("pages/4_🔍_Recherche.py")
    st.stop()

df = pd.DataFrame(leads)

# Calcul des métriques
total_leads = len(df)
emails_count = df['email'].notna().sum()
phones_count = df['phone'].notna().sum()
avg_rating = df['rating'].mean() if 'rating' in df.columns and df['rating'].notna().any() else 0
enrichment_rate = (emails_count / total_leads * 100) if total_leads > 0 else 0

# Métriques principales avec tendances
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-header">
            <div class="metric-icon">👥</div>
            <div class="metric-trend">+12%</div>
        </div>
        <div class="metric-value">{total_leads:,}</div>
        <div class="metric-label">Leads Total</div>
        <div class="metric-sublabel">Base de données complète</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-header">
            <div class="metric-icon">📧</div>
            <div class="metric-trend">+8%</div>
        </div>
        <div class="metric-value">{emails_count:,}</div>
        <div class="metric-label">Avec Email</div>
        <div class="metric-sublabel">{enrichment_rate:.1f}% du total</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-header">
            <div class="metric-icon">📱</div>
            <div class="metric-trend">+15%</div>
        </div>
        <div class="metric-value">{phones_count:,}</div>
        <div class="metric-label">Avec Téléphone</div>
        <div class="metric-sublabel">{(phones_count/total_leads*100):.1f}% du total</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-header">
            <div class="metric-icon">⭐</div>
            <div class="metric-trend">+0.3</div>
        </div>
        <div class="metric-value">{avg_rating:.1f}</div>
        <div class="metric-label">Note Moyenne</div>
        <div class="metric-sublabel">Sur 5.0 étoiles</div>
    </div>
    """, unsafe_allow_html=True)

# Quick Stats supplémentaires
complete_profiles = df[(df['email'].notna()) & (df['phone'].notna())].shape[0]
unique_cities = df['city'].nunique() if 'city' in df.columns else 0
unique_categories = df['category'].nunique() if 'category' in df.columns else 0

st.markdown(f"""
<div class="quick-stats">
    <div class="quick-stat-item">
        <div class="quick-stat-value">{complete_profiles}</div>
        <div class="quick-stat-label">Profils Complets</div>
    </div>
    <div class="quick-stat-item">
        <div class="quick-stat-value">{unique_cities}</div>
        <div class="quick-stat-label">Villes</div>
    </div>
    <div class="quick-stat-item">
        <div class="quick-stat-value">{unique_categories}</div>
        <div class="quick-stat-label">Catégories</div>
    </div>
    <div class="quick-stat-item">
        <div class="quick-stat-value">{enrichment_rate:.0f}%</div>
        <div class="quick-stat-label">Enrichissement</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Graphiques
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("""
    <div class="chart-header">
        <div class="chart-title">
            <span class="chart-icon">🗺️</span>
            <span>Distribution Géographique</span>
        </div>
        <div class="chart-badge">Top 15 villes</div>
    </div>
    """, unsafe_allow_html=True)
    
    if 'city' in df.columns:
        city_counts = df['city'].value_counts().head(15)
        fig_city = px.bar(
            x=city_counts.values,
            y=city_counts.index,
            orientation='h',
            color=city_counts.values,
            color_continuous_scale=['#667eea', '#764ba2', '#f093fb'],
            labels={'x': 'Nombre de leads', 'y': 'Ville', 'color': 'Count'}
        )
        fig_city.update_layout(
            showlegend=False,
            height=450,
            margin=dict(l=0, r=0, t=0, b=0),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Arial, sans-serif", size=12, color="#275dc9")
        )
        fig_city.update_xaxes(showgrid=True, gridcolor='rgba(0,0,0,0.05)')
        st.plotly_chart(fig_city, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("""
    <div class="chart-header">
        <div class="chart-title">
            <span class="chart-icon">🏢</span>
            <span>Secteurs d'Activité</span>
        </div>
        <div class="chart-badge">Répartition</div>
    </div>
    """, unsafe_allow_html=True)
    
    if 'category' in df.columns:
        cat_counts = df['category'].value_counts().head(10)
        fig_cat = px.pie(
            values=cat_counts.values,
            names=cat_counts.index,
            color_discrete_sequence=px.colors.sequential.Plasma_r,
            hole=0.4
        )
        fig_cat.update_layout(
            height=450,
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Arial, sans-serif", size=12)
        )
        fig_cat.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>%{value} leads<br>%{percent}<extra></extra>'
        )
        st.plotly_chart(fig_cat, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Graphique de performance d'enrichissement
st.markdown('<div class="chart-card">', unsafe_allow_html=True)
st.markdown("""
<div class="chart-header">
    <div class="chart-title">
        <span class="chart-icon">📈</span>
        <span>Performance d'Enrichissement</span>
    </div>
    <div class="chart-badge">Taux de complétion</div>
</div>
""", unsafe_allow_html=True)

enrichment_data = pd.DataFrame({
    'Critère': ['Email', 'Téléphone', 'Site Web', 'Note'],
    'Disponible': [
        emails_count,
        phones_count,
        df['website'].notna().sum() if 'website' in df.columns else 0,
        df['rating'].notna().sum() if 'rating' in df.columns else 0
    ],
    'Total': [total_leads] * 4
})
enrichment_data['Pourcentage'] = (enrichment_data['Disponible'] / enrichment_data['Total'] * 100).round(1)

fig_enrichment = go.Figure()
fig_enrichment.add_trace(go.Bar(
    y=enrichment_data['Critère'],
    x=enrichment_data['Pourcentage'],
    orientation='h',
    marker=dict(
        color=enrichment_data['Pourcentage'],
        colorscale=[[0, '#ef4444'], [0.5, "#52390f"], [1, '#10b981']],
        line=dict(color='rgba(0,0,0,0.1)', width=1)
    ),
    text=enrichment_data['Pourcentage'].apply(lambda x: f'{x:.1f}%'),
    textposition='outside',
    hovertemplate='<b>%{y}</b><br>%{x:.1f}% disponible<extra></extra>'
))

fig_enrichment.update_layout(
    height=300,
    margin=dict(l=0, r=50, t=0, b=0),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(family="Arial, sans-serif", size=12, color="#2c5bb9"),
    xaxis=dict(range=[0, 105], showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
    yaxis=dict(showgrid=False)
)

st.plotly_chart(fig_enrichment, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Section Filtres
st.markdown('<div class="filter-section">', unsafe_allow_html=True)
st.markdown("""
<div class="filter-header">
    <div class="filter-icon">🔍</div>
    <h3 class="filter-title">Filtres Avancés</h3>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    cities = ["Toutes"] + sorted(df['city'].dropna().unique().tolist())
    city_filter = st.selectbox("📍 Ville", cities, key="city_filter")

with col2:
    categories = ["Toutes"] + sorted(df['category'].dropna().unique().tolist())
    category_filter = st.selectbox("🏢 Catégorie", categories, key="cat_filter")

with col3:
    has_email = st.selectbox("📧 Email", ["Tous", "Avec email", "Sans email"], key="email_filter")

with col4:
    has_phone = st.selectbox("📱 Téléphone", ["Tous", "Avec téléphone", "Sans téléphone"], key="phone_filter")

st.markdown('</div>', unsafe_allow_html=True)

# Application des filtres
df_filtered = df.copy()

if city_filter != "Toutes":
    df_filtered = df_filtered[df_filtered['city'] == city_filter]

if category_filter != "Toutes":
    df_filtered = df_filtered[df_filtered['category'] == category_filter]

if has_email == "Avec email":
    df_filtered = df_filtered[df_filtered['email'].notna()]
elif has_email == "Sans email":
    df_filtered = df_filtered[df_filtered['email'].isna()]

if has_phone == "Avec téléphone":
    df_filtered = df_filtered[df_filtered['phone'].notna()]
elif has_phone == "Sans téléphone":
    df_filtered = df_filtered[df_filtered['phone'].isna()]

# Tableau de données
st.markdown('<div class="data-section">', unsafe_allow_html=True)
st.markdown(f"""
<div class="data-header">
    <h3 class="data-title">📋 Base de Données</h3>
    <span class="data-count">{len(df_filtered)} résultats</span>
</div>
""", unsafe_allow_html=True)

# Configuration des colonnes pour l'éditeur
column_config = {
    "id": st.column_config.NumberColumn("ID", width="small", disabled=True),
    "name": st.column_config.TextColumn("Nom", width="medium"),
    "email": st.column_config.TextColumn("Email", width="medium"),
    "phone": st.column_config.TextColumn("Téléphone", width="small"),
    "city": st.column_config.TextColumn("Ville", width="small"),
    "category": st.column_config.TextColumn("Catégorie", width="medium"),
    "rating": st.column_config.NumberColumn("Note", format="⭐ %.1f", width="small"),
    "website": st.column_config.LinkColumn("Site Web", width="small")
}

edited_df = st.data_editor(
    df_filtered,
    num_rows="dynamic",
    use_container_width=True,
    hide_index=True,
    column_config=column_config,
    key="data_editor"
)

# Actions
st.markdown('<div class="action-bar">', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("💾 Sauvegarder", use_container_width=True, type="primary"):
        try:
            for idx, row in edited_df.iterrows():
                update_business(row['id'], row.to_dict())
            st.markdown('<div class="custom-success">✅ Modifications sauvegardées avec succès !</div>', unsafe_allow_html=True)
            st.rerun()
        except Exception as e:
            st.error(f"❌ Erreur: {e}")

with col2:
    csv = edited_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Exporter CSV",
        data=csv,
        file_name=f"leads_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        use_container_width=True
    )

with col3:
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
        edited_df.to_excel(writer, index=False, sheet_name='Leads')
    excel_buffer.seek(0)
    
    st.download_button(
        label="📊 Exporter Excel",
        data=excel_buffer,
        file_name=f"leads_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

with col4:
    with st.popover("🗑️ Supprimer", use_container_width=True):
        st.write("⚠️ Supprimer un lead")
        delete_id = st.number_input("ID du lead", min_value=1, step=1, key="delete_id")
        if st.button("Confirmer la suppression", type="secondary"):
            try:
                delete_business(delete_id)
                st.success(f"Lead {delete_id} supprimé !")
                st.rerun()
            except Exception as e:
                st.error(f"Erreur: {e}")

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Import nécessaire pour Excel
import io