# WeatherBot Backend

Un chatbot de clima inteligente construido con FastAPI, Langchain y Gemini API.

## Características

- 🤖 Chatbot de clima usando Gemini API
- 🌤️ Integración con OpenWeather API
- 📱 Soporte para WhatsApp a través de Twilio
- 📊 Observabilidad con LangSmith
- 🐳 Despliegue fácil con Docker
- 🚀 Configuración para Render.com

## Requisitos

- Python 3.11+
- Cuenta de Google Cloud (para Gemini API)
- Cuenta de OpenWeather
- Cuenta de Twilio (opcional, para WhatsApp)
- Cuenta de LangSmith (opcional, para observabilidad)

## Configuración

1. Clona el repositorio:
```bash
git clone https://github.com/yourusername/weatherbot-backend.git
cd weatherbot-backend
```

2. Crea un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

4. Copia el archivo .env.example a .env y configura las variables:
```bash
cp .env.example .env
```

5. Edita el archivo .env con tus claves API:
```bash
GEMINI_API_KEY=tu_clave_de_gemini
OPENWEATHER_API_KEY=tu_clave_de_openweather
TWILIO_AUTH_TOKEN=tu_token_de_twilio
LANGCHAIN_API_KEY=tu_clave_de_langsmith
```

## Ejecución Local

```bash
uvicorn main:app --reload
```

El servidor estará disponible en `http://localhost:8000`

## Endpoints

### Chat API
- `POST /api/chat`: Endpoint para interactuar con el chatbot
  ```json
  {
    "messages": [
      {"role": "user", "content": "¿Cómo está el clima en Madrid?"}
    ]
  }
  ```

### Webhook WhatsApp
- `POST /webhook/whatsapp`: Endpoint para recibir mensajes de WhatsApp a través de Twilio

## Despliegue en Render

1. Crea una cuenta en [Render](https://render.com)
2. Conecta tu repositorio de GitHub
3. Crea un nuevo Web Service
4. Configura las variables de entorno en el dashboard de Render
5. ¡Listo! Tu aplicación se desplegará automáticamente

## Estructura del Proyecto

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

## Contribuir

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles. 