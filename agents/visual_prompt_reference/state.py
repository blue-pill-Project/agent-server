from typing import TypedDict, Annotated
import operator
from dataclasses import dataclass

@dataclass
class Context:
    pinterest_url: str


class GraphState(TypedDict):
    pinterest_url: str
    image_urls: list[str]
    visual_prompt_references: Annotated[list[str], operator.add]
