from langgraph.graph import StateGraph, START, END
from agents.character_chat_agent.nodes import generate_reply
from agents.character_chat_agent.state import GraphState, Context
from agents.subgraphs.search_long_term_memory.graph import (
    build_search_long_term_memory_graph,
)
from agents.subgraphs.search_long_term_memory.state import Source
from agents.subgraphs.write_long_term_memory.graph import (
    build_write_long_term_memory_graph,
)
from agents.subgraphs.write_long_term_memory.state import MemorySource
from langgraph.runtime import Runtime

write_long_term_memory_graph = build_write_long_term_memory_graph()
search_long_term_memory_graph = build_search_long_term_memory_graph()


compiled_search_long_term_memory_graph = search_long_term_memory_graph.compile()
compiled_write_long_term_memory_graph = write_long_term_memory_graph.compile()


async def call_search_long_term_memory_graph(state, runtime: Runtime[Context]):
    # TODO: 이게 최선인가?
    source = f"[사용자의 메세지]\n{state['messages'][-1]}\n\n"

    print(source)
    result = await compiled_search_long_term_memory_graph.ainvoke(
        {
            "source": Source(
                purpose="chat",
                source=source,
            ),
        },
        context=runtime.context,
    )

    long_term_memories = result["final_long_term_memories"]
    return {"long_term_memories": long_term_memories}


async def call_write_long_term_memory_graph(state, runtime: Runtime[Context]):

    source = (
        f"[사용자의 메세지]\n"
        f"{state['messages'][-2]}\n\n"
        f"[캐릭터의 메세지]\n"
        f"{state['messages'][-1]}\n\n"
    )

    print(source)

    memory_source = MemorySource(
        source_type="log",
        source=source,
        occurred_at=runtime.context.current_date,
    )

    result = await compiled_write_long_term_memory_graph.ainvoke(
        {"memory_source": memory_source, "is_saved_long_term_memory": False},
        context=runtime.context,
    )
    is_saved_long_term_memory = result["is_saved_long_term_memory"]
    return {"is_saved_long_term_memory": is_saved_long_term_memory}


def build_character_chat_graph():
    graph = StateGraph(
        GraphState,
        context_schema=Context,
    )

    graph.add_node("generate_reply", generate_reply)
    graph.add_node(
        "call_search_long_term_memory_graph", call_search_long_term_memory_graph
    )
    graph.add_node(
        "call_write_long_term_memory_graph", call_write_long_term_memory_graph
    )

    graph.add_edge(START, "call_search_long_term_memory_graph")
    graph.add_edge("call_search_long_term_memory_graph", "generate_reply")
    graph.add_edge("generate_reply", "call_write_long_term_memory_graph")

    graph.add_edge("call_write_long_term_memory_graph", END)

    return graph
