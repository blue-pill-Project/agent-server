import pprint
from agents.subgraphs.generate_log_image.state import GraphState
from langgraph.runtime import Runtime
from agents.daily_logs_agent.state import Context
from common.config import settings
import logging

logger = logging.getLogger(__name__)


async def get_default_selfie_visual_prompt_reference(
    state: GraphState, runtime: Runtime[Context]
):

    repository = runtime.context.visual_prompt_reference_repository
    reference = await repository.get_random_default_selfie()
    logger.info("get_default_selfie_visual_prompt_reference 완료")

    return {
        "image_reference": reference,
        "image_reference_image_url": f"{settings.R2_PUBLIC_DOMAIN}/{reference['image_url']}",
    }
