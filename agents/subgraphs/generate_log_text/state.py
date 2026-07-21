from typing_extensions import TypedDict
from agents.daily_logs_agent.state import HourlyPlan, LogText


class GraphState(TypedDict):
    hourly_plan: HourlyPlan
    log_text: LogText
