import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_chat_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/chat", json={
            "messages": [{"role": "user", "content": "What is the weather in Paris?"}]
        })
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert "Paris" in data["response"] 