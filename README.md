# 🗺️ Local Business Finder AI

Une application **IA & Data** qui permet de :
- Rechercher des business locaux depuis Google Maps
- Extraire automatiquement email & téléphone depuis leurs sites web
- Évaluer chaque business avec un score IA
- Gérer et exporter les leads via un dashboard interactif

---

## 🚀 Fonctionnalités

### 🔍 Recherche Business
- Recherche par activité et ville
- Basée sur Google Maps
- Récupération : nom, catégorie, site web, note, avis

### 🌐 Scraping Automatique
- Extraction d’emails et numéros de téléphone
- Analyse des sites web officiels

### 🤖 Scoring IA
- Score IA basé sur :
  - Note Google
  - Nombre d’avis
  - Catégorie du business
- Recommandation automatique (bon / moyen / mauvais lead)

### 📊 Dashboard Leads
- Filtres par ville et activité
- Édition directe (email, téléphone, etc.)
- Suppression de leads
- Export CSV

---

## 🏗️ Architecture du Projet

local-business-finder/
│
├── app/
│ ├── Accueil.py # Page principale Streamlit
│ ├── pages/
│ │ └── 2_📊_Dashboard.py # Dashboard des leads
│ │
│ ├── services/
│ │ ├── discovery.py # Pipeline complet
│ │ ├── crawler.py # Scraping email / phone
│ │ ├── llm_extractor.py # Scoring IA
│ │ ├── crud.py # CRUD DB
│ │ └── database.py # Connexion SQLite
│ │
│ ├── config/
│ │ ├── settings.py # Config globale
│ │ └── logger.py # Logs
│
├── data/
│ └── business.db # Base SQLite
│
├── requirements.txt
├── README.md
└── .gitignore


---

## ⚙️ Installation

### 1️⃣ Cloner le projet
```bash
git clone https://github.com/ton-username/local-business-finder.git
cd local-business-finder
2️⃣ Créer un environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Linux / Mac
.venv\Scripts\activate     # Windows
3️⃣ Installer les dépendances
pip install -r requirements.txt
🔑 Configuration
config/settings.py
APP_NAME = "Local Business Finder AI"
APP_VERSION = "1.0.0"
DB_PATH = "data/business.db"
⚠️ (Optionnel)
Ajouter une API Key Google Maps si nécessaire.

▶️ Lancer l’application
streamlit run app/Accueil.py
Puis ouvrir :

http://localhost:8501
🧠 Pipeline Global
Recherche Google Maps
        ↓
Scraping email / phone
        ↓
Scoring IA + recommandation
        ↓
Sauvegarde en base SQLite
        ↓
Dashboard Streamlit
🧪 Technologies Utilisées
Python

Streamlit

SQLite

Pandas

BeautifulSoup / Requests

Google Maps API

IA / règles intelligentes

📈 Cas d’Utilisation
Génération de leads

Prospection commerciale

Analyse business locale

Automatisation marketing

Freelance / Startup

🔮 Améliorations Futures
Authentification utilisateur

Export Excel / CRM

Intégration WhatsApp / Email

Scoring IA avec LLM (GPT)

Déploiement cloud (Render, Railway)

👨‍💻 Auteur
Zaid Hsain
Étudiant en IA & Data Science
 ENSAM Rabat 🇲🇦

⭐ Support
Si le projet t’aide :
👉 laisse une ⭐ sur GitHub
👉 partage-le 🙌
