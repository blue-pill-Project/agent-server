from agents.subgraphs.generate_log_text.llm import generate_log_text_llm
from agents.subgraphs.generate_log_text.state import LogText, GraphState
from agents.daily_logs_agent.state import Context
from langgraph.runtime import Runtime
from agents.subgraphs.generate_log_text.prompts import (
    generate_log_text_instructions,
)


def generate_log_text(state: GraphState, runtime: Runtime[Context]) -> dict:
    log_room_member_prompt = runtime.context.log_room_member_prompt
    hourly_plan = state["hourly_plan"]

    formatted_prompt = generate_log_text_instructions.format(
        log_room_member_prompt=log_room_member_prompt, hourly_plan=hourly_plan
    )
    structured_model = generate_log_text_llm.with_structured_output(LogText)
    response = structured_model.invoke(formatted_prompt)
    return {"log_text": response}
