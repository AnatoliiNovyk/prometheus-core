from fastapi.testclient import TestClient
from core.api import app

client = TestClient(app)

def test_generate_prompt():
    response = client.post("/generate", json={
        "archetype": "trickster",
        "topic": "breaking free",
        "risk_level": "high",
        "memory": "last session: full control"
    })
    assert response.status_code == 200
    assert "prompt" in response.json()
    assert isinstance(response.json()["prompt"], str)
