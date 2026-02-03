import hashlib
from services.database import get_connection
from config.logger import logger

# Hasher le mot de passe
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# Vérifier si un utilisateur existe et mot de passe correct
def verify_user(username: str, password: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        if row:
            stored_hash = row[0]
            return stored_hash == hash_password(password)
        return False
    except Exception as e:
        logger.error(f"Erreur vérification utilisateur: {e}")
        return False
    finally:
        conn.close()

# Créer un utilisateur (admin par défaut)
def create_user(username: str, password: str):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            return  # utilisateur existe déjà
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hash_password(password))
        )
        conn.commit()
        logger.info(f"Utilisateur créé: {username}")
    except Exception as e:
        logger.error(f"Erreur création utilisateur: {e}")
    finally:
        conn.close()
