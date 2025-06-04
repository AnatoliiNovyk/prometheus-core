import dash
import dash_bootstrap_components as dbc
from layout import layout
import callbacks

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.CYBORG],
    suppress_callback_exceptions=True,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ]
)
app.title = "PROMETHEUS GODMODE"
app.layout = layout
server = app.server

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)
