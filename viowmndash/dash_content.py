from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import dash_daq as daq

from src.plotting import (
    missing_values_plot,
    statement_response_plot,
    survey_year_plot,
    ques_gender_scatter_plot,
    data_table,
)

card_class = "card bg-light"

missing_val_plot = dcc.Graph(id="missing_values_plot", figure=missing_values_plot())

survey_yr_plot = dcc.Graph(
    id="survey_year_plot", figure=survey_year_plot(), config={"displayModeBar": False}
)

qr_plot = dcc.Graph(id="statement_response_plot", figure=statement_response_plot())

gender_scatter = dcc.Graph(
    id="ques_gender_scatter_plot", figure=ques_gender_scatter_plot()
)

init_f_data, init_f_columns = data_table(gender="F")
summary_table_women = dash_table.DataTable(
    id="summary_table_women",
    columns=init_f_columns,
    data=init_f_data,
    style_data={
        "whiteSpace": "normal",
    },
    style_cell={"fontSize": "9pt", "font-family": "sans-serif", "textAlign": "left"},
)

init_m_data, init_m_columns = data_table(gender="M")
summary_table_men = dash_table.DataTable(
    id="summary_table_men",
    columns=init_m_columns,
    data=init_m_data,
    style_data={
        "whiteSpace": "normal",
    },
    style_cell={"fontSize": "9pt", "font-family": "sans-serif", "textAlign": "left"},
)

row_3 = dbc.Row(
    [
        dbc.Col(
            dbc.Card(
                [
                    dbc.CardHeader(
                        [
                            html.H3(
                                "Percent surveyed pop. that agrees with statement avgd. over demographic and gender",
                                className="card-title",
                            ),
                            html.H4(
                                "Statement: ... for at least one specific reason",
                                id="statementtext_plot",
                                className="card-subtitle",
                            ),
                        ]
                    ),
                    dbc.CardBody([qr_plot]),
                ],
                className=card_class,
            ),
            style={"padding-right": "5px"},
            width=8,
        ),
        dbc.Col(
            dbc.Card(
                [
                    dbc.CardHeader(
                        [
                            html.H3(
                                "Continental Summary - All continents",
                                id="continenttext",
                                className="card-title",
                            ),
                            html.H4(
                                "Statement: ... for at least one specific reason",
                                id="statementtext_table",
                                className="card-subtitle",
                            ),
                        ]
                    ),
                    dbc.CardBody(
                        [
                            html.H5("Men"),
                            summary_table_men,
                            html.H5("Women"),
                            summary_table_women,
                        ],
                        style={"padding": "5px 5px"},
                    ),
                ],
                className=card_class,
            ),
            style={"padding-left": "5px"},
            width=4,
        ),
    ]
)

row_2 = dbc.Row(
    [
        dbc.Col(
            dbc.Card(
                [
                    dbc.CardHeader(
                        [
                            html.H3(
                                "Percent surveyed pop. that agrees with statements across gender and demographic",
                                className="card-title",
                            ),
                            html.H4(
                                "Scatter - useful for visualising country-specific gender comparison. Box - useful for visualising continental/population trends.",
                                className="card-subtitle",
                            ),
                            html.Div(
                                dbc.Card(
                                    [
                                        dbc.CardBody(
                                            daq.ToggleSwitch(
                                                id="plot-toggle-switch",
                                                label={
                                                    "label": "Plot type: Scatter / Box",
                                                    "style": {"font-size": "smaller"},
                                                },
                                                value=True,
                                                size=30,
                                                style={
                                                    "margin": "0px",
                                                    "padding": "0px",
                                                },  # toggle style
                                            ),
                                            style={
                                                "margin": "0px 0px",
                                                "padding": "0px 0px",
                                            },
                                        )  # card body style
                                    ],
                                    style={"padding": "5px"},
                                ),  # card style
                                style={"float": "right", "margin-top": "-50px"},
                            ),  # div style
                        ]
                    ),
                    dbc.CardBody([gender_scatter]),
                ],
                className=card_class,
            ),
            width=12,
        )
    ]
)

row_1 = dbc.Row(
    [
        dbc.Col(
            dbc.Card(
                [
                    dbc.CardHeader(
                        [
                            html.H3("Survey year", className="card-title"),
                        ]
                    ),
                    dbc.CardBody(survey_yr_plot),
                ],
                className=card_class,
            ),
            width=8,
            style={"padding-right": "5px"},
        ),
        dbc.Col(
            dbc.Card(
                [
                    dbc.CardHeader(
                        [
                            html.H3(
                                "Missing values in source data", className="card-title"
                            ),
                        ]
                    ),
                    dbc.CardBody([missing_val_plot], style={"padding-right": "15px"}),
                ],
                className=card_class,
            ),
            width=4,
            style={"padding-left": "5px"},
        ),
    ]
)

dash_content = html.Div([row_1, row_2, row_3], className="app-content")
