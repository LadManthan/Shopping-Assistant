import requests
from dotenv import load_dotenv
import os

load_dotenv()

RAINFOREST_API_KEY = os.getenv("RAINFOREST_API_KEY")
RAINFOREST_BASE_URL = "https://api.rainforestapi.com/request"


def fetch_products(query: str) -> list[dict]:
    """
    Fetches products from Amazon India via Rainforest API.
    Returns a normalized list of product dicts.
    """
    params = {
        "api_key": RAINFOREST_API_KEY,
        "type": "search",
        "amazon_domain": "amazon.in",
        "search_term": query,
        "sort_by": "featured",
        "exclude_sponsored": "true",
    }

    try:
        response = requests.get(RAINFOREST_BASE_URL, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"[RainforestAPI] Request failed: {e}")
        return []

    raw_results = data.get("search_results", [])
    products = []

    for item in raw_results[:15]:  # fetch more, ranking will trim to top 5
        try:
            # Price
            price_obj = item.get("price", {})
            price = float(price_obj.get("value", 0) or 0)

            # Rating
            rating = float(item.get("rating", 0) or 0)
            ratings_total = int(item.get("ratings_total", 0) or 0)

            # Skip products with no price or rating (not useful for comparison)
            if price == 0 or rating == 0:
                continue

            products.append({
                "title": item.get("title", "Unknown"),
                "brand": item.get("brand", "Unknown"),
                "price": price,
                "rating": rating,
                "ratings_total": ratings_total,  # review count — important for trust
                "asin": item.get("asin", ""),
                "product_link": item.get("link", ""),
                "image": item.get("image", ""),
            })
        except (TypeError, ValueError):
            continue  # skip malformed entries

    return products