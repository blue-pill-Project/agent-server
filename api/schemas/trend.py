from pydantic import BaseModel


class TrendResponse(BaseModel):
    is_saved: bool
