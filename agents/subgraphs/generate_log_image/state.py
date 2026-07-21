from enum import Enum
from pydantic import BaseModel
from typing_extensions import TypedDict
from agents.daily_logs_agent.state import HourlyPlan


class ImageCategory(str, Enum):
    SOLO_PHOTO = "solo_photo"
    PAIR_PHOTO = "pair_photo"
    GROUP_PHOTO = "group_photo"
    FOOD_PHOTO = "food_photo"
    PLACE_PHOTO = "place_photo"
    OBJECT_PHOTO = "object_photo"


class ImageCategoryResult(BaseModel):
    image_category: ImageCategory


class GraphState(TypedDict):
    hourly_plan: HourlyPlan
    image_category: str
    generated_image_url: str
    # image_reference: dict
    image_prompt: str
    image_url: str
    image_base64: str
    saved_image_path: str
    log_image_url: str
