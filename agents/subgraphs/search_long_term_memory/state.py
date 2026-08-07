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
    now: datetime.datetime


class Source(BaseModel):
    purpose: Literal["chat", "post"]
    source: str


class RetrievalQuery(BaseModel):
    should_search: bool
    retrieval_query: str | None
    kind_hint: Literal[
        "semantic",
        "episodic",
        "all",
    ]


class SourceType(StrEnum):
    CHAT = "chat"
    LOG = "log"


class MemoryKind(StrEnum):
    SEMANTIC = "semantic"
    EPISODIC = "episodic"


class SearchResult(BaseModel):
    kind: MemoryKind
    source_type: SourceType
    content: str
    occurred_at: datetime.date

class RerankedResults(BaseModel):
    reranked_results: list[SearchResult]


class GraphState(TypedDict):
    source: Source
    retrieval_query: RetrievalQuery
    search_results: list[SearchResult] | None
    reranked_results: list[SearchResult] | None
