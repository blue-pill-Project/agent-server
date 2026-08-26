import pprint
from common.utils.embedding import embed_text
from agents.subgraphs.generate_log_image.state import GraphState
from langgraph.runtime import Runtime
from agents.daily_logs_agent.state import Context
from common.config import settings


async def rerank_visual_prompt_references(state: GraphState, runtime: Runtime[Context]):
    image_references = state["image_references"]
    visual_scene = state["visual_scene"]

    reranker = runtime.context.reranker

    results = reranker.rerank(
        query=visual_scene,
        documents=[ref["situation"] for ref in image_references],
        top_k=3,
    )

    best_result = results[0]

    best_reference = image_references[best_result.original_index]

    image_reference_image_url = (
        f"{settings.R2_PUBLIC_DOMAIN}/{best_reference['image_url']}"
    )
    return {
        "image_reference": results[0],
        "image_reference_image_url": image_reference_image_url,
    }
