from agents.subgraphs.chat_rule_agent.llm import generate_chat_rule_llm
from agents.subgraphs.chat_rule_agent.prompts import (
    generate_chat_rule_instructions,
)
from agents.subgraphs.chat_rule_agent.state import Context, GraphState
from langgraph.runtime import Runtime


def generate_chat_rule(
    state: GraphState,
    runtime: Runtime[Context],
) -> dict:
    log_room_member_prompt = runtime.context.log_room_member_prompt
    example_dialogues = runtime.context.example_dialogues
    relationship = runtime.context.relationship

    formatted_prompt = generate_chat_rule_instructions.format(
        log_room_member_prompt=log_room_member_prompt,
        example_dialogues=example_dialogues,
        relationship=relationship,
    )

    response = generate_chat_rule_llm.invoke(formatted_prompt)
    return {"chat_rule": response.content}
