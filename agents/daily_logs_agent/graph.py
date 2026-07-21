from langgraph.graph import StateGraph, START, END

from agents.daily_logs_agent.nodes import (
    load_long_term_memories,
)

from agents.daily_logs_agent.state import Context, GraphState, HourlyLog
from agents.subgraphs.generate_hourly_plan.graph import build_generate_hourly_plan_graph
from agents.subgraphs.generate_log_image.graph import build_generate_log_image_graph
from agents.subgraphs.generate_log_text.graph import build_generate_log_text_graph


generate_hourly_plan_graph = build_generate_hourly_plan_graph()
generate_log_text_graph = build_generate_log_text_graph()
generate_log_image_graph = build_generate_log_image_graph()


compiled_generate_hourly_plan_graph = generate_hourly_plan_graph.compile()
compiled_generate_log_text_graph = generate_log_text_graph.compile()
compiled_generate_log_image_graph = generate_log_image_graph.compile()


def call_generate_hourly_plan_graph(state):
    state = compiled_generate_hourly_plan_graph.invoke(
        {
            "character_info": state["character_info"],
            "history": state["history"],
            "daily_plan": state["daily_plan"],
            "timeslot": state["timeslot"],
            "today_chat": state["today_chat"],
            "related_chats": state["related_chats"],
            "previous_plans": state["previous_plans"],
            "long_term_memories": state["long_term_memories"],
        }
    )

    hourly_plan = state["hourly_plan"]

    return {"hourly_plan": hourly_plan}


def call_generate_log_image_graph(state):
    state = compiled_generate_log_image_graph.invoke(
        {
            "hourly_plan": state["hourly_plan"],
            "image_url": state["image_url"],
        }
    )

    log_image_url = state["log_image_url"]

    return {"log_image_url": log_image_url}


def call_generate_log_text_graph(state):
    state = compiled_generate_log_text_graph.invoke(
        {
            "character_info": state["character_info"],
            "history": state["history"],
            "hourly_plan": state["hourly_plan"],
        }
    )

    log_text = state["log_text"]

    return {"log_text": log_text}


def aggregate_log_outputs(state: GraphState):
    log_image_url = state["log_image_url"]

    # TODO: 타입 수정해야함
    if isinstance(log_image_url, list):
        log_image_url = log_image_url[0] if log_image_url else ""

    hourly_log = HourlyLog(
        timeslot=state["timeslot"],
        hourly_plan=state["hourly_plan"],
        log_image_url=log_image_url,
        log_text=state["log_text"],
    )

    return {
        "hourly_log": hourly_log,
    }


def build_daily_logs_graph() -> StateGraph:
    graph = StateGraph(
        GraphState,
        context_schema=Context,
    )

    graph.add_node("call_generate_hourly_plan_graph", call_generate_hourly_plan_graph)
    graph.add_node("call_generate_log_text_graph", call_generate_log_text_graph)
    graph.add_node("call_generate_log_image_graph", call_generate_log_image_graph)
    graph.add_node("aggregate_log_outputs", aggregate_log_outputs)
    graph.add_node("load_long_term_memories", load_long_term_memories)

    graph.add_edge(START, "load_long_term_memories")
    graph.add_edge("load_long_term_memories", "call_generate_hourly_plan_graph")
    graph.add_edge("call_generate_hourly_plan_graph", "call_generate_log_text_graph")
    graph.add_edge("call_generate_hourly_plan_graph", "call_generate_log_image_graph")

    graph.add_edge("call_generate_log_text_graph", "aggregate_log_outputs")
    graph.add_edge("call_generate_log_image_graph", "aggregate_log_outputs")
    graph.add_edge("aggregate_log_outputs", END)

    return graph
