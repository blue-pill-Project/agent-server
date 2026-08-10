from agents.character_chat_agent.llm import generate_reply_llm
from agents.character_chat_agent.state import GraphState, IntentDecision
from agents.character_chat_agent.prompts import classify_intent_instructions


def classify_intent(state: GraphState) -> dict:
    last_message = state["messages"][-1]
    content = last_message.content

    formatted_prompt = classify_intent_instructions.format(content=content)

    structured_model = generate_reply_llm.with_structured_output(IntentDecision)
    response = structured_model.invoke(formatted_prompt)
    print(f"💛: {response}")
    return {"intent_decision": response}
