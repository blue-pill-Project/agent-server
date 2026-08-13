from langgraph.graph import StateGraph, START, END
from agents.character_prompt_agent.state import GraphState
from agents.character_prompt_agent.nodes import generate_character_prompt


def build_character_prompt_graph() -> StateGraph:
    graph = StateGraph(GraphState)

    graph.add_node("generate_character_prompt", generate_character_prompt)

    graph.add_edge(START, "generate_character_prompt")
    graph.add_edge("generate_character_prompt", END)

    return graph
