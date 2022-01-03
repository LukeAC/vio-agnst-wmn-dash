## Run this in terminal
## FLASK_APP=app.py FLASK_ENV=development FLASK_DEBUG=1 TEMPLATES_AUTO_RELOAD=1 python app.py


from flask import Flask, render_template
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import dash_daq as daq

from queries import get_countries_in_continent_code, \
                    get_continent_with_country_code, \
                    get_demographics

from plotting import missing_values_plot,\
                    question_response_plot,\
                    survey_year_plot,\
                    ques_gender_scatter_plot


app = Dash()   #initialising dash app

app.layout = html.Div(id = 'parent', children = [
    html.H1(
            id = 'dash-header', 
            children = 'Violence Against Women Dashboard',
            style = {
                    'textAlign':'center',
                    'marginTop':40,
                    'marginBottom':40
                }
        ),

    dcc.Dropdown(
        id = 'question-dd',
        options = [
                {'label': '... for at least one specific reason', 'value': 1},
                {'label': '... if she argues with him', 'value': 2},
                {'label': '... if she burns the food', 'value': 3},
                {'label': '... if she goes out without telling him', 'value': 4},
                {'label': '... if she refuses to have sex with him', 'value': 5},
                {'label': '... if she neglects the children', 'value': 6}
            ],
        value = 1
        ),
    
    dcc.Dropdown(
        id = 'country-dd',
        options = get_countries_in_continent_code(),
        value = 'All'
        ),
    
    dcc.Dropdown(
        id = 'continent-dd',
        options = get_continent_with_country_code(),
        value = 'All'
        ),

    dcc.Dropdown(
        id = 'demographic-dd',
        options = get_demographics(),
        value = 'Education'
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

    html.H2(
            id = 'dash-header-2', 
            children = 'Compare Men and Women in Demographic Groups',
            style = {
                    'textAlign':'center',
                    'marginTop':40,
                    'marginBottom':40
                }
        ),
    
    daq.ToggleSwitch(
        id='plot-toggle-switch',
        label='Scatter plot / Box Plot',
        value=False
    ),

    dcc.Slider(
        id = 'opacity-slider',
        min=0.1,
        max=1,
        step=0.1,
        value = 1
        ),

    dcc.Graph(
        id = 'ques_gender_scatter_plot', 
        figure = ques_gender_scatter_plot(),
    )
    ]
)


@app.callback(
    Output('country-dd', 'options'),
    Input('continent-dd', 'value'))
def update_country_dd_options(continent_code):
    return get_countries_in_continent_code(continent_code)

@app.callback(
    Output('continent-dd', 'options'),
    Input('country-dd', 'value'))
def update_continent_dd_options(country_code):
    return get_continent_with_country_code(country_code)


@app.callback(Output(component_id='question_response_plot', component_property= 'figure'),
              [Input(component_id='continent-dd', component_property= 'value'),
              Input(component_id='country-dd', component_property= 'value'),
              Input(component_id='question-dd', component_property= 'value')])
def update_question_response_plot(continent_value, country_value, question_value):
    print(continent_value)
    print(country_value)
    print(question_value)
    fig = question_response_plot(continent_value, country_value, question_value)

    return fig  


@app.callback(Output(component_id='ques_gender_scatter_plot', component_property= 'figure'),
             [Input(component_id='continent-dd', component_property= 'value'),
              Input(component_id='country-dd', component_property= 'value'),
              Input(component_id='demographic-dd', component_property= 'value'),
              Input(component_id='opacity-slider', component_property= 'value'),
              Input(component_id='plot-toggle-switch', component_property='value')])
def update_ques_gender_scatter_plot(continent_value, country_value, demographic_value,
opacity, plot_toggle):
    print(continent_value)
    print(country_value)
    print(demographic_value)
    fig = ques_gender_scatter_plot(continent_value, country_value, demographic_value, opacity, plot_toggle)

    return fig 

if __name__ == '__main__':
    app.run_server()
