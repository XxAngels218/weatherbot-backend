from fastapi.testclient import TestClient
import main
app = main.app

def test_chat_endpoint():
    client = TestClient(app)
    response = client.post("/api/chat", json={
        "messages": [{"role": "user", "content": "What is the weather in Paris?"}]
    })
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "Paris" in data["response"] 