import streamlit as st
import sys
import os
import pandas as pd

# Ajouter dossier parent au path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from services.crud import get_all_business, update_business, delete_business
import streamlit as st

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("🔐 Veuillez vous connecter pour accéder à cette page.")
    st.stop()  # Arrête le reste de la page


st.title("📊 Dashboard des leads")

# 1️⃣ Charger les données
leads = get_all_business()
df = pd.DataFrame(leads)

# Si la DB est vide, créer les colonnes pour éviter KeyError



# 2️⃣ Filtres
city_filter = st.selectbox(
    "Filtrer par ville",
    options=["Toutes"] + df['city'].dropna().unique().tolist()
)
activity_filter = st.selectbox(
    "Filtrer par activité",
    options=["Toutes"] + df['category'].dropna().unique().tolist()
)

df_filtered = df.copy()
if city_filter != "Toutes":
    df_filtered = df_filtered[df_filtered['city'] == city_filter]
if activity_filter != "Toutes":
    df_filtered = df_filtered[df_filtered['category'] == activity_filter]

# 3️⃣ Tableau interactif
st.write("💡 Double-cliquez sur une cellule pour modifier (ex: email, téléphone)")
edited_df = st.data_editor(
    df_filtered,
    num_rows="dynamic",
    use_container_width=True
)

# 4️⃣ Détecter les changements et sauvegarder
if st.button("💾 Sauvegarder les modifications"):
    for idx, row in edited_df.iterrows():
        lead_id = row['id']
        fields_to_update = {
            "name": row["name"],
            "category": row["category"],
            "email": row["email"],
            "phone": row["phone"],
            "website": row["website"],
            "city": row["city"]
        }
        update_business(lead_id, fields_to_update)
    st.success("Modifications sauvegardées !")
    st.experimental_rerun()

# 5️⃣ Supprimer un lead
delete_id = st.number_input("ID du lead à supprimer", min_value=1, step=1)
if st.button("❌ Supprimer lead"):
    delete_business(delete_id)
    st.success(f"Lead {delete_id} supprimé !")
    st.experimental_rerun()

# 6️⃣ Export CSV filtré
csv = edited_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Télécharger CSV filtré",
    data=csv,
    file_name="leads_dashboard.csv",
    mime="text/csv"
)

