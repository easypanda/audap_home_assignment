import os
from pathlib import Path
import dash_bootstrap_components as dbc
import dash_html_components as html

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR.joinpath('assets')

layout = dbc.Container([
    dbc.Col([
    html.Br(),
    html.Iframe(
        src=os.path.join("assets", "methodologie.html"),
        style={'height': '1067px',
               'width': '100%'}
                ),
            ])
],fluid=True)