from pydantic import BaseModel


class ChatRuleRequest(BaseModel):
    character_id: str
    relationship: str


class ChatRuleResponse(BaseModel):
    chat_rule: str
