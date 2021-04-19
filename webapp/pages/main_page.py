import locale
from app import app

locale.setlocale(locale.LC_ALL, '')
from pathlib import Path
import pandas as pd
import numpy as np
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
from dash.exceptions import PreventUpdate
from collections import Counter
import json

# Plotly charts
year = [2016, 2017, 2018, 2019, 2020, 2021, "Toutes années confondues"]
dpts = ['33', '64', '24', '40', '47', "Tous départements confondus"]

layout = html.Div([
    html.Div(id='intermediate-value', style={'display': 'none'}),
    dbc.Row([
        dbc.Col([
            html.H1("Tableau de bord avec des données provenant de BOAMP",
                    style={"text-align": "center",
                           "margin-top": "10px"}),
            html.Hr()
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.Div([
                html.P("Sélection de l'année souhaitée pour l'analyse (multi-sélection possible)",
                       style={"text-align": "center"}),
                dcc.Dropdown(id="year",
                             options=[{'label': k, 'value': k} for k in year],
                             multi=True,
                             value='Toutes années confondues')
            ]),
        ]),
        dbc.Col([
            html.Div([
                html.P("Sélection du département souhaité pour l'analyse (multi-sélection possible)",
                       style={"text-align": "center"}),
                dcc.Dropdown(id="dpts",
                             options=[{'label': k, 'value': k} for k in dpts],
                             multi=True,
                             value='Tous départements confondus'),
            ])
        ]),
    ]),
    html.Hr(),
    dbc.Row([
        dbc.Col([
            html.Div([
                dcc.Graph(id="map")
            ])
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.Div([
                dcc.Graph(id="dept")
            ]),
        ], width=4),
        dbc.Col([
            html.Div([
                dcc.Graph(id="cat")
            ]),
        ], width=4),
        dbc.Col([
            html.Div([
                dcc.Graph(id="number")
            ]),
        ], width=4),
    ]),
    dbc.Row([
        dbc.Col([
            html.P("Sélection de l'interval"),
            dcc.Input(id="top_buyer",
                      type="number",
                      value=20,
                      placeholder=20),
            html.Div([
                dcc.Graph(id="buyer")
            ]),
        ], width=12),
    ]),
    dbc.Row([
        dbc.Col([
            html.P("Sélection de l'interval"),
            dcc.Input(id="top_libelle",
                      type="number",
                      value=20,
                      placeholder=20),
            html.Div([
                dcc.Graph(id="code")
            ]),
        ], width=12),
    ]),
], style={'margin-left': '20px', 'margin-right': '20px', 'margin-bottom': '20px'})


