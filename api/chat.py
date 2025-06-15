from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from agents.weather_agent import WeatherAgent

router = APIRouter()

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

class ChatResponse(BaseModel):
    response: str

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        agent = WeatherAgent()
        # Convert Pydantic models to dict for the agent
        messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
        response = await agent.process_messages(messages)
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 