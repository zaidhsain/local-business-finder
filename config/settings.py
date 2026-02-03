# config/settings.py
import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = "Local Business Finder AI"
APP_VERSION = "0.1.0"

# Limits
MAX_RESULTS = 25

# APIs
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Paths
DB_PATH = "data/leads_database.db"
LOG_PATH = "logs/app.log"
# app/config/settings.py

# SMTP Email
EMAIL_HOST = "smtp.gmail.com"  # ou smtp.brevo.com
EMAIL_PORT = 587
EMAIL_USER = "zaidhsain2@gmail.com"
EMAIL_PASS = "Temara2005"
