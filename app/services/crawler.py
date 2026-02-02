import requests
from bs4 import BeautifulSoup
import re
from config.logger import logger

def extract_email_phone(website_url: str):
    """
    Extrait email et téléphone depuis un site web.
    """
    result = {"email": None, "phone": None}
    if not website_url:
        return result

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(website_url, headers=headers, timeout=5)
        soup = BeautifulSoup(r.text, "html.parser")
        text = soup.get_text()

        # Emails
        emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
        result["email"] = emails[0] if emails else None

        # Téléphone (ex: +212 6 00 00 00 00)
        phones = re.findall(r"(\+?\d[\d\s\-]{7,}\d)", text)
        result["phone"] = phones[0] if phones else None

        return result

    except Exception as e:
        logger.error(f"Erreur crawler.py pour {website_url} : {e}")
        return result
