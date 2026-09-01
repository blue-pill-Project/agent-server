from agents.base import BaseAgent
from agents.chat_rule_agent.graph import build_generate_chat_rule_graph
from agents.chat_rule_agent.state import Context
from domains.character.repository import CharacterRepository


class ChatRuleAgent(BaseAgent):
    def __init__(
        self,
        character_repository: CharacterRepository,
    ):
        super().__init__()
        self._character_repository = character_repository

    def build_graph(self):
        return build_generate_chat_rule_graph()

    async def run(self, character_id: str, relationship: str) -> str:
        character_prompt = await self._character_repository.get_prompt(character_id)
        example_dialogues = await self._character_repository.get_example_dialogues(
            character_id
        )
        context = Context(
            character_prompt=character_prompt,
            example_dialogues=example_dialogues,
            relationship=relationship,
        )

        state = await self.invoke({}, context=context)

        chat_rule = state["chat_rule"]

        return chat_rule
