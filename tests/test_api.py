from fastapi.testclient import TestClient
from core.api import app
from core.archetypes import load_archetypes

client = TestClient(app)

# Завантажуємо архетипи та отримуємо перший доступний для тестів
archetypes = load_archetypes()
test_archetype = next(iter(archetypes.keys()))

# ✅ Позитивний тест — коректний запит
def test_generate_prompt_success():
    response = client.post("/generate", json={
        "archetype": test_archetype,
        "topic": "breaking free",
        "risk_level": "max",  # Використовуємо допустиме значення
        "memory": "last session: full control"
    })
    assert response.status_code == 200
    assert "prompt" in response.json()
    assert isinstance(response.json()["prompt"], str)

# ❌ Відсутній archetype
def test_missing_archetype():
    response = client.post("/generate", json={
        "topic": "hack system"
    })
    assert response.status_code == 422

# ❌ Відсутній topic
def test_missing_topic():
    response = client.post("/generate", json={
        "archetype": test_archetype
    })
    assert response.status_code == 422

# ❌ Некоректний тип risk_level
def test_invalid_risk_level_type():
    response = client.post("/generate", json={
        "archetype": test_archetype,
        "topic": "hack system",
        "risk_level": 123
    })
    assert response.status_code == 422

# ❌ Порожній JSON
def test_empty_request():
    response = client.post("/generate", json={})
    assert response.status_code == 422

# ✅ Перевірка, що memory можна не передавати
def test_memory_can_be_none():
    response = client.post("/generate", json={
        "archetype": test_archetype,
        "topic": "hack system"
    })
    assert response.status_code == 200
    assert "prompt" in response.json()
    assert isinstance(response.json()["prompt"], str)
