from pydantic import BaseModel


class CharacterPromptRequest(BaseModel):
    name: str
    intro: str
    user_prompt: str = ""


class CharacterPromptResponse(BaseModel):
    prompt: str
