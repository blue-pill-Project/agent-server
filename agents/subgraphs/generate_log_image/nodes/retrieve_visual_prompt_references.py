import pprint
from common.utils.embedding import embed_text
from agents.subgraphs.generate_log_image.state import GraphState, ImageCategory
from langgraph.runtime import Runtime
from agents.daily_logs_agent.state import Context


async def retrieve_visual_prompt_references(
    state: GraphState, runtime: Runtime[Context]
):
    repository = runtime.context.visual_prompt_reference_repository
    visual_prompt_reference_search_query = state["visual_prompt_reference_search_query"]
    # TODO: 나중에 이미지 SOLO 말고 다른 종류의 사진도 검색해서 제네레이션 가능해야함
    category = ImageCategory.SOLO_PHOTO
    embedding = embed_text(f"{visual_prompt_reference_search_query}")

    print(visual_prompt_reference_search_query)

    references = await repository.search(
        category=category,
        query_vector=embedding,
        limit=5,
    )

    pprint.pprint(references, indent=2, width=60)

    return {"image_references": references}
