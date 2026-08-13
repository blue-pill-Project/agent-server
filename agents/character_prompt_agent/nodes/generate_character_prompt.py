from agents.character_prompt_agent.llm import generate_character_prompt_llm
from agents.character_prompt_agent.prompts import (
    generate_character_prompt_instructions,
)
from agents.character_prompt_agent.state import Context, CharacterPrompt, GraphState
from langgraph.runtime import Runtime


def generate_character_prompt(state: GraphState, runtime: Runtime[Context]) -> dict:
    name = runtime.context.name
    intro = runtime.context.intro
    user_prompt = runtime.context.user_prompt

    formatted_prompt = generate_character_prompt_instructions.format(
        name=name,
        intro=intro,
        user_prompt=user_prompt,
    )

    structured_model = generate_character_prompt_llm.with_structured_output(
        CharacterPrompt, method="json_schema"
    )
    response = structured_model.invoke(formatted_prompt)
    return {"character_prompt": response}
