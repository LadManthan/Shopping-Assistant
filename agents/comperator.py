from langchain_groq import ChatGroq
import streamlit as st
from models.schemas import GraphState

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

llm = ChatGroq(
    groq_api_key = GROQ_API_KEY,
    model_name = 'llama-3.3-70b-versatile'
)

def generate_comparison(state:GraphState) -> GraphState:
    top_products = state["ranked_products"][:5]

    if not top_products:
        return {
            **state,
            "final_response": "No products found for your query. Please try a different search term.",
        }

    product_lines = []
    for i, p in enumerate(top_products, 1):
        brand = p.get("brand", "Unknown Brand")
        reviews = p.get("ratings_total", 0)
        product_lines.append(
            f"{i}. {p['title']}\n"
            f"Brand: {brand} | Price: ₹{p['price']:,.0f} | "
            f"Rating: {p['rating']}⭐ ({reviews:,} reviews)"
        )

    product_text = "\n".join(product_lines)

    prompt = f"""You are a smart product comparison assistant for Indian shoppers.

User is looking for: {state['user_query']}

Top Ranked Products (ranked by rating, review count, and value):
{product_text}

Provide a structured comparison with:
1. **Price Range** — What price range do these products fall in?
2. **Best Rated** — Which product has the highest rating and why it stands out
3. **Best Value** — Which product gives the most for the money
4. **Brand Insights** — Any notable brands in the list worth trusting
5. **Final Recommendation** — One clear winner with a brief reason

Keep it concise, helpful, and specific to Indian buyers. Use ₹ for prices.
"""

    response = llm.invoke(prompt)
    return {**state, "final_response": response.content}