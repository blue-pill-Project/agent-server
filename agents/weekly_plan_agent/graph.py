from langgraph.graph import StateGraph, START, END
from agents.weekly_plan_agent.nodes import (
    select_trends,
    generate_weekly_plan,
)
from agents.weekly_plan_agent.state import GraphState


def build_weekly_plan_graph() -> StateGraph:
    graph = StateGraph(GraphState)

    graph.add_node("select_trends", select_trends)
    graph.add_node("generate_weekly_plan", generate_weekly_plan)

    graph.add_edge(START, "select_trends")
    graph.add_edge("select_trends", "generate_weekly_plan")
    graph.add_edge("generate_weekly_plan", END)

    return graph
