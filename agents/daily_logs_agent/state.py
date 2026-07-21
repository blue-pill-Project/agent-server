from dataclasses import dataclass
import datetime
from typing import NotRequired

from typing_extensions import TypedDict, Literal
from pydantic import BaseModel, Field
# from src.graphs.subgraphs.generate_log_image.state import GraphState

TimeSlot = Literal["6", "9", "12", "15", "18", "21", "0", "3"]


@dataclass
class Context:
    user_id: str
    log_room_id: str
    log_room_member_id: str
    current_month: datetime.date
    current_date: datetime.date
    timeslot: str
    previous_plans: list[HourlyPlan]
    log_room_member_prompt: str
    today_plan: str
    image_url: str


class HourlyPlan(BaseModel):
    """하루 중 한 시간대(3시간 단위)의 계획"""

    timeslot: TimeSlot = Field(
        description="시간대 시작 시각 (6, 9, 12, 15, 18, 21, 0, 3 중 하나)"
    )
    title: str = Field(description="그 시간대 활동의 제목")
    description: str = Field(description="그 시간대 활동에 대한 설명")
    outfit: str = Field(description="그 시간대 캐릭터의 착장(옷차림)")
    location: str = Field(description="그 시간대의 장소")


class LogText(BaseModel):
    """한 시간대의 활동을 캐릭터 시점으로 서술한 로그"""

    timeslot: TimeSlot = Field(
        description="시간대 시작 시각 (6, 9, 12, 15, 18, 21, 0, 3 중 하나)"
    )
    log_text: str = Field(
        description="그 시간대에 일어난 일을 캐릭터의 말투와 시점으로 서술한 로그 텍스트"
    )


class HourlyLog(BaseModel):
    """한 시간대의 활동을 캐릭터가 올린 로그"""

    timeslot: TimeSlot = Field(
        description="시간대 시작 시각 (6, 9, 12, 15, 18, 21, 0, 3 중 하나)"
    )
    hourly_plan: HourlyPlan = Field(description="그 시간대 일어난 사건")
    log_image_url: str = Field(description="그 시간대에 캐릭터가 찍은 사진")
    log_text: LogText = Field(
        description="그 시간대에 일어난 일을 캐릭터의 말투와 시점으로 서술한 로그 텍스트"
    )


class DayInfo(BaseModel):
    date: datetime.date
    weekday: str


class GraphState(TypedDict):
    current_month: str
    current_date: datetime.date
    week_dates: list[DayInfo]
    character_info: str
    image_url: str
    history: str
    daily_plan: str
    timeslot: TimeSlot
    today_chat: str
    related_chats: str
    previous_plans: list[HourlyPlan]
    long_term_memories: NotRequired[list[dict]]
    hourly_plan: HourlyPlan
    log_text: LogText
    hourly_log: HourlyLog
    log_image_url: str
