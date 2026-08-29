from common.utils.embedding import embed_text
from agents.subgraphs.generate_log_image.state import GraphState, ImageCategory
from langgraph.runtime import Runtime
from agents.daily_logs_agent.state import Context
import logging

logger = logging.getLogger(__name__)
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

    # SIMILARITY_THRESHOLD를 넘지 못하면 기본 셀카로 진행
    # 레퍼런스가 없다면 그냥 참조이미지 없이 셀카 생성
    if not references:
        logger.info(
            "retrieve_visual_prompt_references 완료 | 참조 없이 텍스트로 이미지 생성"
        )
        return {
            "use_default_reference": False,
            "image_references": references,
        }

    logger.debug("similarity | similarity=%s", references[0]["similarity"])
    if not references[0]["similarity"] >= SIMILARITY_THRESHOLD:
        logger.info(
            "retrieve_visual_prompt_references 완료 | 기본 참조 이미지로 이미지 생성"
        )
        return {
            "use_default_reference": True,
            "image_references": [],
        }
    logger.info(
        "retrieve_visual_prompt_references 완료 | 유사 참조 이미지로 이미지 생성"
    )
    return {
        "use_default_reference": False,
        "image_references": references,
    }
