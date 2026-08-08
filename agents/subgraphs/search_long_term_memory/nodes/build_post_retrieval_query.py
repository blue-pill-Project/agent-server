from agents.subgraphs.search_long_term_memory.llm import build_retrieval_query_llm
from agents.subgraphs.search_long_term_memory.state import (
    GraphState,
    Context,
    RetrievalQuery,
)
from agents.subgraphs.search_long_term_memory.prompts import (
    build_post_retrieval_query_instructions,
)
from langgraph.runtime import Runtime


def build_post_retrieval_query(
    state: GraphState,
    runtime: Runtime[Context],
):
    print("📋")
    formatted_prompt = build_post_retrieval_query_instructions.format(
        now=runtime.context.now,
        source=state["source"].source,
    )
    structured_model = build_retrieval_query_llm.with_structured_output(RetrievalQuery)

    result = structured_model.invoke(formatted_prompt)

    return {"retrieval_query": result}
