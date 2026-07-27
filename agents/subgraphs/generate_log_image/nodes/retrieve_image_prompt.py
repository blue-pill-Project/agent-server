import pprint
from common.utils.embedding import embed_text
from agents.subgraphs.generate_log_image.state import GraphState
from langgraph.runtime import Runtime
from agents.daily_logs_agent.state import Context


async def retrieve_image_prompt(state: GraphState, runtime: Runtime[Context]):
    repository = runtime.context.visual_prompt_reference_repository

    visual_prompt_reference_search_query = state["visual_prompt_reference_search_query"]
    category = state["image_category"].value

    embedding = embed_text(visual_prompt_reference_search_query)

    print(visual_prompt_reference_search_query)

    reference = await repository.search(
        category=category,
        query_vector=embedding,
    )

    return {"image_reference": reference}
