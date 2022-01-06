from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_daq as daq

from plotting import missing_values_plot,\
                    question_response_plot,\
                    survey_year_plot,\
                    ques_gender_scatter_plot

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
        )
    ])

row_4 = dbc.Row([
    dbc.Col(daq.ToggleSwitch(
        id='plot-toggle-switch',
        label={'label': 'Plot type: Scatter / Box', 'style': {'font-size': "smaller"}},
        value=False,
        size=30,
        style={'margin-top': '-418px', 'margin-left': '70%'})
        ),
    ])

dash_content = html.Div(
    [
        html.H2('Analytics Dashboard Template',
            className="app-header"),
        html.Hr(),
        row_1,
        row_2,
        row_3,
        row_4
    ],
    className="app-content"
)