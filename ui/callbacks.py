from dash import Input, Output, State
import requests
import dash_bootstrap_components as dbc
from app import app  # если app создан в app.py

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
def generate_prompt_api(...):
    ...
