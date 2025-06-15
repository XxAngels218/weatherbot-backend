import os
from typing import List, Dict, Any
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import tool
from langchain.smith import RunEvalConfig, run_on_dataset
from langchain.callbacks.tracers import LangChainTracer
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.tracers.langchain import LangChainTracer
from langchain.callbacks.tracers.run_collector import RunCollectorCallbackHandler
from langchain.smith import RunEvalConfig, run_on_dataset
from services.weather import WeatherService
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
import asyncio

load_dotenv()

# Configure LangSmith
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = "weatherbot"

# Create a tracer
tracer = LangChainTracer()
run_collector = RunCollectorCallbackHandler()
callback_manager = CallbackManager([tracer, run_collector])

# Instantiate the weather service once
weather_service = WeatherService()

@tool
async def get_current_weather(city: str) -> str:
    """Get current weather for a city"""
    try:
        data = await weather_service.get_current_weather(city)
        return weather_service.format_weather_response(data)
    except Exception as e:
        return f"Error getting current weather: {str(e)}"

@tool
async def get_forecast(city: str) -> str:
    """Get weather forecast for a city"""
    try:
        data = await weather_service.get_forecast(city)
        return weather_service.format_weather_response(data)
    except Exception as e:
        return f"Error getting forecast: {str(e)}"

class WeatherAgent:
    def __init__(self):
        # Initialize OpenAI model with LangSmith tracing
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7,
            callbacks=callback_manager
        )
        
        # Define tools
        self.tools = [get_current_weather, get_forecast]
        
        # Create prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful weather assistant. You can help users get weather information.
            Use the available tools to get accurate information.
            Always respond in a friendly and concise manner."""),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        # Create agent with tracing
        self.agent = create_openai_functions_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )
        
        # Create agent executor with tracing
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True,
            callbacks=callback_manager
        )
    
    async def process_messages(self, messages: List[Dict[str, str]]) -> str:
        """
        Process a list of messages and return a response.
        The last message is the user input, the rest is chat history.
        """
        try:
            print("[DEBUG] messages:", messages)
            
            # Convert chat history to Langchain message objects
            chat_history = []
            for m in messages[:-1]:
                if m["role"] == "user":
                    chat_history.append(HumanMessage(content=m["content"]))
                elif m["role"] == "assistant":
                    chat_history.append(AIMessage(content=m["content"]))
            
            last_message = messages[-1]["content"]
            print("[DEBUG] chat_history:", chat_history)
            print("[DEBUG] last_message:", last_message)

            # Run the agent in an event loop
            loop = asyncio.get_event_loop()
            response = await loop.create_task(
                self.agent_executor.ainvoke({
                    "input": last_message,
                    "chat_history": chat_history
                })
            )

            return response["output"]
        except Exception as e:
            print("[ERROR]", str(e))
            return f"Sorry, there was an error processing your message: {str(e)}" 