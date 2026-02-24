from serpapi import GoogleSearch
import streamlit as st

SERP_API_KEY = st.secrets["SERP_API_KEY"]

def fetch_products(query):
    params = {
            "q": query,
            "tbm": "shop",
            "hl": "en",
            "gl": "in",
            "location": "India",
            "google_domain": "google.co.in",
            "api_key": SERP_API_KEY
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    shopping_results = results.get("shopping_results",[])
    
    products = []
    for result in shopping_results[:10]:
        products.append({
            "title":result.get("title"),
            "price":float(result.get("extracted_price",0) or 0),
            "rating":result.get("rating",0),
            "source":result.get("source"),
            "product_link":result.get("product_link")
        })
        
    return products