import pprint
from common.utils.embedding import embed_text
from agents.subgraphs.generate_log_image.state import GraphState, ImageCategory
from langgraph.runtime import Runtime
from agents.daily_logs_agent.state import Context
from common.config import settings


async def rerank_visual_prompt_references(state: GraphState, runtime: Runtime[Context]):
    image_references = state["image_references"]
    hourly_plan_description = state["hourly_plan"].description

    reranker = runtime.context.reranker

    results = reranker.rerank(
        query=hourly_plan_description,
        documents=[ref["situation"] for ref in image_references],
        top_k=3,
    )

    best_result = results[0]

    best_reference = image_references[best_result.original_index]

    # 원본 ref에서 실제로 사용할 prompt만 가져온다.
    image_reference_image_url = (
        f"{settings.R2_PUBLIC_DOMAIN}/{best_reference['image_url']}"
    )

    return {
        "image_reference": results[0],
        "image_reference_image_url": image_reference_image_url,
    }
