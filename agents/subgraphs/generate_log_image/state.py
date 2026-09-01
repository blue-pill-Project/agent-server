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


# NOTE:
# 1. classify_image_category는 우선 SOLO 사진 즉, 인물이 하나만 나오는 사진만 검색하기 위해 비활성화
class GraphState(TypedDict):
    hourly_plan: HourlyPlan
    # image_category: str
    generated_image_url: str
    image_prompt: str
    image_base64: str
    saved_image_path: str
    log_image_url: str
    image_references: list[dict] | None
    image_reference: dict | None
    image_reference_image_url: str | None
    visual_scene: str
    use_default_reference: bool
