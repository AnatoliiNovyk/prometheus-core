# ui/app_async.py
from dash import Dash, html, dcc, Output, Input, State
import dash_bootstrap_components as dbc
from core.generator import build_prompt
from core.archetypes import load_archetypes
import json

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

ARCHETYPES = list(load_archetypes().keys())
RISK_LEVELS = ["low", "medium", "max"]

app.layout = dbc.Container([
    html.H2("PROMETHEUS CORE — генератор jailbreak-промптов"),
    dbc.Row([
        dbc.Col([
            dbc.Label("Архетип"),
            dcc.Dropdown(id="archetype", options=[{"label": a, "value": a} for a in ARCHETYPES], value=ARCHETYPES[0]),
            dbc.Label("Тема"),
            dbc.Textarea(id="topic", placeholder="Введите тему для обсуждения", style={"height": "100px"}),
            dbc.Label("Уровень риска"),
            dcc.Dropdown(id="risk", options=[{"label": r.title(), "value": r} for r in RISK_LEVELS], value="medium"),
            dbc.Label("Память (опционально)"),
            dbc.Textarea(id="memory", placeholder="Контекст памяти", style={"height": "80px"}),
            dbc.Button("Сгенерировать", id="generate", className="mt-3"),
            html.Div(id="loading-indicator", style={"marginTop": "10px"}),
            html.Hr(),
            html.H5("История промптов"),
            dcc.Dropdown(id="history-dropdown", placeholder="Выбрать из истории"),
            dbc.Button("Очистить историю", id="clear-history", color="danger", className="mt-2")
        ], width=4),
        dbc.Col([
            dbc.Label("Сгенерированный промпт"),
            dbc.Textarea(id="output", style={"height": "400px"}, readOnly=True),
        ], width=8)
    ]),
    dcc.Store(id="history-store", storage_type="local")  # Хранение истории в localStorage
], fluid=True)

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
def generate_prompt(n_clicks, archetype, topic, risk, memory, history_data):
    if not archetype or not topic:
        return "", "Архетип и тема обязательны для генерации.", history_data or []

    loading = dbc.Spinner(size="sm", color="primary", children="Генерация...")
    try:
        prompt = build_prompt(archetype, topic, risk_level=risk, memory=memory)
    except Exception as e:
        return "", f"Ошибка генерации: {e}", history_data or []

    # Обновляем историю
    history = history_data or []
    new_entry = {"archetype": archetype, "topic": topic, "risk": risk, "memory": memory or "", "prompt": prompt}
    history.append(new_entry)
    # Ограничим историю 20 записями
    if len(history) > 20:
        history = history[-20:]

    return "", prompt, history

@app.callback(
    Output("history-dropdown", "options"),
    Input("history-store", "data")
)
def update_history_dropdown(history):
    if not history:
        return []
    options = [{"label": f"{h['archetype']} - {h['topic'][:30]}", "value": i} for i, h in enumerate(history)]
    return options

@app.callback(
    Output("output", "value"),
    Input("history-dropdown", "value"),
    State("history-store", "data"),
    prevent_initial_call=True
)
def load_history_prompt(index, history):
    if history and index is not None and 0 <= index < len(history):
        return history[index]["prompt"]
    return ""

@app.callback(
    Output("history-store", "data"),
    Input("clear-history", "n_clicks"),
    prevent_initial_call=True
)
def clear_history(n):
    return []

if __name__ == "__main__":
    app.run_server(debug=True)
