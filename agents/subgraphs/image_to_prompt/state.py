from enum import Enum
from pydantic import BaseModel, Field
from typing_extensions import TypedDict


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
    image_url: str
    image_base64: str
    image_prompt: ImagePrompt
    embedding: list[float]
