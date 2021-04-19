from pathlib import Path
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_table
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR.joinpath('assets')
df = pd.read_csv(DATA_DIR / "data.csv",index_col=0)

data_table = dash_table.DataTable(
    id='datatable-interactivity',
    columns=[
        {"name": i.capitalize(), "id": i, "deletable": False, "selectable": True} for i in df.columns
    ],
    data=df.to_dict('records'),
    editable=False,
    filter_action="native",
    sort_action="native",
    sort_mode="multi",
    filter_query='',
    style_cell={
        'overflow': 'hidden',
        'textOverflow': 'ellipsis',
        'maxWidth': 400
    },
    style_table={'overflowX': 'auto',
                 'overflowY': 'auto',
                 'height':650},
    export_format='xlsx',
    export_headers='display',
    merge_duplicate_headers=True
)

# Filtering the table
operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith']]


def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if v0 == value_part[-1] and v0 in ("'", '"', '`'):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value

    return [None] * 3


layout = dbc.Container([
    html.H1("Tableau des données",
            style={"text-align": "center",
                   "margin-top": "10px"}
            ),
    html.Hr(),
    html.P("Il est possible de filter les colonnes puis d'exporter les données en cliquant sur 'Export'."),
    data_table
])