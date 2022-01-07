## Run this in terminal
## FLASK_APP=app.py FLASK_ENV=development FLASK_DEBUG=1 TEMPLATES_AUTO_RELOAD=1 python app.py


from dash import Dash, html
from dash.dependencies import Input, Output
import dash_sidebar
import dash_content
import dash_bootstrap_components as dbc

from queries import get_labels_countries_in_continent_code, \
                    get_labels_continent_with_country_code

from plotting import missing_values_plot,\
                    statement_response_plot,\
                    survey_year_plot,\
                    ques_gender_scatter_plot


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(fluid=True, children=[#html.Div(id = 'parent', children = [
    dash_sidebar.dash_sidebar,
    dash_content.dash_content,  
    ]
)

@app.callback(
    Output('country-dd', 'options'),
    Input('continent-dd', 'value'))
def update_country_dd_options(continent_code):
    return get_labels_countries_in_continent_code(continent_code)

@app.callback(
    Output('continent-dd', 'options'),
    Input('country-dd', 'value'))
def update_continent_dd_options(country_code):
    return get_labels_continent_with_country_code(country_code)

@app.callback(Output(component_id='missing_values_plot', component_property='figure'),
              [Input(component_id='continent-dd', component_property= 'value'),
              Input(component_id='country-dd', component_property= 'value')])
def update_missing_values_plot(continent_value, country_value):
    print(continent_value)
    print(country_value)  
    fig = missing_values_plot(continent_value, country_value)

    return fig

@app.callback(Output(component_id='survey_year_plot', component_property='figure'),
              [Input(component_id='continent-dd', component_property= 'value'),
              Input(component_id='country-dd', component_property= 'value')])
def update_survey_year_plot(continent_value, country_value):
    print(continent_value)
    print(country_value)  
    fig = survey_year_plot(continent_value, country_value)

    return fig

@app.callback(Output(component_id='statement_response_plot', component_property= 'figure'),
              [Input(component_id='continent-dd', component_property= 'value'),
              Input(component_id='country-dd', component_property= 'value'),
              Input(component_id='statement-dd', component_property= 'value')])
def update_statement_response_plot(continent_value, country_value, question_value):
    print(continent_value)
    print(country_value)
    print(question_value)
    fig = statement_response_plot(continent_value, country_value, question_value)

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
