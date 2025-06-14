from fastapi import APIRouter, Request, Form
from twilio.twiml.messaging_response import MessagingResponse
from agents.weather_agent import WeatherAgent
from typing import List
from pydantic import BaseModel

router = APIRouter()

class Message(BaseModel):
    role: str
    content: str

@router.post("/whatsapp")
async def whatsapp_webhook(
    request: Request,
    Body: str = Form(...),
    From: str = Form(...)
):
    try:
        # Create a message for the agent
        message = Message(role="user", content=Body)
        
        # Process the message with our agent
        agent = WeatherAgent()
        response = await agent.process_messages([message])
        
        # Create Twilio response
        twiml = MessagingResponse()
        twiml.message(response)
        
        return str(twiml)
    except Exception as e:
        # In case of error, send a friendly message
        twiml = MessagingResponse()
        twiml.message("Lo siento, hubo un error procesando tu mensaje. Por favor, intenta de nuevo.")
        return str(twiml) 