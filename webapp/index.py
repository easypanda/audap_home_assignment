import locale
from pathlib import Path

locale.setlocale(locale.LC_ALL, '')

# Dash visualización
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Plotly charts

from app import app
from pages import main_page, methodologie, navbar, data

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.joinpath('assets')

app.layout = html.Div([
    dcc.Location(id='url', refresh=True),
    html.Div([
        navbar.navbar,
        html.Div(id='page-content')
    ])
])


# Update the index
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/methodologie':
        return methodologie.layout

    elif pathname == '/data':
        return data.layout

    else:
        return main_page.layout
        # You could also return a 404 "URL not found" page  here


if __name__ == "__main__":
    app.run_server(debug=False, threaded=True, port=8080)
