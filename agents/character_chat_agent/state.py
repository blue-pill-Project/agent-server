from dataclasses import dataclass
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


class MemoryDecision(BaseModel):
    should_save: bool
    content: str | None
    reason: str
    memory_type: Literal[
        "user_preference",
        "relationship",
        "constraint",
        "feedback",
        "none",
    ] = "none"


class GraphState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

    character_profile: dict
    relationship: str
    recent_summary: str

    memory_decision: MemoryDecision
    stored_memory_id: str | None
    system_prompt: str
