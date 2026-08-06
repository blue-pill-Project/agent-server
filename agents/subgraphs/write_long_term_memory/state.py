from enum import StrEnum
from typing import Literal
from typing_extensions import TypedDict
from pydantic import BaseModel, Field
import datetime
from dataclasses import dataclass


@dataclass
class Context:
    user_id: str
    log_room_id: str
    log_room_member_id: str


class SourceType(StrEnum):
    CHAT = "chat"
    LOG = "log"


class MemoryKind(StrEnum):
    SEMANTIC = "semantic"
    EPISODIC = "episodic"


class MemorySource(BaseModel):
    source_type: SourceType
    source: str
    occurred_at: datetime.date


class MemoryValue(BaseModel):
    kind: MemoryKind
    source_type: SourceType
    content: str
    occurred_at: datetime.date


class Memories(BaseModel):
    memories: list[MemoryValue]


class GraphState(TypedDict):
    memory_source: MemorySource
    memories: Memories
    success: bool
