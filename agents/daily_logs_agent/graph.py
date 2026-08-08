from langgraph.graph import StateGraph, START, END
from agents.daily_logs_agent.state import Context, GraphState, HourlyLog
from agents.subgraphs.generate_hourly_plan.graph import build_generate_hourly_plan_graph
from agents.subgraphs.generate_log_image.graph import build_generate_log_image_graph
from agents.subgraphs.generate_log_text.graph import build_generate_log_text_graph
from langgraph.runtime import Runtime

from agents.subgraphs.search_long_term_memory.graph import (
    build_search_long_term_memory_graph,
)
from agents.subgraphs.search_long_term_memory.state import Source
from agents.subgraphs.write_long_term_memory.graph import (
    build_write_long_term_memory_graph,
)
from agents.subgraphs.write_long_term_memory.state import MemorySource


generate_hourly_plan_graph = build_generate_hourly_plan_graph()
generate_log_text_graph = build_generate_log_text_graph()
generate_log_image_graph = build_generate_log_image_graph()
search_long_term_memory_graph = build_search_long_term_memory_graph()
write_long_term_memory_graph = build_write_long_term_memory_graph()


compiled_generate_hourly_plan_graph = generate_hourly_plan_graph.compile()
compiled_generate_log_text_graph = generate_log_text_graph.compile()
compiled_generate_log_image_graph = generate_log_image_graph.compile()
compiled_search_long_term_memory_graph = search_long_term_memory_graph.compile()
compiled_write_long_term_memory_graph = write_long_term_memory_graph.compile()


async def call_search_long_term_memory_graph(state, runtime: Runtime[Context]):
    # TODO: 이게 최선인가?
    source = f"""[Target Timeslot] {runtime.context.timeslot_label} [Daily Plan] {runtime.context.today_plan} [Previous Hourly Plans] {runtime.context.previous_plans}"""

    result = await compiled_search_long_term_memory_graph.ainvoke(
        {
            "source": Source(
                purpose="post",
                source=source,
            ),
        },
        context=runtime.context,
    )

    long_term_memories = result["final_long_term_memories"]
    return {"long_term_memories": long_term_memories}


async def call_generate_hourly_plan_graph(state, runtime: Runtime[Context]):
    result = await compiled_generate_hourly_plan_graph.ainvoke(
        {
            "long_term_memories": state["long_term_memories"],
        },
        context=runtime.context,
    )

    hourly_plan = result["hourly_plan"]

    return {"hourly_plan": hourly_plan}


async def call_generate_log_image_graph(state, runtime: Runtime[Context]):
    result = await compiled_generate_log_image_graph.ainvoke(
        {
            "hourly_plan": state["hourly_plan"],
        },
        context=runtime.context,
    )

    log_image_url = result["log_image_url"]

    return {"log_image_url": log_image_url}


async def call_generate_log_text_graph(state, runtime: Runtime[Context]):
    result = await compiled_generate_log_text_graph.ainvoke(
        {
            "hourly_plan": state["hourly_plan"],
        },
        context=runtime.context,
    )

    log_text = result["log_text"]

    return {"log_text": log_text}


def aggregate_log_outputs(state: GraphState, runtime: Runtime[Context]):
    log_image_url = state["log_image_url"]
    hourly_plan = state["hourly_plan"]
    log_text = state["log_text"]
    # TODO: 타입 수정해야함
    if isinstance(log_image_url, list):
        log_image_url = log_image_url[0] if log_image_url else ""

    hourly_log = HourlyLog(
        timeslot=runtime.context.timeslot,
        hourly_plan=hourly_plan,
        log_image_url=log_image_url,
        log_text=log_text,
    )

    return {
        "hourly_log": hourly_log,
    }


async def call_write_long_term_memory_graph(state, runtime: Runtime[Context]):
    source = (
        f"[Target Timeslot]\n"
        f"{runtime.context.timeslot_label}\n\n"
        f"[이번 시간대 계획]\n"
        f"{state['hourly_plan']}\n\n"
        f"[이번 시간대 로그 텍스트]\n"
        f"{state['log_text']}"
    )

    memory_source = MemorySource(
        source_type="log",
        source=source,
        occurred_at=runtime.context.current_date,
    )

    result = await compiled_write_long_term_memory_graph.ainvoke(
        {
            "memory_source": memory_source,
            "is_saved_long_term_memory":False
        },
        context=runtime.context,
    )
    is_saved_long_term_memory = result["is_saved_long_term_memory"]
    return {"is_saved_long_term_memory": is_saved_long_term_memory}


def build_daily_logs_graph() -> StateGraph:
    graph = StateGraph(
        GraphState,
        context_schema=Context,
    )

    graph.add_node("call_generate_hourly_plan_graph", call_generate_hourly_plan_graph)
    graph.add_node("call_generate_log_text_graph", call_generate_log_text_graph)
    graph.add_node("call_generate_log_image_graph", call_generate_log_image_graph)
    graph.add_node("aggregate_log_outputs", aggregate_log_outputs)
    graph.add_node(
        "call_search_long_term_memory_graph", call_search_long_term_memory_graph
    )
    graph.add_node(
        "call_write_long_term_memory_graph", call_write_long_term_memory_graph
    )

    graph.add_edge(START, "call_search_long_term_memory_graph")
    graph.add_edge(
        "call_search_long_term_memory_graph", "call_generate_hourly_plan_graph"
    )
    graph.add_edge("call_generate_hourly_plan_graph", "call_generate_log_text_graph")
    graph.add_edge("call_generate_hourly_plan_graph", "call_generate_log_image_graph")

    graph.add_edge("call_generate_log_text_graph", "aggregate_log_outputs")
    graph.add_edge("call_generate_log_image_graph", "aggregate_log_outputs")
    graph.add_edge("aggregate_log_outputs", "call_write_long_term_memory_graph")
    graph.add_edge("call_write_long_term_memory_graph", END)

    return graph
