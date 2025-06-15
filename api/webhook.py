from fastapi import APIRouter, Request, Form
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from agents.weather_agent import WeatherAgent
from typing import List
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

# Initialize Twilio client
twilio_client = Client(
    os.getenv("TWILIO_ACCOUNT_SID"),
    os.getenv("TWILIO_AUTH_TOKEN")
)

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
        messages = [{"role": "user", "content": Body}]
        
        # Process the message with our agent
        agent = WeatherAgent()
        response = await agent.process_messages(messages)
        
        # Create Twilio response
        twiml = MessagingResponse()
        twiml.message(response)
        
        return str(twiml)
    except Exception as e:
        # In case of error, send a friendly message
        twiml = MessagingResponse()
        twiml.message(f"Sorry, there was an error processing your message: {str(e)}")
        return str(twiml)

@router.get("/whatsapp/status")
async def whatsapp_status():
    """Check WhatsApp connection status"""
    try:
        # Try to get account info to verify credentials
        account = twilio_client.api.accounts(os.getenv("TWILIO_ACCOUNT_SID")).fetch()
        return {
            "status": "connected",
            "account_sid": account.sid,
            "phone_number": os.getenv("TWILIO_PHONE_NUMBER")
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        } 