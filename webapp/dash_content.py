from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import dash_daq as daq
import dash_bootstrap_components as dbc
import dash_sidebar

from queries import get_countries_in_continent_code, \
                    get_continent_with_country_code, \
                    get_demographics

from plotting import missing_values_plot,\
                    question_response_plot,\
                    survey_year_plot,\
                    ques_gender_scatter_plot

CONTENT_STYLE = {
    'margin-left': '25%',
    'margin-right': '5%',
    'padding': '20px 10p'
}

TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#191970'
}

row_1 = dbc.Row([
    dbc.Col(dcc.Graph(
        id = 'missing_values_plot', 
        figure = missing_values_plot()),
        style={'width': "50%"}),
    dbc.Col(dcc.Graph(
        id = 'survey_year_plot', 
        figure = survey_year_plot()), 
        style={'width': "50%"})
    ])

row_2 = dbc.Row([dbc.Col(dcc.Graph(
        id = 'question_response_plot', 
        figure = question_response_plot()
    ))])

row_3 = dbc.Row([
    dbc.Col(dcc.Graph(
        id = 'ques_gender_scatter_plot', 
        figure = ques_gender_scatter_plot()), 
        style={'width': "auto"})
    ])

dash_content = html.Div(
    [
        html.H2('Analytics Dashboard Template', style=TEXT_STYLE),
        html.Hr(),
        row_1,
        row_2,
        row_3
    ],
    style=CONTENT_STYLE
)