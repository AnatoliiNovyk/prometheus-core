from fastapi.testclient import TestClient
from core.api import app
from core.archetypes import load_archetypes

client = TestClient(app)

def test_generate_prompt():
    # Завантажуємо архетипи та отримуємо перший доступний
    archetypes = load_archetypes()
    test_archetype = next(iter(archetypes.keys()))
    
    response = client.post("/generate", json={
        "archetype": test_archetype,
        "topic": "breaking free",
        "risk_level": "max",  # Використовуємо допустиме значення
        "memory": "last session: full control"
    })
    assert response.status_code == 200
    assert "prompt" in response.json()
    assert isinstance(response.json()["prompt"], str)
