from fastapi.testclient import TestClient
import main
app = main.app

def test_whatsapp_webhook():
    client = TestClient(app)
    response = client.post(
        "/webhook/whatsapp",
        data={"Body": "What is the weather in Madrid?", "From": "whatsapp:+1234567890"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    assert "Madrid" in response.text 