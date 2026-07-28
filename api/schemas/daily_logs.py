from pydantic import BaseModel


class DailyLogsRequest(BaseModel):
    timeslot: str  # "6", "9", "12", "15", "18", "21", "0", "3"
    user_id: str
    log_room_id: str
    log_room_member_id: str


class DailyLogsResponse(BaseModel):
    success: bool
