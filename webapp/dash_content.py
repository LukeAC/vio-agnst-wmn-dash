from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import dash_daq as daq

from plotting import missing_values_plot,\
                    statement_response_plot,\
                    survey_year_plot,\
                    ques_gender_scatter_plot, \
                    data_table

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

init_f_data, init_f_columns = data_table(gender='F')
summary_table_women = dash_table.DataTable(
    id = 'summary_table_women',
    columns=init_f_columns,
    data=init_f_data,
    style_data={
        'whiteSpace': 'normal',
    },
    style_cell={
        'fontSize': '9pt', 
        'font-family':'sans-serif',
        'textAlign': 'left'
    }
)

init_m_data, init_m_columns = data_table(gender='M')
summary_table_men = dash_table.DataTable(
    id = 'summary_table_men',
    columns=init_m_columns,
    data=init_m_data,
    style_data={
        'whiteSpace': 'normal',
    },
    style_cell={
        'fontSize': '9pt', 
        'font-family':'sans-serif',
        'textAlign': 'left'
    },
)

row_4 = dbc.Row([
    dbc.Col(
        dbc.Card([
            html.H3('Percent of surveyed pop. that agrees with statement averaged over demographic and gender', className='card-title'),
            html.H4('Statement: ... for at least one specific reason', id='statementtext_plot', className='card-subtitle'),
            dbc.CardBody([qr_plot])],
            className='card'
            ), 
        style={'padding-right': '5px'},
        width=8
        ),
    dbc.Col(
        dbc.Card([
            html.H3('Continental Summary - All continents', id='continenttext', className='card-title'),
            html.H4('Statement: ... for at least one specific reason', id='statementtext_table', className='card-subtitle'),
            dbc.CardBody([html.H5('Men'), summary_table_men, html.H5('Women'), summary_table_women])], 
        className='card'
        ),
        style={'padding-left': '5px'},
        width=4)
    ])

row_2 = dbc.Row([
    dbc.Col(dbc.Card([
            html.H3('Agreement as a function of demographic and gender', className='card-title'),
            dbc.CardBody(gender_scatter)
            ], 
        className='card'
        ), 
        width=12,
        )
    ])

row_3 = dbc.Row([
    dbc.Col(daq.ToggleSwitch(
        id='plot-toggle-switch',
        label={'label': 'Plot type: Scatter / Box', 'style': {'font-size': "smaller"}},
        value=False,
        size=30,
        style={'margin-top': '-450px', 'margin-left': '70%'})
        ),
    ])

row_1 = dbc.Row([
    dbc.Col(
        dbc.Card([
            html.H3('Survey year', className='card-title'),
            dbc.CardBody(survey_yr_plot)
        ],
        className='card'
        ), 
    width=8,
    style={'padding-right': '5px'}
    ),
    dbc.Col(
        dbc.Card([
            html.H3('Missing values in source data', className='card-title'),
            dbc.CardBody(missing_val_plot)
        ],
        className='card'
        ),
        width=4,
        style={'padding-left': '5px'}
    )
])

dash_content = html.Div(
    [
        row_1,
        row_2,
        row_3,
        row_4
    ],
    className="app-content"
)

