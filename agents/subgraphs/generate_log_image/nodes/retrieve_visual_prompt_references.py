import pprint
from common.utils.embedding import embed_text
from agents.subgraphs.generate_log_image.state import GraphState, ImageCategory
from langgraph.runtime import Runtime
from agents.daily_logs_agent.state import Context

SIMILARITY_THRESHOLD = 0.5


async def retrieve_visual_prompt_references(
    state: GraphState, runtime: Runtime[Context]
):
    repository = runtime.context.visual_prompt_reference_repository
    visual_scene = state["visual_scene"]
    # TODO: 나중에 이미지 SOLO 말고 다른 종류의 사진도 검색해서 제네레이션 가능해야함
    category = ImageCategory.SOLO_PHOTO
    embedding = embed_text(f"{visual_scene}")

    references = await repository.search(
        category=category,
        query_vector=embedding,
        limit=5,
    )
    # 유사도 검사
    # SIMILARITY_THRESHOLD를 넘지 못하면 기본 셀카로 진행
    has_relevant_reference = (
        references and references[0]["similarity"] >= SIMILARITY_THRESHOLD
    )
    print(f"🔢: {references[0]['similarity']}")

    if not has_relevant_reference:
        return {
            "use_default_reference": True,
            "image_references": [],
        }

    return {
        "use_default_reference": False,
        "image_references": references,
    }
