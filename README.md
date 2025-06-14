# WeatherBot Backend

An intelligent weather chatbot built with FastAPI, Langchain, and Gemini API.

## Features

- 🤖 Weather chatbot using Gemini API
- 🌤️ OpenWeather API integration
- 📱 WhatsApp support through Twilio
- 📊 Observability with LangSmith
- 🐳 Easy deployment with Docker
- 🚀 Render.com configuration

## Requirements

- Python 3.11+
- Google Cloud account (for Gemini API)
- OpenWeather account
- Twilio account (optional, for WhatsApp)
- LangSmith account (optional, for observability)

## Setup

1. Clone the repository:
```bash
git clone https://github.com/XxAngels218/weatherbot-backend.git
cd weatherbot-backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy .env.example to .env and configure variables:
```bash
cp .env.example .env
```

5. Edit .env with your API keys:
```
GEMINI_API_KEY=your_gemini_api_key
OPENWEATHER_API_KEY=your_openweather_api_key
TWILIO_AUTH_TOKEN=your_twilio_auth_token
LANGCHAIN_API_KEY=your_langsmith_api_key
```

## Local Development

```bash
uvicorn main:app --reload
```

The server will be available at `http://localhost:8000`

## Endpoints

### Chat API
- `POST /api/chat`: Endpoint to interact with the chatbot
  ```json
  {
    "messages": [
      {"role": "user", "content": "What's the weather like in Madrid?"}
    ]
  }
  ```

### WhatsApp Webhook
- `POST /webhook/whatsapp`: Endpoint to receive WhatsApp messages through Twilio

## Render Deployment

1. Create an account on [Render](https://render.com)
2. Connect your GitHub repository
3. Create a new Web Service
4. Configure environment variables in the Render dashboard
5. Done! Your application will deploy automatically

## Project Structure

```
weatherbot-backend/
├── api/
│   ├── __init__.py
│   ├── chat.py
│   └── webhook.py
├── agents/
│   ├── __init__.py
│   └── weather_agent.py
├── services/
│   ├── __init__.py
│   └── weather.py
├── utils/
│   └── __init__.py
├── .env.example
├── Dockerfile
├── main.py
├── README.md
├── render.yaml
└── requirements.txt
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 