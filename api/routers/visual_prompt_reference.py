from typing import Annotated
from fastapi import APIRouter, File, Form, HTTPException, Request, UploadFile
from api.schemas.visual_prompt_reference import VisualPromptReferenceResponse


router = APIRouter(
    prefix="/visual-prompt-reference",
    tags=["visual_prompt_reference"],
)

ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
}

MAX_BATCH_SIZE = 10


async def _validate_and_read_image(
    image: UploadFile,
) -> tuple[bytes, str]:
    """업로드된 이미지를 검증하고 바이트 데이터로 반환한다."""

    if image.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=415,
            detail=(
                f"{image.filename}: JPEG, PNG, WEBP 이미지만 업로드할 수 있습니다."
            ),
        )

    image_bytes = await image.read()

    return image_bytes, image.content_type


async def _process_image(
    image: UploadFile,
    visual_prompt_reference_agent,
    is_default: bool,
) -> VisualPromptReferenceResponse:
    """단일 이미지로 Visual Prompt Reference를 생성한다."""

    image_bytes, image_content_type = await _validate_and_read_image(image)

    success = await visual_prompt_reference_agent.run(
        image_bytes=image_bytes,
        image_content_type=image_content_type,
        is_default=is_default,
    )

    return VisualPromptReferenceResponse(
        success=success,
    )


@router.post(
    "/run",
    response_model=VisualPromptReferenceResponse,
)
async def run_visual_prompt_reference(
    request: Request,
    image: Annotated[UploadFile, File()],
    is_default: Annotated[bool, Form()] = False,
) -> VisualPromptReferenceResponse:
    """단일 이미지로 Visual Prompt Reference를 생성한다."""

    visual_prompt_reference_agent = request.app.state.visual_prompt_reference_agent

    return await _process_image(
        image=image,
        visual_prompt_reference_agent=visual_prompt_reference_agent,
        is_default=is_default,
    )
