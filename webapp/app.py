## Run this in terminal
## FLASK_APP=app.py FLASK_ENV=development FLASK_DEBUG=1 TEMPLATES_AUTO_RELOAD=1 python app.py


from flask import Flask, render_template
from dash import Dash, html, dcc

from data_processing import missing_values_plot, \
                            question_response_plot, \
                            survey_year_plot, \
                            quesvalue_scatter_plot

import plotly.graph_objects as go
import plotly.express as px

app = Dash()   #initialising dash app
df = px.data.stocks() #reading stock price dataset 

## Should import graph from EDA module here
## import << viowmn_eda_module >> as viowmn
## figure_1 = viowmn.Graph1.generate_graph()
def stock_prices():
    # Function for creating line chart showing Google stock prices over time 
    fig = go.Figure([go.Scatter(x = df['date'], y = df['GOOG'],\
                     line = dict(color = 'firebrick', width = 4), name = 'Google')
                     ])
    fig.update_layout(title = 'Prices over time',
                      xaxis_title = 'Dates',
                      yaxis_title = 'Prices'
                      )
    return fig  

 
app.layout = html.Div(id = 'parent', children = [
    html.H1(
            id = 'figure_1', 
            children = 'Figure 1',
            style = {
                    'textAlign':'center',
                    'marginTop':40,
                    'marginBottom':40
                }
        ),
 
    dcc.Graph(
            id = 'missing_values_plot', 
            figure = missing_values_plot()
        ),
    
    dcc.Graph(
         id = 'question_response_plot', 
        figure = question_response_plot()
    ),

    dcc.Graph(
         id = 'survey_year_plot', 
        figure = survey_year_plot()
    ),

    dcc.Graph(
         id = 'quesvalue_scatter_plot', 
        figure = quesvalue_scatter_plot()
    )
    ]
)

if __name__ == '__main__': 
    app.run_server()
