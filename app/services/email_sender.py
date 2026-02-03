import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config.settings import EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASS
from config.logger import logger

def send_email(to_email: str, subject: str, body: str):
    """
    Envoie un email simple via SMTP
    """
    try:
        # Création du message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        # Connexion au serveur SMTP
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()  # sécurité TLS
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        server.quit()

        logger.info(f"Email envoyé à {to_email} avec succès !")
        return True
    except Exception as e:
        logger.error(f"Erreur envoi email à {to_email}: {e}")
        return False
