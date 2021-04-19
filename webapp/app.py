import dash
import dash_bootstrap_components as dbc
import locale


locale.setlocale(locale.LC_ALL, '')
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.YETI])
server = app.server
app.config.suppress_callback_exceptions = True

import index