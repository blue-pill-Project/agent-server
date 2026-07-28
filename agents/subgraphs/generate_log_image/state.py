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
# 1. build_visual_prompt_reference_search_query 해당 노드 쓸지 모르겠음
# 2. classify_image_category는 우선 SOLO 사진 즉, 인물이 하나만 나오는 사진만 검색하기 위해 비활성화
class GraphState(TypedDict):
    hourly_plan: HourlyPlan
    # image_category: str
    generated_image_url: str
    image_reference: dict
    image_prompt: str
    image_base64: str
    saved_image_path: str
    log_image_url: str
    # visual_prompt_reference_search_query: str
