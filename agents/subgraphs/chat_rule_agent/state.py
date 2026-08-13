from dataclasses import dataclass
from typing_extensions import TypedDict


@dataclass
class Context:
    log_room_member_prompt: str
    example_dialogues: str
    relationship: str


class GraphState(TypedDict):
    chat_rule: str
