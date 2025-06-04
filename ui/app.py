import dash
import dash_bootstrap_components as dbc
from layout import layout
import callbacks

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
app.layout = layout
server = app.server

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8050)
