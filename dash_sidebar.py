## Imports
from dash import html, dcc
import dash_bootstrap_components as dbc
from src.queries import (
    get_labels_countries_in_continent_code,
    get_labels_continent_with_country_code,
    get_labels_demographics,
    get_labels_statements,
)


## Define sidebar controls
controls = dbc.FormGroup(
    [
        html.P("Continent Selection", className="app-sidebar-dd-label"),
        dcc.Dropdown(
            id="continent-dd",
            options=get_labels_continent_with_country_code(),
            value="All",
            clearable=False,
            className="dropdown",
        ),
        html.P("Country Selection", className="app-sidebar-dd-label"),
        dcc.Dropdown(
            id="country-dd",
            options=get_labels_countries_in_continent_code(),
            value="All",
            clearable=False,
            className="dropdown",
        ),
        html.P("Statement", className="app-sidebar-dd-label"),
        dcc.Dropdown(
            id="statement-dd",
            options=get_labels_statements(),
            value=1,
            clearable=False,
            className="dropdown",
        ),
        html.P("Demographic", className="app-sidebar-dd-label"),
        dcc.Dropdown(
            id="demographic-dd",
            options=get_labels_demographics(),
            value="Education",
            clearable=False,
            className="dropdown",
        ),
        dbc.Card(
            [
                dbc.CardHeader([html.H4("NOTE", className="note-subtitle")]),
                dbc.CardBody(
                    [
                        "The term 'Statement' used in this dashboard is short-form \
                    for the selected sentence fragment prefaced by the statement: \n \
                    'A husband is justified in hitting or beating his wife...'"
                    ],
                    style={"padding": "6px 6px"},
                ),
            ],
            className="text-white bg-info",
        ),
    ]
)


## Create sidebar
dash_sidebar = html.Div(
    id="sidebar",
    children=[
        html.H2(
            "EDA Dashboard for Violence Against Women & Girls Dataset",
            className="sidebar-header",
        ),
        html.Hr(),
        controls,
    ],
    className="app-sidebar",
)
