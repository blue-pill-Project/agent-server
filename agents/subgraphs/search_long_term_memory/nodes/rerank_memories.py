from agents.subgraphs.search_long_term_memory.state import GraphState, Context, RerankedResults
from agents.subgraphs.search_long_term_memory.prompts import rerank_memories_instructions
from agents.subgraphs.search_long_term_memory.llm import rerank_memories_llm
from langgraph.runtime import Runtime
from domains.long_term_memory.service import build_memory_namespace


def rerank_memories(
    state: GraphState,
    runtime: Runtime[Context],
):
    formatted_prompt = rerank_memories_instructions.format(
        retrieval_query=state["retrieval_query"].retrieval_query,
        now=runtime.context.now,
        search_results=state["search_results"],
    )
    structured_model = rerank_memories_llm.with_structured_output(RerankedResults)

    result = structured_model.invoke(formatted_prompt)

    return {
        "reranked_results": result.reranked_results
    }
