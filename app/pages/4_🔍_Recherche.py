import streamlit as st

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("🔐 Veuillez vous connecter pour accéder à cette page.")
    st.stop()  # Arrête le reste de la page
import streamlit as st
import sys, os
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.crud import get_all_business

st.title("🔍 Recherche de leads")

# Récupérer les leads
leads = get_all_business()
df = pd.DataFrame(leads)

# Filtres
name_filter = st.text_input("Nom du business")
city_filter = st.text_input("Ville")
category_filter = st.text_input("Catégorie")

df_filtered = df.copy()
if name_filter:
    df_filtered = df_filtered[df_filtered['name'].str.contains(name_filter, case=False)]
if city_filter:
    df_filtered = df_filtered[df_filtered['city'].str.contains(city_filter, case=False)]
if category_filter:
    df_filtered = df_filtered[df_filtered['category'].str.contains(category_filter, case=False)]

st.dataframe(df_filtered)
