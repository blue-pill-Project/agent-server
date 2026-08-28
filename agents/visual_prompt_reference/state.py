from enum import Enum
from typing import TypedDict
from dataclasses import dataclass
from pydantic import BaseModel, Field


@dataclass(frozen=True)
class VisualPromptReferenceForSave:
    category: str
    camera_style: str
    participant_count: int
    image_key: str
    situation: str
    situation_embedding: list[float]
    is_default_selfie: bool


@dataclass
class Context:
    image_bytes: bytes
    image_content_type: str
    is_default: bool


class ImagePromptCategory(str, Enum):
    SOLO_PHOTO = "solo_photo"
    PAIR_PHOTO = "pair_photo"
    GROUP_PHOTO = "group_photo"
    FOOD_PHOTO = "food_photo"
    PLACE_PHOTO = "place_photo"
    OBJECT_PHOTO = "object_photo"


class CameraStyle(str, Enum):
    SELFIE = "selfie"
    THIRD_PERSON = "third_person"
    POV = "pov"


class VisualPromptReferenceInfo(BaseModel):
    category: ImagePromptCategory = Field(description="Main category of image")
    camera_style: CameraStyle
    participant_count: int = Field(
        description="Number of main characters appearing in the image"
    )
    situation: str


class GraphState(TypedDict):
    visual_prompt_reference_info: VisualPromptReferenceInfo
