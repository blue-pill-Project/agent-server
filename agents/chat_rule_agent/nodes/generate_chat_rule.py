from agents.chat_rule_agent.llm import generate_chat_rule_llm
from agents.chat_rule_agent.prompts import (
    generate_chat_rule_instructions,
)
from agents.chat_rule_agent.state import Context, GraphState
from langgraph.runtime import Runtime


def format_example_dialogues(dialogues: list[str]) -> str:
    if not dialogues:
        return "대화 예시 없음"

    return "\n".join(f"- {dialogue}" for dialogue in dialogues)


def generate_chat_rule(
    state: GraphState,
    runtime: Runtime[Context],
) -> dict:
    character_prompt = runtime.context.character_prompt
    example_dialogues = runtime.context.example_dialogues
    relationship = runtime.context.relationship

    formatted_example_dialogues = format_example_dialogues(example_dialogues)

    formatted_prompt = generate_chat_rule_instructions.format(
        character_prompt=character_prompt,
        example_dialogues=formatted_example_dialogues,
        relationship=relationship,
    )

    response = generate_chat_rule_llm.invoke(formatted_prompt)
    return {"chat_rule": response.content}
