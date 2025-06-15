# WeatherBot Backend

A weather chatbot API using FastAPI, Langchain, and Gemini. This backend provides weather information through a REST API and WhatsApp integration.

## Features

- Weather information retrieval
- WhatsApp integration via Twilio
- OpenAI integration for natural language processing
- Docker support for easy deployment

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