from dataclasses import dataclass
import datetime
from typing import Annotated, Any, Literal, NotRequired, TypedDict
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
    reranker: Any


class IntentDecision(BaseModel):
    intent: Literal["GENERAL_CHAT", "ACCEPT_REQUEST", "REFUSE_REQUEST"]
    request_summary: str
    reason: str


class GraphState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

    character_profile: dict
    relationship: str
    recent_summary: str

    long_term_memories: list[str]

    stored_memory_id: str | None
    system_prompt: str
    chat_rule: str
    intent_decision: IntentDecision
    search_results: list
    retrieved_memories: list[dict]
    is_saved_long_term_memory: bool
