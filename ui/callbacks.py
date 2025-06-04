from dash import Input, Output, State
import requests
import dash_bootstrap_components as dbc
from app import app
from config import API_URL

@app.callback(
    Output("loading-indicator", "children"),
    Output("output", "value"),
    Output("history-store", "data"),
    Input("generate", "n_clicks"),
    State("archetype", "value"),
    State("topic", "value"),
    State("risk", "value"),
    State("memory", "value"),
    State("history-store", "data"),
    prevent_initial_call=True
)
def generate_prompt_api(n_clicks, archetype, topic, risk, memory, history_data):
    if not archetype or not topic:
        return "", "Архетип и тема обязательны.", history_data or []

    loading = dbc.Spinner(size="sm", color="primary", children="Генерация...")

    try:
        response = requests.post(f"{API_URL}/generate", json={
            "archetype": archetype,
            "topic": topic,
            "risk_level": risk,
            "memory": memory
        })
        response.raise_for_status()
        prompt = response.json()["prompt"]
    except Exception as e:
        return "", f"Ошибка API: {e}", history_data or []

    history = history_data or []
    history.append({
        "archetype": archetype, "topic": topic, "risk": risk, "memory": memory or "", "prompt": prompt
    })
    if len(history) > 20:
        history = history[-20:]

    return "", prompt, history
