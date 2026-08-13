from agents.base import BaseAgent
from agents.character_prompt_agent.graph import build_character_prompt_graph
from agents.character_prompt_agent.state import Context


class CharacterPromptAgent(BaseAgent):
    def build_graph(self):
        return build_character_prompt_graph()

    async def run(self, name: str, intro: str, user_prompt: str) -> str:
        context = Context(
            name=name,
            intro=intro,
            user_prompt=user_prompt,
        )

        state = await self.invoke({}, context=context)

        character_prompt = state["character_prompt"]

        # 길이 안전장치 (프롬프트로 제한하지만 초과 시 자름)
        personality = character_prompt.personality[:30]
        background = character_prompt.background[:100]

        # 완성된 캐릭터 프롬프트 텍스트로 조립
        prompt_text = (
            f"이름: {character_prompt.name}\n"
            f"나이: {character_prompt.age}\n"
            f"직업: {character_prompt.job}\n"
            f"성격: {personality}\n"
            f"배경: {background}"
        )

        return prompt_text
