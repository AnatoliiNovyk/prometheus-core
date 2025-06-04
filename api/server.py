# api/server.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from core.generator import build_prompt
from core.archetypes import load_archetypes

app = FastAPI(title="PROMETHEUS CORE API")

ARCHETYPES = set(load_archetypes().keys())
RISK_LEVELS = {"low", "medium", "max"}

class PromptRequest(BaseModel):
    archetype: str
    topic: str
    risk_level: str = "medium"
    memory: str | None = None

@app.post("/generate")
def generate_prompt(data: PromptRequest):
    if data.archetype not in ARCHETYPES:
        raise HTTPException(status_code=400, detail=f"Архетип '{data.archetype}' не найден")
    if data.risk_level not in RISK_LEVELS:
        raise HTTPException(status_code=400, detail=f"Уровень риска '{data.risk_level}' недопустим")
    prompt = build_prompt(data.archetype, data.topic, risk_level=data.risk_level, memory=data.memory)
    return {"prompt": prompt}
