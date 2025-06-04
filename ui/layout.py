from dash import dcc, html
import dash_bootstrap_components as dbc

layout = dbc.Container([
    html.H1("PROMETHEUS GODMODE", className="text-center"),
    dbc.Input(id="archetype", placeholder="Архетип"),
    dbc.Input(id="topic", placeholder="Тема"),
    dbc.Input(id="risk", placeholder="Уровень риска"),
    dbc.Textarea(id="memory", placeholder="Память"),
    dbc.Button("Сгенерировать", id="generate", n_clicks=0, className="mt-2"),
    html.Div(id="loading-indicator"),
    dbc.Textarea(id="output", rows=6, className="mt-2"),
    dcc.Store(id="history-store")
], fluid=True)
