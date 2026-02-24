import streamlit as st
from graph import shopping_graph
from models.schemas import GraphState

st.set_page_config(page_title="AI Shopping Comparison", layout="wide")

st.markdown("<h1 style='text-align:center'>🛍️ AI Shopping Comparison Assistant</h1>", unsafe_allow_html=True)

query = st.text_input("Enter product requirement:", placeholder="e.g. noise cancelling headphones under 5000")

if st.button("🔍 Compare", use_container_width=True):
    if not query.strip():
        st.warning("Please enter a product to search.")
    else:
        with st.spinner("Fetching and comparing products from Amazon India..."):
            try:
                graph = shopping_graph()
                state: GraphState = {
                    "user_query": query,
                    "refined_query": "",
                    "products": [],
                    "ranked_products": [],
                    "final_response": "",
                }
                result = graph.invoke(state)
            except Exception as e:
                st.error(f"Something went wrong: {e}")
                st.stop()

        ranked = result.get("ranked_products", [])
        final_response = result.get("final_response", "")

        if not ranked:
            st.warning("No products found. Try a different or broader search term.")
            st.stop()

        # ── AI Recommendation ─────
        st.markdown("## AI Recommendation")
        st.markdown(final_response)
        st.divider()

        # ── Top Products ─────
        st.markdown("## 🏆 Top Matched Products")
        top_products = ranked[:5]

        for i, product in enumerate(top_products, 1):
            with st.container():
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.markdown(f"### {i}. {product['title']}")

                    brand = product.get("brand", "")
                    if brand and brand != "Unknown":
                        st.write(f"**Brand:** {brand}")

                    st.write(f"**Price:** ₹{product['price']:,.0f}")

                    rating = product.get("rating", 0)
                    reviews = product.get("ratings_total", 0)
                    st.write(f"**Rating:** {'⭐' * int(round(rating))} {rating} ({reviews:,} reviews)")

                    score = product.get("score", 0)
                    st.caption(f"Composite Score: {score:.3f}")

                with col2:
                    image_url = product.get("image", "")
                    if image_url:
                        st.image(image_url, width=140)

                    product_link = product.get("product_link", "")
                    if product_link:
                        st.markdown(f"[🔗 View on Amazon]({product_link})")

            st.markdown("---")