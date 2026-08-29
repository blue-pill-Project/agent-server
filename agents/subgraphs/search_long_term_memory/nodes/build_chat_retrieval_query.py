from agents.subgraphs.search_long_term_memory.llm import build_retrieval_query_llm
from agents.subgraphs.search_long_term_memory.state import (
    GraphState,
    Context,
    RetrievalQuery,
)
from agents.subgraphs.search_long_term_memory.prompts import (
    build_chat_retrieval_query_instructions,
)
from langgraph.runtime import Runtime
import logging

logger = logging.getLogger(__name__)


def build_chat_retrieval_query(
    state: GraphState,
    runtime: Runtime[Context],
):
    print("💬")
    formatted_prompt = build_chat_retrieval_query_instructions.format(
        now=runtime.context.now,
        source=state["source"].source,
    )
    structured_model = build_retrieval_query_llm.with_structured_output(RetrievalQuery)

    result = structured_model.invoke(formatted_prompt)

    logger.info("build_chat_retrieval_query 완료")
    logger.debug(
        "retrieval query | should_search=%s | retrieval_query=%s | kind_hint=%s ",
        result.should_search,
        result.retrieval_query,
        result.kind_hint,
    )

    return {"retrieval_query": result}
