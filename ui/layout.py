from dash import dcc, html
import dash_bootstrap_components as dbc

layout = dbc.Container([
    html.H1("PROMETHEUS GODMODE"),
    dbc.Input(id="archetype", placeholder="Архетип"),
    dbc.Input(id="topic", placeholder="Тема"),
    dbc.Input(id="risk", placeholder="Риск"),
    dbc.Textarea(id="memory", placeholder="Память"),
    dbc.Button("Сгенерировать", id="generate", n_clicks=0),
    html.Div(id="loading-indicator"),
    dbc.Textarea(id="output", rows=5),
    dcc.Store(id="history-store")
], fluid=True)
