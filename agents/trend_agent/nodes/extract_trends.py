from agents.trend_agent.llm import extract_trends_llm
from agents.trend_agent.prompts import trend_extractor_instruction
from agents.trend_agent.state import GraphState, Trends



def extract_trends(state: GraphState) -> str:
    formatted_prompt = trend_extractor_instruction.format(
        current_month=state["current_month"], scraped_contents=state["scraped_contents"]
    )

    structured_model = extract_trends_llm.with_structured_output(Trends, method="json_schema")
    response = structured_model.invoke(formatted_prompt)
    return {"trends": response}
