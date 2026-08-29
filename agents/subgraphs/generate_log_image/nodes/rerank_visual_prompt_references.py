from common.utils.embedding import embed_text
from agents.subgraphs.generate_log_image.state import GraphState
from langgraph.runtime import Runtime
from agents.daily_logs_agent.state import Context
from common.config import settings
import logging

logger = logging.getLogger(__name__)


async def rerank_visual_prompt_references(state: GraphState, runtime: Runtime[Context]):
    image_references = state["image_references"]
    visual_scene = state["visual_scene"]
    reranker = runtime.context.reranker

    reranked_results = reranker.rerank(
        query=visual_scene,
        documents=[reference["situation"] for reference in image_references],
        top_k=3,
    )

    # 리랭킹된 결과중 가장 적합한 결과 선택
    best_result = reranked_results[0]
    best_image_reference = image_references[best_result.original_index]
    logger.info("rerank_visual_prompt_references 완료")
    logger.debug(
        "rerank visual prompt references | top_results=%s",
        reranked_results[:3],
    )
    return {
        "image_reference": best_image_reference,
        "image_reference_image_url": f"{settings.R2_PUBLIC_DOMAIN}/{best_image_reference['image_url']}",
    }
