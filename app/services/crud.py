from services.database import get_connection
from config.logger import logger

# Ajouter un business
def add_business(data: dict):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        INSERT INTO business (
            name, category, phone, email, website, rating, reviews_count, city, score_ai, recommendation, source_url
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get("name"),
            data.get("category"),
            data.get("phone"),
            data.get("email"),
            data.get("website"),
            data.get("rating"),
            data.get("reviews_count"),
            data.get("city"),
            data.get("score_ai"),
            data.get("recommendation"),
            data.get("source_url")
        ))
        conn.commit()
        logger.info(f"Business ajouté : {data.get('name')}")
    except Exception as e:
        logger.error(f"Erreur insertion business : {e}")
    finally:
        conn.close()

# Lire tous les business
def get_all_business():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM business")

    columns = [description[0] for description in cursor.description]
    rows = cursor.fetchall()

    conn.close()
    return [dict(zip(columns, row)) for row in rows]

# update_business
def update_business(lead_id: int, fields: dict):
    """
    fields = {"email": "nouvel@email.com", "phone": "0612345678"}
    """
    conn = get_connection()
    cursor = conn.cursor()

    set_clause = ", ".join([f"{k} = ?" for k in fields.keys()])
    values = list(fields.values())
    values.append(lead_id)

    query = f"UPDATE business SET {set_clause} WHERE id = ?"  # <-- changer 'leads' en 'business'
    cursor.execute(query, values)
    conn.commit()
    conn.close()

# delete_business
def delete_business(lead_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM business WHERE id = ?", (lead_id,))  # <-- changer 'leads' en 'business'
    conn.commit()
    conn.close()
