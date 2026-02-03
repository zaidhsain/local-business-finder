import streamlit as st
import sys, os
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.crud import get_all_business
from services.email_generator import generate_email
from services.email_sender import send_email

st.title("📧 Campaign Manager")

# Récupérer les leads avec email
leads = get_all_business()
df = pd.DataFrame(leads)
df_emails = df[df['email'].notnull() & (df['email'] != "")]

st.dataframe(df_emails)

# Sélection lead
selected_idx = st.selectbox("Sélectionnez un lead pour envoyer un email", df_emails.index)

# Générer email
if st.button("✍️ Générer email IA"):
    lead = df_emails.loc[selected_idx]
    subject, body = generate_email(lead['name'], lead['category'])
    st.write("Objet :", subject)
    st.write("Contenu :", body)

    if st.button("📤 Envoyer email"):
        send_email(lead['email'], subject, body)
        st.success(f"Email envoyé à {lead['email']}")
