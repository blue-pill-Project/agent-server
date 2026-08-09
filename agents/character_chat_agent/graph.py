from langgraph.graph import StateGraph, START, END
from agents.character_chat_agent.nodes import (
    classify_intent,
    generate_reply,
    answer_with_search,
)
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

def route_intent(state):
    return state["intent_decision"].intent

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
    graph.add_node("classify_intent", classify_intent)
    graph.add_node("answer_with_search", answer_with_search)
    graph.add_node("generate_reply", generate_reply)
    graph.add_node(
        "call_search_long_term_memory_graph", call_search_long_term_memory_graph
    )
    graph.add_node(
        "call_write_long_term_memory_graph", call_write_long_term_memory_graph
    )
    # TODO: 코드가 합쳐지면서 이중 메모리 서칭 필요 유무 확인하고있음 수정해야함
    graph.add_edge(START, "classify_intent")
    graph.add_conditional_edges(
        "classify_intent",
        route_intent,
        {
            "memory": "call_search_long_term_memory_graph",
            "search": "answer_with_search",
            "other":  "generate_reply",
        },
    )
    graph.add_edge("call_search_long_term_memory_graph", "generate_reply")
    graph.add_edge("answer_with_search", "call_write_long_term_memory_graph")
    graph.add_edge("generate_reply", "call_write_long_term_memory_graph")
    graph.add_edge("call_write_long_term_memory_graph", END)
 
    return graph
