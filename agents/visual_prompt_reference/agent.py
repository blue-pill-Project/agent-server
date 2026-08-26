import os
from uuid import uuid4
from agents.base import BaseAgent
from agents.visual_prompt_reference.state import Context
from agents.visual_prompt_reference.graph import build_visual_prompt_reference_graph
from common.utils.embedding import embed_text
from common.utils.r2 import get_r2_client
from domains.visual_prompt_reference.repository import VisualPromptReferenceRepository
from pathlib import Path


class VisualPromptReferenceAgent(BaseAgent):
    def __init__(
        self,
        visual_prompt_reference_repository: VisualPromptReferenceRepository,
    ):
        super().__init__()

        self._visual_prompt_reference_repository = visual_prompt_reference_repository

    def build_graph(self):
        return build_visual_prompt_reference_graph()

    async def run(
        self,
        image_bytes: bytes,
        image_content_type: str,
    ):

        context = Context(
            image_bytes=image_bytes,
            image_content_type=image_content_type,
        )

        state = await self.invoke({}, context=context)
        # TODO: 반복 수정 해야함
        bucket = os.getenv("R2_BUCKET_NAME", "bluepill-images")
        r2 = get_r2_client()
        filename = f"{uuid4().hex}.png"
        key = f"visual_prompt_references/{filename}"
        r2.put_object(Bucket=bucket, Key=key, Body=image_bytes, ContentType="image/png")

        visual_prompt_reference = state["visual_prompt_reference"]

        visual_prompt_reference_for_save = (
            visual_prompt_reference.category,
            visual_prompt_reference.participant_count,
            key,
            visual_prompt_reference.situation,
            embed_text(visual_prompt_reference.situation),
        )

        success = await self._visual_prompt_reference_repository.save(
            visual_prompt_reference_for_save
        )

        # TODO: 테스트 후 삭제해야함
        print(visual_prompt_reference.situation)

        return success
