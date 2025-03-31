from fastapi import FastAPI, HTTPException
from src.agent import get_agent_response
from src.models import Query, AgentResponse

app = FastAPI()

@app.get("/")
async def root():
    return await get_agent_response()

@app.post("/query")
async def query(query: Query) -> AgentResponse:
    response = await get_agent_response(query.text)
    if response.data.get("status") == "error":
        raise HTTPException(status_code=500, detail=response.message)
    return response
