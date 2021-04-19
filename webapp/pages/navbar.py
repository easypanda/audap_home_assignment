import dash_bootstrap_components as dbc

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Méthodologie", href="/methodologie")),
        dbc.NavItem(dbc.NavLink("Données", href="/data")),
    ],
    brand="AUDAP - Agence d'urbanisme Atlantique & Pyrénées",
    brand_href="/",
    sticky="top",
    dark=True,
    color="primary",
    className="fixed-top"
)
