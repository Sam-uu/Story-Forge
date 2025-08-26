from pydantic import BaseModel, Field

class IntentRequest(BaseModel):
    requirement: str = Field(..., min_length=3)

class IntentResponse(BaseModel):
    intent: str

class StoryRequest(BaseModel):
    requirement: str = Field(..., min_length=3)

class StoryResponse(BaseModel):
    user_story: str

class AcceptanceRequest(BaseModel):
    requirement: str = Field(..., min_length=3)
    intent: str = Field(..., min_length=3)
    user_story: str = Field(..., min_length=3)

class AcceptanceResponse(BaseModel):
    acceptance_criteria: list[str]

class PipelineRequest(BaseModel):
    requirement: str = Field(..., min_length=3)

class PipelineResponse(BaseModel):
    intent: str
    user_story: str
    acceptance_criteria: list[str]
