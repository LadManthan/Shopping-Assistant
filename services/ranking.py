from models.schemas import GraphState


def _normalize(values: list[float]) -> list[float]:
    """Min-max normalize a list of floats to [0, 1]."""
    min_v, max_v = min(values), max(values)
    if max_v == min_v:
        return [1.0] * len(values)
    return [(v - min_v) / (max_v - min_v) for v in values]


def rank_products(state: GraphState) -> GraphState:
    """
    Ranks products using a normalized composite score:
      - 40% rating (higher is better)
      - 30% review count (more reviews = more trustworthy)
      - 30% inverse price (lower price = better value)

    Raw rating/price caused extreme skew — normalization fixes this.
    """
    products = state["products"]

    if not products:
        return {**state, "ranked_products": []}


    ratings = [float(p.get("rating") or 0) for p in products]
    review_counts = [int(p.get("ratings_total") or 0) for p in products]
    prices = [float(p.get("price") or 1) for p in products]

    norm_ratings = _normalize(ratings)
    norm_reviews = _normalize(review_counts)
    # Invert price so cheaper = higher score
    norm_inv_prices = _normalize([-p for p in prices])

    for i, product in enumerate(products):
        product["score"] = round(
            0.40 * norm_ratings[i]
            + 0.30 * norm_reviews[i]
            + 0.30 * norm_inv_prices[i],
            4,
        )

    ranked = sorted(products, key=lambda x: x["score"], reverse=True)
    return {**state, "ranked_products": ranked}