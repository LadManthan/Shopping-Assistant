from typing import List, Dict, TypedDict

class GraphState(TypedDict):
    user_query : str
    refined_query : str
    products : List[Dict]
    ranked_products : List[Dict]
    final_response : str