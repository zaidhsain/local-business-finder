import streamlit as st
import sys
import os
import pandas as pd

# Ajouter le dossier parent
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from services.database import get_connection
from services.auth import create_user
from services.crud import get_all_business

# -------------------------------
# Sécurité : accès admin seulement
# -------------------------------
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("⛔ Accès refusé. Veuillez vous connecter.")
    st.stop()

# ⚠️ Ici on considère que seul "admin" est admin
if st.session_state.username != "admin":
    st.error("⛔ Accès réservé à l'administrateur.")
    st.stop()

st.title("⚙️ Administration")

# -------------------------------
# 📊 STATISTIQUES
# -------------------------------
st.header("📊 Statistiques générales")

conn = get_connection()
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM business")
total_leads = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM users")
total_users = cursor.fetchone()[0]

conn.close()

col1, col2 = st.columns(2)
col1.metric("📌 Total Leads", total_leads)
col2.metric("👤 Total Utilisateurs", total_users)

# -------------------------------
# 👤 GESTION DES UTILISATEURS
# -------------------------------
st.header("👤 Gestion des utilisateurs")

conn = get_connection()
users_df = pd.read_sql_query("SELECT id, username FROM users", conn)
conn.close()

st.dataframe(users_df, use_container_width=True)

# -------------------------------
# ➕ CRÉER UN UTILISATEUR
# -------------------------------
st.subheader("➕ Créer un nouvel utilisateur")

new_username = st.text_input("Nom d'utilisateur")
new_password = st.text_input("Mot de passe", type="password")

if st.button("Créer utilisateur"):
    if not new_username or not new_password:
        st.warning("Veuillez remplir tous les champs")
    else:
        create_user(new_username, new_password)
        st.success(f"Utilisateur `{new_username}` créé avec succès")
        st.rerun()

# -------------------------------
# ❌ SUPPRIMER UN UTILISATEUR
# -------------------------------
st.subheader("❌ Supprimer un utilisateur")

user_id_to_delete = st.number_input(
    "ID utilisateur à supprimer",
    min_value=1,
    step=1
)

if st.button("Supprimer utilisateur"):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id_to_delete,))
    conn.commit()
    conn.close()
    st.success("Utilisateur supprimé")
    st.rerun()

# -------------------------------
# 📁 EXPORT LEADS
# -------------------------------
st.header("📁 Export des leads")

leads = get_all_business()
if leads:
    df = pd.DataFrame(leads)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Télécharger tous les leads (CSV)",
        csv,
        "all_leads.csv",
        "text/csv"
    )
else:
    st.info("Aucun lead disponible")
