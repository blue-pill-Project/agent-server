from uuid import uuid4
from agents.base import BaseAgent
from agents.visual_prompt_reference.state import Context
from agents.visual_prompt_reference.graph import build_visual_prompt_reference_graph
from common.utils.embedding import embed_text
from domains.visual_prompt_reference.repository import VisualPromptReferenceRepository


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

        visual_prompt_reference = state["visual_prompt_reference"]

        visual_prompt_reference_for_save = (
            visual_prompt_reference.category,
            visual_prompt_reference.participant_count,
            visual_prompt_reference.prompt,
            embed_text(visual_prompt_reference.prompt),
        )

        success = await self._visual_prompt_reference_repository.save(
            visual_prompt_reference_for_save
        )
        print(visual_prompt_reference)

        return success
