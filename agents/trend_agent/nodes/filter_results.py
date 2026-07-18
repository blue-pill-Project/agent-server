from agents.trend_agent.llm import filter_results_llm
from agents.trend_agent.prompts import result_filter_instruction
from agents.trend_agent.state import GraphState, FilteredResults


def filter_results(state: GraphState) -> FilteredResults:
    formatted_prompt = result_filter_instruction.format(raw_trend_results_with_naver_blog=state["raw_trend_results_with_naver_blog"])

    structured_model = filter_results_llm.with_structured_output(
        FilteredResults, method="json_schema"
    )
    response = structured_model.invoke(formatted_prompt)
    return {"filtered_results": response}
