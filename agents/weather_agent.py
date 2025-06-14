import os
from typing import List, Dict, Any
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import tool
from langchain.smith import RunEvalConfig, run_on_dataset
from services.weather import WeatherService
from dotenv import load_dotenv

load_dotenv()

class WeatherAgent:
    def __init__(self):
        self.weather_service = WeatherService()
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            google_api_key=os.getenv("GEMINI_API_KEY"),
            temperature=0.7
        )
        
        # Define tools
        self.tools = [
            self.get_current_weather,
            self.get_forecast
        ]
        
        # Create prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """Eres un asistente especializado en el clima. 
            Puedes proporcionar información sobre el clima actual y pronósticos.
            Usa las herramientas disponibles para obtener información precisa.
            Responde siempre en español de manera amigable y concisa."""),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        # Create agent
        self.agent = create_openai_functions_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )
        
        # Create agent executor
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True
        )
    
    @tool
    async def get_current_weather(self, city: str) -> str:
        """Get current weather for a city"""
        try:
            data = await self.weather_service.get_current_weather(city)
            return self.weather_service.format_weather_response(data)
        except Exception as e:
            return f"Error al obtener el clima actual: {str(e)}"
    
    @tool
    async def get_forecast(self, city: str) -> str:
        """Get weather forecast for a city"""
        try:
            data = await self.weather_service.get_forecast(city)
            return self.weather_service.format_weather_response(data)
        except Exception as e:
            return f"Error al obtener el pronóstico: {str(e)}"
    
    async def process_messages(self, messages: List[Dict[str, str]]) -> str:
        """Process a list of messages and return a response"""
        try:
            # Extract the last user message
            last_message = messages[-1]["content"]
            
            # Run the agent
            response = await self.agent_executor.ainvoke({
                "input": last_message,
                "chat_history": messages[:-1]
            })
            
            return response["output"]
        except Exception as e:
            return f"Lo siento, hubo un error procesando tu mensaje: {str(e)}" 