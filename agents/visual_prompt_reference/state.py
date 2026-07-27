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


class ShotSpec(BaseModel):
    category: ImagePromptCategory = Field(description="Main category of image")
    participant_count: int = Field(
        description="Number of main characters appearing in the image"
    )
    prompt: str = Field(
        description="Reusable filming-style prompt excluding character appearance, costume, props, and specific locations"
    )

class VisualPromptReference(BaseModel):
    category: ImagePromptCategory = Field(description="Main category of image")
    participant_count: int = Field(
        description="Number of main characters appearing in the image"
    )
    prompt: str = Field(
        description="Reusable filming-style prompt excluding character appearance, costume, props, and specific locations"
    )
    situation: str


class GraphState(TypedDict):
    shot_spec: ShotSpec
    situation: str
    visual_prompt_reference:VisualPromptReference
