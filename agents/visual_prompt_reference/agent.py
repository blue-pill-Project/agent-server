from uuid import uuid4
from agents.base import BaseAgent
from agents.visual_prompt_reference.state import Context
from agents.visual_prompt_reference.graph import build_visual_prompt_reference_graph
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
        pinterest_url: str,
    ):

        context = Context(
            pinterest_url=pinterest_url,
        )

        state = await self.invoke({}, context=context)

        visual_prompt_references = state["visual_prompt_references"]

        rows = [
            (
                item["category"],
                item["participant_count"],
                item["prompt"],
                item["embedding"],
            )
            for item in visual_prompt_references
        ]

        success = await self._visual_prompt_reference_repository.save_all(rows)

        return success
