from agents.subgraphs.write_long_term_memory.prompts import (
    extract_memory_candidates_instructions,
)
from agents.subgraphs.write_long_term_memory.state import Memories, GraphState
from agents.subgraphs.write_long_term_memory.llm import (
    extract_memory_candidates_llm,
)
import logging

logger = logging.getLogger(__name__)


def extract_memory_candidates(
    state: GraphState,
):
    memory_source = state["memory_source"]
    memory_source_source_type = memory_source.source_type
    memory_source_source = memory_source.source
    memory_source_occurred_at = memory_source.occurred_at

    formatted_prompt = extract_memory_candidates_instructions.format(
        memory_source_source_type=memory_source_source_type,
        memory_source_source=memory_source_source,
        memory_source_occurred_at=memory_source_occurred_at,
    )

    structured_model = extract_memory_candidates_llm.with_structured_output(Memories)
    response = structured_model.invoke(formatted_prompt)
    logger.info("extract_memory_candidates 완료")
    logger.debug(
        "memory candidates | count=%d\n%s",
        len(response.memories),
        "\n".join(f"- {memory}" for memory in response.memories),
    )

    return {"memories": response.memories}
