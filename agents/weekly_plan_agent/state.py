from dataclasses import dataclass
import datetime
from pydantic import BaseModel, Field
from typing_extensions import TypedDict


@dataclass
class Context:
    user_id: str
    log_room_id: str
    log_room_member_id: str
    current_month: datetime.date
    current_date: datetime.date
    week_dates: list[dict]
    log_room_member_prompt: str
    trends: list[dict]


class DayInfo(BaseModel):
    date: datetime.date
    weekday: str


class Trend(BaseModel):
    """A Trend"""

    title: str = Field(description="The title of the trend")
    category: str = Field(description="The category of the trend")
    location: str = Field(description="The location of the trend")
    summary: str = Field(description="The summary of the trend")
    reason: str = Field(description="The reason for the trend")


class SelectedTrends(BaseModel):
    selected_trends: list[Trend] = Field(description="The list of selected trends")


class DailyPlan(BaseModel):
    """A DailyPlan"""

    date: datetime.date = Field(description="The date of the plan")
    day: str = Field(description="The day of the week")
    plan: str = Field(description="The description of the plan for the day")


class WeeklyPlan(BaseModel):
    daily_plans: list[DailyPlan] = Field(description="The Weekly plan")


class GraphState(TypedDict):
    current_month: str
    current_date: datetime.date
    week_dates: list[DayInfo]
    character_info: str
    history: str
    trends: str
    selected_trends: SelectedTrends
    weekly_plan: WeeklyPlan
    is_saved: bool
