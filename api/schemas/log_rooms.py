from pydantic import BaseModel


class LogRoomDeleteResponse(BaseModel):
    success: bool
