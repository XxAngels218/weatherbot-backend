# WeatherBot Backend

A weather chatbot API using FastAPI, Langchain, and Gemini. This backend provides weather information through a REST API and WhatsApp integration.

## Features

- Weather information retrieval
- WhatsApp integration via Twilio
- OpenAI integration for natural language processing
- Docker support for easy deployment
- **Observability with LangSmith** (see below)

## Prerequisites

- Python 3.10 or higher
- Docker and Docker Compose
- Twilio account (for WhatsApp integration)
- OpenAI API key
- OpenWeather API key
- Langchain API key

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
OPENWEATHER_API_KEY=your_openweather_api_key
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number
LANGCHAIN_API_KEY=your_langchain_api_key
LANGCHAIN_PROJECT=weatherbot
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
OPENAI_API_KEY=your_openai_api_key
```

## Local Development Setup

1. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the development server:
```bash
python main.py
```

The server will be available at `http://localhost:8000`

## Docker Setup

1. Build the Docker image:
```bash
docker build -t weatherbot-backend .
```

2. Run the container:
```bash
docker run -p 8000:8000 \
  -e OPENWEATHER_API_KEY=your_openweather_api_key \
  -e TWILIO_ACCOUNT_SID=your_twilio_account_sid \
  -e TWILIO_AUTH_TOKEN=your_twilio_auth_token \
  -e TWILIO_PHONE_NUMBER=your_twilio_phone_number \
  -e LANGCHAIN_API_KEY=your_langchain_api_key \
  -e LANGCHAIN_PROJECT=weatherbot \
  -e LANGCHAIN_ENDPOINT=https://api.smith.langchain.com \
  -e OPENAI_API_KEY=your_openai_api_key \
  weatherbot-backend
```

## API Endpoints

### Chat Endpoint
```bash
POST /api/chat
Content-Type: application/json

{
    "messages": [
        {
            "role": "user",
            "content": "What is the weather like in New York?"
        }
    ]
}
```

### WhatsApp Webhook
```bash
POST /webhook/whatsapp
Content-Type: application/x-www-form-urlencoded

Body=What is the weather like in New York?&From=whatsapp:+1234567890
```

### WhatsApp Status
```bash
GET /webhook/whatsapp/status
```

## Testing the API

1. Test the chat endpoint:
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "What is the weather like in New York?"}]}'
```

2. Test the WhatsApp webhook:
```bash
curl -X POST "http://localhost:8000/webhook/whatsapp" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "Body=What is the weather like in New York?&From=whatsapp:+1234567890"
```

## Automated Tests

This project includes automated tests to ensure the core functionality of the WeatherBot backend:

- Tests cover the chat API, WhatsApp webhook, and weather service integration.
- To run the tests locally:

```bash
pytest
```

- Make sure to install the development dependencies:
```bash
pip install -r requirements.txt
```

Test results will be shown in the terminal. You can add more tests in the `tests/` directory. 

## Deployment

The application is containerized and can be deployed to any cloud platform that supports Docker containers (e.g., Render.com, Heroku, AWS, etc.).

### Deploying to Render.com

1. Create a new Web Service
2. Connect your GitHub repository
3. Configure the following:
   - Build Command: `docker build -t weatherbot-backend .`
   - Start Command: `docker run -p 8000:8000 --env-file .env weatherbot-backend`
4. Add all environment variables from your `.env` file in the Render dashboard
5. Deploy!

## Project Structure

```
weatherbot-backend/
├── api/
│   ├── chat.py
│   └── webhook.py
├── agents/
│   └── weather_agent.py
├── services/
│   └── weather.py
├── main.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
└── README.md
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Observability with LangSmith

WeatherBot includes full observability and tracing using [LangSmith](https://smith.langchain.com/):

- **Conversation Tracing:** Every user interaction is logged as a trace.
- **Token Usage & Latency:** Monitor tokens, costs, and response times.
- **Error Tracking:** All errors and exceptions are visible in the dashboard.
- **External API Calls:** See all weather and LLM calls.

**Example LangSmith Dashboard:**
![LangSmith Dashboard](./docs/screenshots/langsmith_dashboard.png)
*You can see each run, input/output, latency, tokens, and errors for every conversation.*

## Live Deployment on Render

WeatherBot is deployed and running on [Render.com](https://render.com/):

- **Production URL:**  
  [https://weatherbot-backend-go0c.onrender.com](https://weatherbot-backend-go0c.onrender.com)

**Example Render Service Settings:**
![Render Service Settings](./docs/screenshots/render_settings.png)

**Example Render Logs:**
![Render Logs](./docs/screenshots/render_logs.png)

## Try it on WhatsApp

You can test WeatherBot directly from WhatsApp using the Twilio Sandbox:

1. **Join the Sandbox:**  
   Send the code shown in your Twilio console to  
   `+1 415 523 8886`  
   ![Twilio Sandbox Join](./docs/screenshots/twilio_sandbox_join.png)

2. **Send a message:**  
   Ask for the weather, e.g. `What is the weather in London?`  
   > ⚠️ The first response may take up to 1 minute due to server cold start.

**Example WhatsApp Conversation:**
![WhatsApp Conversation](./docs/screenshots/whatsapp_conversation.png)

**Twilio Messaging Logs:**
![Twilio Messaging Logs](./docs/screenshots/twilio_logs.png)

## Application Flow

The application follows this flow for every user interaction:

1. **User sends a message** via WhatsApp (or API).
2. **Twilio** receives the message and forwards it to the webhook endpoint (`/webhook/whatsapp`).
3. **FastAPI backend** receives the webhook, extracts the message, and passes it to the WeatherAgent.
4. **WeatherAgent**:
    - Uses LangChain and OpenAI to interpret the user's intent.
    - If weather data is needed, calls the OpenWeather API.
    - Constructs a friendly, concise response.
    - All steps are traced and logged in LangSmith for observability.
5. **Backend returns a TwiML XML response** to Twilio.
6. **Twilio delivers the response** back to the user on WhatsApp.
7. **All interactions** (inputs, outputs, errors, latency, token usage) are visible in LangSmith for monitoring and debugging.

**Visual Flow:**
1. ![LangSmith Dashboard](./docs/screenshots/langsmith_dashboard.png) — See all traces and details.
2. ![Render Logs](./docs/screenshots/render_logs.png) — Monitor backend logs and status.
3. ![WhatsApp Conversation](./docs/screenshots/whatsapp_conversation.png) — Example user interaction.

