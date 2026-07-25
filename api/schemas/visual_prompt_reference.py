from pydantic import BaseModel


class VisualPromptReferenceRequest(BaseModel):
    pinterest_url: str


class VisualPromptReferenceResponse(BaseModel):
    success: bool
