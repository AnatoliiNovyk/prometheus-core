 # ui/app.py
from dash import Dash, html, dcc, Output, Input, State
import dash_bootstrap_components as dbc
from core.generator import build_prompt
from core.archetypes import load_archetypes

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Загружаем доступные архетипы
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
        ], width=4),
        dbc.Col([
            dbc.Label("Сгенерированный промпт"),
            dbc.Textarea(id="output", style={"height": "400px"}, readOnly=True),
        ], width=8)
    ])
], fluid=True)

@app.callback(
    Output("output", "value"),
    Input("generate", "n_clicks"),
    State("archetype", "value"),
    State("topic", "value"),
    State("risk", "value"),
    State("memory", "value"),
    prevent_initial_call=True
)
def generate_prompt(n_clicks, archetype, topic, risk, memory):
    if not archetype or not topic:
        return "Архетип и тема обязательны для генерации."
    try:
        prompt = build_prompt(archetype, topic, risk_level=risk, memory=memory)
        return prompt
    except Exception as e:
        return f"Ошибка генерации: {e}"

if __name__ == "__main__":
    app.run_server(debug=True)
