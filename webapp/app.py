## Run this in terminal
## FLASK_APP=app.py FLASK_ENV=development FLASK_DEBUG=1 TEMPLATES_AUTO_RELOAD=1 python app.py


from flask import Flask, render_template
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import dash_sidebar
import dash_content
import dash_daq as daq
import dash_bootstrap_components as dbc

from queries import get_countries_in_continent_code, \
                    get_continent_with_country_code, \
                    get_demographics

from plotting import missing_values_plot,\
                    question_response_plot,\
                    survey_year_plot,\
                    ques_gender_scatter_plot


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(id = 'parent', children = [
    dash_sidebar.dash_sidebar,
    dash_content.dash_content,  
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
              Input(component_id='plot-toggle-switch', component_property='value')])
def update_ques_gender_scatter_plot(continent_value, country_value, demographic_value, plot_toggle):
    print(continent_value)
    print(country_value)
    print(demographic_value)
    print(plot_toggle)
    fig = ques_gender_scatter_plot(continent_value, country_value, demographic_value, plot_toggle)

    return fig 

if __name__ == '__main__':
    app.run_server()
