from typing import Annotated
from fastapi import APIRouter, File, HTTPException, Request, UploadFile
from api.schemas.visual_prompt_reference import VisualPromptReferenceResponse


router = APIRouter(prefix="/visual-prompt-reference", tags=["visual_prompt_reference"])


ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
}


@router.post(
    "/run",
    response_model=VisualPromptReferenceResponse,
)
async def run_visual_prompt_reference(
    request: Request,
    image: Annotated[UploadFile, File()],
):
    if image.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=415,
            detail="JPEG, PNG, WEBP 이미지만 업로드할 수 있습니다.",
        )

    image_bytes = await image.read()

    visual_prompt_reference_agent = request.app.state.visual_prompt_reference_agent

    result = await visual_prompt_reference_agent.run(
        image_bytes=image_bytes,
        image_content_type=image.content_type,
    )

    return VisualPromptReferenceResponse(success=result)
