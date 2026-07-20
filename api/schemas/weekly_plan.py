from pydantic import BaseModel


class WeeklyPlanRequest(BaseModel):
    user_id: str
    log_room_id: str
    log_room_member_id: str


class WeeklyPlanResponse(BaseModel):
    success: bool
