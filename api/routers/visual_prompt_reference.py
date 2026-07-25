from fastapi import APIRouter, Request
from api.schemas.trend import TrendResponse
from api.schemas.visual_prompt_reference import (
    VisualPromptReferenceRequest,
    VisualPromptReferenceResponse,
)


router = APIRouter(prefix="/visual-prompt-reference", tags=["visual-prompt-reference"])


@router.post("/run", response_model=VisualPromptReferenceResponse)
async def run_visual_prompt_reference(
    body: VisualPromptReferenceRequest,
    request: Request,
):
    visual_prompt_reference_agent = request.app.state.visual_prompt_reference_agent

    pinterest_url = body.pinterest_url

    result = await visual_prompt_reference_agent.run(pinterest_url)

    return VisualPromptReferenceResponse(success=result)
