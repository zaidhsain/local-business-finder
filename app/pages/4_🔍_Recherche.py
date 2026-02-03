import streamlit as st
import sys
import os
import pandas as pd

# Ajouter le dossier parent au path pour que services soient trouvés
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.crud import get_all_business
from services.email_generator import generate_email
from services.email_sender import send_email

st.set_page_config(page_title="📧 Gestion Emails", layout="wide")
st.title("📧 Gestion des campagnes Email")

# -------------------------------
# Charger les leads depuis la DB
# -------------------------------
leads = get_all_business()
if not leads:
    st.warning("Aucun lead dans la base de données. Lancez d'abord une recherche.")
    st.stop()

df = pd.DataFrame(leads)

# -------------------------------
# Sélection du lead ou tous
# -------------------------------
st.header("Sélection des destinataires")
recipient_option = st.radio(
    "Envoyer à :",
    ("Tous les leads", "Un lead spécifique")
)

selected_leads = []

if recipient_option == "Tous les leads":
    selected_leads = df.to_dict('records')
else:
    lead_id = st.selectbox(
        "Sélectionnez un lead par ID",
        options=df['id'].tolist()
    )
    selected_leads = [df[df['id'] == lead_id].iloc[0].to_dict()]

# -------------------------------
# Génération du contenu email
# -------------------------------
st.header("Contenu de l'email")
subject = st.text_input("Objet de l'email", "Votre activité peut attirer plus de clients !")

default_body = generate_email()  # Génération IA (ou texte par défaut)
body = st.text_area("Corps de l'email", value=default_body, height=200)

# -------------------------------
# Bouton d'envoi
# -------------------------------
if st.button("📤 Envoyer les emails"):
    if not subject or not body:
        st.warning("Veuillez remplir l'objet et le corps de l'email.")
    else:
        sent_count = 0
        for lead in selected_leads:
            if lead.get("email"):
                try:
                    send_email(
                        to_email=lead["email"],
                        subject=subject,
                        body=body
                    )
                    sent_count += 1
                except Exception as e:
                    st.error(f"Erreur pour {lead['name']} : {e}")
            else:
                st.warning(f"{lead['name']} n'a pas d'email, impossible d'envoyer.")
        st.success(f"{sent_count} email(s) envoyés avec succès !")
