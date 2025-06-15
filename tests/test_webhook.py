import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_whatsapp_webhook():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/webhook/whatsapp",
            data={"Body": "What is the weather in Madrid?", "From": "whatsapp:+1234567890"},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        assert response.status_code == 200
        assert "Madrid" in response.text 