from pydantic import BaseModel


class CharacterChatRequest(BaseModel):
    log_room_id: str
    log_room_member_id: str
    user_id: str
    content: str


class CharacterChatResponse(BaseModel):
    reply: str
