from langgraph.graph import StateGraph, START, END
from agents.subgraphs.generate_hourly_plan.nodes import generate_hourly_plan
from agents.subgraphs.generate_hourly_plan.state import GraphState


def build_generate_hourly_plan_graph() -> StateGraph:
    graph = StateGraph(GraphState)

    graph.add_node("generate_hourly_plan", generate_hourly_plan)

    graph.add_edge(START, "generate_hourly_plan")
    graph.add_edge("generate_hourly_plan", END)

    return graph
