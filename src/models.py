from pydantic import BaseModel

class Query(BaseModel):
    text: str

class AgentResponse(BaseModel):
    message: str
    data: dict
