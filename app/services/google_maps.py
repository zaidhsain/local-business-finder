# services/google_maps.py
import requests
from config.settings import GOOGLE_MAPS_API_KEY
from services.crud import add_business
from config.logger import logger

GOOGLE_MAPS_PLACES_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"

def search_local_business(query: str, city: str, max_results: int = 10):
    """
    Recherche des business locaux via Google Maps Places API.
    """
    results = []
    params = {
        "query": f"{query} in {city}",
        "key": GOOGLE_MAPS_API_KEY,
        "language": "fr"
    }

    try:
        response = requests.get(GOOGLE_MAPS_PLACES_URL, params=params)
        data = response.json()

        if data.get("status") != "OK":
            logger.error(f"Google Maps API error: {data.get('status')}")
            return results

        businesses = data.get("results", [])[:max_results]

        for b in businesses:
            business_data = {
                "name": b.get("name"),
                "category": query,
                "phone": "",
                "email": "",
                "website": b.get("website") if "website" in b else "",
                "rating": b.get("rating", 0),
                "reviews_count": b.get("user_ratings_total", 0),
                "city": city,
                "score_ai": None,
                "recommendation": None,
                "source_url": f"https://www.google.com/maps/place/?q=place_id:{b.get('place_id')}"
            }
            add_business(business_data)
            results.append(business_data)

        logger.info(f"{len(results)} business ajoutés depuis Google Maps")
        return results

    except Exception as e:
        logger.error(f"Erreur google_maps.py: {e}")
        return results
