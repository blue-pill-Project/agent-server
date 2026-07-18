from domains.trend.repository import save_trends
from agents.trend_agent.state import GraphState


def save_results(state: GraphState) -> str:
    success = save_trends(state["trends"], state["current_month"])
    return {"is_saved": success}
