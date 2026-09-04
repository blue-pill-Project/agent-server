from agents.character_chat_agent.llm import classify_intent_llm
from agents.character_chat_agent.state import GraphState, IntentDecision
from agents.character_chat_agent.prompts import classify_intent_instructions
from agents.character_chat_agent.state import Context
from langgraph.runtime import Runtime


def classify_intent(state: GraphState, runtime: Runtime[Context]) -> dict:
    last_message = state["messages"][-1]
    content = last_message.content
    log_room_member_prompt = runtime.context.log_room_member_prompt
    log_room_relationships = runtime.context.log_room_relationships

    formatted_prompt = classify_intent_instructions.format(
        content=content,
        log_room_member_prompt=log_room_member_prompt,
        log_room_relationships=log_room_relationships,
    )

    structured_model = classify_intent_llm.with_structured_output(IntentDecision)
    response = structured_model.invoke(formatted_prompt)
    print(f"💛: {response}")
    return {"intent_decision": response}
