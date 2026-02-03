import sqlite3
from config.settings import DB_PATH
from config.logger import logger

def get_connection():
    return sqlite3.connect(DB_PATH)

def create_tables():
    """
    Crée les tables nécessaires pour l'application :
    - business : pour stocker les leads
    - users : pour stocker les utilisateurs (login)
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # -------------------------
        # Table business
        # -------------------------
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS business (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            category TEXT,
            phone TEXT,
            email TEXT,
            website TEXT,
            rating REAL,
            reviews_count INTEGER,
            city TEXT,
            score_ai REAL,
            recommendation TEXT,
            source_url TEXT UNIQUE
        )
        """)

        # -------------------------
        # Table users (login)
        # -------------------------
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
        """)

        # Commit uniquement après toutes les opérations
        conn.commit()
        logger.info("Tables créées avec succès !")
    except Exception as e:
        logger.error(f"Erreur création tables: {e}")
    finally:
        # Fermer la connexion à la fin seulement
        conn.close()
