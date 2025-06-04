from dash import Input, Output, State, html
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
        return "", "Архетип та тема обов'язкові.", history_data or []

    loading = dbc.Spinner(size="sm", color="primary", children="Генерація...")

    try:
        response = requests.post(f"{API_URL}/generate", json={
            "archetype": archetype,
            "topic": topic,
            "risk_level": risk or "medium",
            "memory": memory
        })
        response.raise_for_status()
        prompt = response.json()["prompt"]
    except requests.exceptions.ConnectionError:
        return "", "Помилка підключення до API. Переконайтесь, що сервер запущено.", history_data or []
    except requests.exceptions.RequestException as e:
        return "", f"Помилка API: {str(e)}", history_data or []
    except Exception as e:
        return "", f"Невідома помилка: {str(e)}", history_data or []

    history = history_data or []
    history.append({
        "archetype": archetype,
        "topic": topic,
        "risk": risk,
        "memory": memory or "",
        "prompt": prompt
    })
    if len(history) > 20:
        history = history[-20:]

    return "", prompt, history
