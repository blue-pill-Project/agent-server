from agents.weekly_plan_agent.state import Context
from domains.trend.repository import save_trends
from agents.trend_agent.state import GraphState
from langgraph.runtime import Runtime


def save_results(state: GraphState, runtime: Runtime[Context]) -> str:
    current_month = runtime.context.current_month
    trends = state["trends"]

    success = save_trends(trends, current_month)
    return {"is_saved": success}
