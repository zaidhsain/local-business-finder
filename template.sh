#!/bin/bash

# Création des dossiers principaux
mkdir -p app/pages
mkdir -p app/services
mkdir -p app/assets/images
mkdir -p config
mkdir -p .streamlit
mkdir -p data
mkdir -p logs

# Création des fichiers dans app/
touch app/Accueil.py
touch app/styles.py

# Création des fichiers dans app/pages/
touch app/pages/1_🔐_Login.py
touch app/pages/2_📊_Dashboard.py
touch app/pages/3_📧_Emails.py
touch app/pages/4_🔍_Recherche.py
touch app/pages/_Admin.py

# Création des fichiers dans app/services/
touch app/services/auth.py
touch app/services/admin_service.py
touch app/services/quota_manager.py
touch app/services/discovery.py
touch app/services/crawler.py
touch app/services/llm_extractor.py
touch app/services/database.py
touch app/services/crud.py
touch app/services/email_generator.py
touch app/services/email_sender.py

# Création des fichiers dans config/
touch config/settings.py
touch config/logger.py

# Création du fichier Streamlit config
touch .streamlit/config.toml

# Création des fichiers data et logs
touch data/leads_database.db
touch logs/app.log

# Création des fichiers à la racine
touch .env
touch .env.example
touch requirements.txt
touch README.md

echo "Architecture complétée avec succès dans ton projet existant !"
