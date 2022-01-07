from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_daq as daq

from plotting import missing_values_plot,\
                    statement_response_plot,\
                    survey_year_plot,\
                    ques_gender_scatter_plot

missing_val_plot = dcc.Graph(
        id = 'missing_values_plot', 
        figure = missing_values_plot()
    )

survey_yr_plot = dcc.Graph(
        id = 'survey_year_plot', 
        figure = survey_year_plot()
    )

qr_plot = dcc.Graph(
        id = 'statement_response_plot', 
        figure = statement_response_plot()
    )

gender_scatter = dcc.Graph(
        id = 'ques_gender_scatter_plot', 
        figure = ques_gender_scatter_plot()
    )

row_1 = dbc.Row([dbc.Col(qr_plot)])

row_2 = dbc.Row([
    dbc.Col(gender_scatter)
    ])

row_3 = dbc.Row([
    dbc.Col(daq.ToggleSwitch(
        id='plot-toggle-switch',
        label={'label': 'Plot type: Scatter / Box', 'style': {'font-size': "smaller"}},
        value=False,
        size=30,
        style={'margin-top': '-418px', 'margin-left': '70%'})
        ),
    ])

row_4 = dbc.Row([
    dbc.Col(survey_yr_plot, width=7),
    dbc.Col(missing_val_plot, width=5)
    ])

dash_content = html.Div(
    [
        html.H2('EDA Dashboard for Violence Against Women & Girls Dataset',
            className="app-header"),
        html.Hr(),
        row_1,
        row_2,
        row_3,
        row_4
    ],
    className="app-content"
)