@app.callback([
    Output('number', 'figure'),
    Output('dept', 'figure'),
    Output('cat', 'figure'),
    Output('buyer', 'figure'),
    Output('code', 'figure'),
    Output('map', 'figure')
],
    [Input('year', 'value'),
     Input('dpts', 'value'),
     Input('top_buyer', 'value'),
     Input('top_libelle', 'value'),
     ]
)
def update_figure(year, dpts, top_buyer, top_libelle):
    dtype = {'gestion.reference.idweb': str,
             'gestion.indexation.descripteurs.descripteur': str,
             'gestion.indexation.resumeobjet': str,
             'donnees.identite.denomination': str,
             'donnees.identite.correspondant': str,
             'donnees.identite.adjudicateurnuts': str,
             'donnees.identite.adresse': str,
             'donnees.identite.cp': np.float32,
             'donnees.identite.ville': str,
             'donnees.identite.tel': str,
             'donnees.identite.fax': str,
             'donnees.identite.mel': str,
             'donnees.identite.url': str,
             'donnees.identite.urlprofilacheteur': str,
             'donnees.identite.urlparticipation': str,
             'donnees.identite.urldocument': str,
             'donnees.identite.agitpourautrecomptenon': "category",
             'donnees.identite.organismeacheteurcentralnon': "category",
             'donnees.activiteprincipale.pouvoiradjudicateur.deforACTSERVADMPUBOrSANTE': str,
             'donnees.objet': str,
             'donnees.conditionrelativemarche.cautionnement': str,
             'donnees.conditionrelativemarche.financement': str,
             'donnees.conditionrelativemarche.formejuridique': "category",
             'donnees.conditionrelativemarche.participationelectroniqueoui': "category",
             'donnees.conditionrelativemarche.autresconditionspartnon': "category",
             'donnees.conditionrelativemarche.unitemonetaireeur': "category",
             'donnees.conditionrelativemarche.langues.langue': "category",
             'donnees.conditionadministrative.referencemarche': str,
             'donnees.conditionadministrative.conditionsremiseoffres': str,
             'donnees.conditionadministrative.dateouvertureoffres': str,
             'donnees.conditionadministrative.envoielectroniqueavecoutilnon': np.float32,
             'donnees.attribution.decision': str,
             'gestion.marche.annonceanterieur': str,
             'schema': str,
             'description': str,
             'annee': np.int32,
             'dept': "category",
             'cat': "category",
             'marche': "category",
             'gestion.reference.typeavis.famille*': str,
             'gestion.reference.typeavis.perimetre*': str,
             'donnees.typeorganisme*': str,
             'gestion.reference.typeavis.nature.appeloffre*': str,
             'gestion.reference.typeavis.statut*': str,
             'gestion.indexation.criteressociauxenv.*': str,
             'adresse_complete': str,
             'latitude': np.float32,
             'longtitude': np.float32}

    BASE_DIR = Path(__file__).resolve().parent.parent
    DATA_DIR = BASE_DIR.joinpath('assets')
    df = pd.read_csv(DATA_DIR / "data.csv", index_col=0,dtype=dtype)
    # some expensive clean data step
    if len(year) == 0:
        raise PreventUpdate
    if len(dpts) == 0:
        raise PreventUpdate
    if "Toutes années confondues" in year:
        pass
    else:
        df = df[df["annee"].isin(year)]

    if "Tous départements confondus" in dpts:
        pass
    else:
        df = df[df["dept"].isin(dpts)]

    fig_1 = go.Figure(go.Indicator(
        mode="number",
        value=len(df),
        title={"text": "Nombre de données totales"}))
    fig_1.update_layout(
        template="simple_white")

    fig_2 = px.pie(df,
                   names='dept',
                   color="dept",
                   title="Répartition des différents départements",
                   template="simple_white")

    fig_3 = px.pie(df,
                   names='cat',
                   color='cat',
                   title="Répartition des différentes catégories",
                   template="simple_white")

    dff = df.groupby(by=["donnees.identite.denomination"]).count()["gestion.reference.idweb"].sort_values(
        ascending=False)[:top_buyer].reset_index()
    if top_buyer is None:
        title = f"Top des entités qui apparaissent le plus"
    else:
        title = f"Top {top_buyer} des entités qui apparaissent le plus"
    fig_4 = px.bar(dff,
                   x='donnees.identite.denomination',
                   y='gestion.reference.idweb',
                   text="gestion.reference.idweb",
                   title=title,
                   template="simple_white",
                   labels={"donnees.identite.denomination": "Dénomination",
                           "gestion.reference.idweb": "Nombre d'occurrences"})
    fig_4.update_traces(textposition='auto')

    if top_libelle is None:
        title = f"Top des principaux libéllés"
    else:
        title = f"Top {top_libelle} des principaux libéllés"

    df3 = pd.DataFrame \
        (Counter \
             (df["gestion.indexation.descripteurs.descripteur"] \
              .str.replace('{', "", regex=True).str.replace("'", "", regex=True).str.replace("}", "", regex=True) \
              .tolist()) \
         .most_common(top_libelle))\
        .rename(columns={0: "type travaux", 1: "Compte"})
    fig_5 = px.bar(df3,
                   x='type travaux',
                   y='Compte',
                   title=f"Top {top_libelle} des principaux libéllés",
                   text="Compte",
                   template="simple_white",
                   labels={"type travaux": "Catégorie de Travaux",
                           "Compte": "Nombre d'occurrences"})
    fig_5.update_traces(textposition='auto')

    fig_6 = go.Figure(go.Scattermapbox(
        lat=df["latitude"],
        lon=df["longtitude"],
        mode='markers',
        marker=go.scattermapbox.Marker(color="salmon"),
        text=[f"Reference idweb:{i} <br>" \
              + f"Adresse:{j} <br>" \
              + f"Libellé Descripteur:{k}<br>" \
              + f"Objet Descripteur:{l}<br>" \
              + f"Identite dénomination:{m}<br>" \
              for i, j, k, l, m in \
              zip(df["gestion.reference.idweb"],
                  df["donnees.identite.adresse"],
                  df["gestion.indexation.descripteurs.descripteur"],
                  df["gestion.indexation.resumeobjet"],
                  df["donnees.identite.denomination"])],
        hoverinfo='text'))

    fig_6.update_layout(mapbox_style="open-street-map",
                        mapbox=dict(
                            zoom=6,
                            center=dict(lat=44.49,
                                        lon=-0.79)))
    fig_6.update_layout(
        title="Carte des marchés publics",
        autosize=True,
        showlegend=False,
        hovermode='closest',
        height=500)

    fig_6.update_layout(
        legend=dict(
            x=0,
            y=1,
            traceorder="normal",
            font=dict(
                family="sans-serif",
                size=12,
                color="black"
            ),
            bgcolor="white",
            bordercolor="Black",
            borderwidth=1
        )
    )

    fig_6.update_layout(margin={"r": 0, "t": 30, "l": 0, "b": 0})

    return fig_1, fig_2, fig_3, fig_4, fig_5, fig_6
