from typing import NotRequired

from typing_extensions import TypedDict
from agents.daily_logs_agent.state import HourlyPlan, TimeSlot


class GraphState(TypedDict):
    long_term_memories: list[str] | None
    hourly_plan: HourlyPlan
