from enum import Enum
from typing import TypedDict, Annotated
import operator
from dataclasses import dataclass
from pydantic import BaseModel, Field


@dataclass
class Context:
    image_bytes: bytes
    image_content_type: str


class ImagePromptCategory(str, Enum):
    SOLO_PHOTO = "solo_photo"
    PAIR_PHOTO = "pair_photo"
    GROUP_PHOTO = "group_photo"
    FOOD_PHOTO = "food_photo"
    PLACE_PHOTO = "place_photo"
    OBJECT_PHOTO = "object_photo"


class ImagePrompt(BaseModel):
    category: ImagePromptCategory = Field(description="Main category of image")
    participant_count: int = Field(
        description="Number of main characters appearing in the image"
    )
    prompt: str = Field(
        description="Reusable filming-style prompt excluding character appearance, costume, props, and specific locations"
    )


class GraphState(TypedDict):
    visual_prompt_reference: str
