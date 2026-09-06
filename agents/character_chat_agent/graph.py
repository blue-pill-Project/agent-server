import logging

from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from agents.character_chat_agent.nodes import (
    generate_reply,
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
from agents.character_chat_agent.llm import tools
from langchain_core.messages import AIMessage, HumanMessage

logger = logging.getLogger(__name__)


write_long_term_memory_graph = build_write_long_term_memory_graph()
search_long_term_memory_graph = build_search_long_term_memory_graph()

compiled_search_long_term_memory_graph = search_long_term_memory_graph.compile()
compiled_write_long_term_memory_graph = write_long_term_memory_graph.compile()


def get_latest_user_message(messages):
    for message in reversed(messages):
        if isinstance(message, HumanMessage):
            return message

    return None


def get_latest_character_message(messages):
    for message in reversed(messages):
        if isinstance(message, AIMessage) and not message.tool_calls:
            return message

    return None


def route_after_actor(state: GraphState):
    last_message = state["messages"][-1]

    tool_calls = last_message.tool_calls if isinstance(last_message, AIMessage) else []

    logger.debug("last message | last_message=%s", last_message.content)

    if tool_calls:
        logger.info("route_after_actor → tools | tool 사용")
        logger.debug("tool calls | tool_calls=%s", tool_calls)
        return "tools"

    logger.info("route_after_actor → write_memory | tool 사용안함")

    return "call_write_long_term_memory_graph"


async def call_search_long_term_memory_graph(state, runtime: Runtime[Context]):
    user_message = get_latest_user_message(state["messages"])
    source = f"[사용자의 메세지] {user_message.content}"

    logger.debug("user message | message=%s", source)
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


async def call_write_long_term_memory_graph(
    state: GraphState,
    runtime: Runtime[Context],
):

    user_message = get_latest_user_message(state["messages"])
    character_message = get_latest_character_message(state["messages"])

    if not user_message or not character_message:
        return {
            "is_saved_long_term_memory": False,
        }

    source = (
        f"[사용자의 메세지] "
        f"{user_message.content} "
        f"[캐릭터의 메세지] "
        f"{character_message.content} "
    )

    logger.debug("recent user and character message | messages=%s", source)

    memory_source = MemorySource(
        source_type="log",
        source=source,
        occurred_at=runtime.context.current_date,
    )

    result = await compiled_write_long_term_memory_graph.ainvoke(
        {
            "memory_source": memory_source,
            "is_saved_long_term_memory": False,
        },
        context=runtime.context,
    )

    return {
        "is_saved_long_term_memory": result["is_saved_long_term_memory"],
    }


def build_character_chat_graph():
    graph = StateGraph(
        GraphState,
        context_schema=Context,
    )

    graph.add_node("generate_reply", generate_reply)
    graph.add_node(
        "tools",
        ToolNode(tools),
    )
    graph.add_node(
        "call_search_long_term_memory_graph", call_search_long_term_memory_graph
    )
    graph.add_node(
        "call_write_long_term_memory_graph", call_write_long_term_memory_graph
    )
    graph.add_edge(START, "call_search_long_term_memory_graph")
    graph.add_edge("call_search_long_term_memory_graph", "generate_reply")
    graph.add_conditional_edges(
        "generate_reply",
        route_after_actor,
        {
            "tools": "tools",
            "call_write_long_term_memory_graph": "call_write_long_term_memory_graph",
        },
    )
    graph.add_edge(
        "tools",
        "generate_reply",
    )

    graph.add_edge("call_write_long_term_memory_graph", END)

    return graph
