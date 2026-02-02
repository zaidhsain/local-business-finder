# services/discovery.py
from services.crud import add_business
from services.crawler import extract_email_phone
from services.llm_extractor import score_business
from services.google_maps import search_local_business  # <-- plus de circular import
from config.logger import logger

def search_local_business_full(query: str, city: str, max_results: int = 5):
    """
    Pipeline complet :
    1. Recherche business Google Maps
    2. Scraping email / phone depuis le site web
    3. Scoring IA + recommandation
    4. Sauvegarde dans DB
    """
    enriched_results = []

    # 1️⃣ Recherche Google Maps
    basic_results = search_local_business(query, city, max_results)

    for b in basic_results:
        # 2️⃣ Scraper email / téléphone
        scraped = extract_email_phone(b.get("website"))
        b["email"] = scraped.get("email")
        b["phone"] = scraped.get("phone")

        # 3️⃣ Score IA + recommandation
        score, reco = score_business(
            b["name"],
            b["category"],
            b["rating"],
            b["reviews_count"]
        )
        b["score_ai"] = score
        b["recommendation"] = reco

        # 4️⃣ Ajouter ou mettre à jour dans la DB
        add_business(b)

        enriched_results.append(b)

    logger.info(f"{len(enriched_results)} business enrichis et ajoutés à la DB")
    return enriched_results
