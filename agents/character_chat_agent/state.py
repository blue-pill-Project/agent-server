from dataclasses import dataclass
import datetime
from typing import Annotated, Literal, NotRequired, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from pydantic import BaseModel


@dataclass
class Context:
    user_id: str
    log_room_id: str
    log_room_member_id: str
    log_room_member_prompt: str
    log_room_relationships: str
    current_date: datetime.date
    now: datetime.date


class GraphState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

    character_profile: dict
    relationship: str
    recent_summary: str

    long_term_memories: list[str]

    stored_memory_id: str | None
    system_prompt: str

    is_saved_long_term_memory: bool
