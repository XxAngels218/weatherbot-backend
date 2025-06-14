from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.chat import router as chat_router
from api.webhook import router as webhook_router

app = FastAPI(
    title="WeatherBot API",
    description="A weather chatbot API using FastAPI, Langchain, and Gemini",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat_router, prefix="/api", tags=["chat"])
app.include_router(webhook_router, prefix="/webhook", tags=["webhook"])

@app.get("/")
async def root():
    return {"message": "Welcome to WeatherBot API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 