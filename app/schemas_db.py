# agile-assistant/app/schemas_db.py
from pydantic import BaseModel
from typing import List

class CardBase(BaseModel):
    intent: str
    user_story: str
    acceptance_criteria: List[str]

class CardCreate(CardBase):
    pass

class CardResponse(CardBase):
    id: int

    class Config:
        orm_mode = True
