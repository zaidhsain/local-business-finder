import sqlite3
from config.settings import DB_PATH
from config.logger import logger

def get_connection():
    try:
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        return conn
    except Exception as e:
        logger.error(f"Erreur connexion DB : {e}")
        return None

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
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
        source_url TEXT UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()
    logger.info("Table business créée (si elle n'existait pas)")
