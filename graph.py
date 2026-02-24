from langgraph.graph import StateGraph
from models.schemas import GraphState
from agents.analyzer import analyze_query
from tools.rainforest_tool import fetch_products
from services.ranking import rank_products
from agents.comperator import generate_comparison

def fetch_node(state: GraphState) -> GraphState:
    query = state["user_query"]
    products = fetch_products(query)
    return {**state, "products": products}


def rank_node(state: GraphState) -> GraphState:
    return rank_products(state)


def shopping_graph():
    workflow = StateGraph(GraphState)

    workflow.add_node("analyze", analyze_query)
    workflow.add_node("fetch", fetch_node)
    workflow.add_node("rank", rank_node)
    workflow.add_node("compare", generate_comparison)

    workflow.set_entry_point("analyze")
    workflow.add_edge("analyze", "fetch")
    workflow.add_edge("fetch", "rank")
    workflow.add_edge("rank", "compare")

    return workflow.compile()
