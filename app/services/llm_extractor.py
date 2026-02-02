import os
import google.generativeai as genai
from config.settings import GEMINI_API_KEY
from config.logger import logger

# Initialiser Gemini
genai.configure(api_key=GEMINI_API_KEY)

def score_business(name, category, rating, reviews_count):
    """
    Analyse le business et retourne un score IA et une recommandation
    """
    try:
        prompt = f"""
        Analyse ce business :
        Nom : {name}
        Catégorie : {category}
        Note Google : {rating}
        Nombre d'avis : {reviews_count}

        Donne :
        1. Un score potentiel (0-100)
        2. Une recommandation courte pour marketing ou contact commercial
        Réponse au format JSON : {{ "score_ai": XX, "recommendation": "texte" }}
        """

        response = genai.generate_text(
            model="text-bison-001",
            prompt=prompt,
            max_output_tokens=200
        )

        # Exemple : parse JSON dans response.text
        import json
        data = json.loads(response.text)
        return data["score_ai"], data["recommendation"]

    except Exception as e:
        logger.error(f"Erreur llm_extractor.py : {e}")
        return None, None
