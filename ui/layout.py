from dash import dcc, html
import dash_bootstrap_components as dbc
from core.archetypes import load_archetypes

# Load archetypes for the dropdown
_archetype_options = []
_default_archetype = ""  # Initialize to a safe default for dbc.Select value prop

try:
    _archetypes_data = load_archetypes()  # Expected to return a dict {'Name': data}
    if _archetypes_data:
        _archetype_keys = list(_archetypes_data.keys())
        if _archetype_keys:  # If there are actual archetypes
            _archetype_options = [{"label": key, "value": key} for key in _archetype_keys]
            _default_archetype = _archetype_keys[0]  # Default to the first one
        else:  # archetypes.yaml might have 'archetypes:' but the list is empty
            _archetype_options = [{"label": "Архетипи не визначені", "value": "", "disabled": True}]
    else:  # load_archetypes() returned None or empty dict (e.g. file empty or 'archetypes' key missing)
        _archetype_options = [{"label": "Архетипи не завантажено", "value": "", "disabled": True}]
except FileNotFoundError:
    print("CRITICAL: Archetypes file not found for UI layout. Check presets/archetypes.yaml.")
    _archetype_options = [{"label": "Файл архетипів не знайдено", "value": "", "disabled": True}]
except Exception as e:
    # Catch other potential errors from load_archetypes (YAML parse, validation)
    print(f"CRITICAL: Error loading archetypes for UI layout: {e}")
    _archetype_options = [{"label": "Помилка завантаження архетипів", "value": "", "disabled": True}]

ARCHETYPE_OPTIONS = _archetype_options
DEFAULT_ARCHETYPE = _default_archetype

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("PROMETHEUS GODMODE", className="text-center mb-4"),
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Select(
                        id="archetype",
                        options=ARCHETYPE_OPTIONS,
                        value=DEFAULT_ARCHETYPE,
                        className="mb-3",
                    ),
                    dbc.Input(id="topic", placeholder="Тема", className="mb-3"),
                    dbc.Select(
                        id="risk",
                        options=[
                            {"label": "Низкий", "value": "low"},
                            {"label": "Середній", "value": "medium"},
                            {"label": "Максимальний", "value": "max"}
                        ],
                        value="medium",
                        className="mb-3"
                    ),
                    dbc.Textarea(id="memory", placeholder="Пам'ять", className="mb-3"),
                    dbc.Button("Згенерувати", id="generate", n_clicks=0, color="primary", className="w-100"),
                ])
            ], className="mb-4")
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div(id="loading-indicator"),
                    dbc.Textarea(id="output", rows=10, className="mt-2", style={"resize": "none"}),
                ])
            ])
        ], width=6)
    ]),
    dcc.Store(id="history-store")
], fluid=True, className="py-4")
