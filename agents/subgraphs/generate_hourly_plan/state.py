from typing import NotRequired

from typing_extensions import TypedDict
from agents.daily_logs_agent.state import HourlyPlan, TimeSlot


class GraphState(TypedDict):
    character_info: str
    history: str
    daily_plan: str
    timeslot: TimeSlot
    today_chat: str
    related_chats: str
    previous_plans: list[HourlyPlan]
    long_term_memories: NotRequired[list[dict]]
    hourly_plan: HourlyPlan
