from dash import Dash
from dash.dependencies import Input, Output
import dash_sidebar
import dash_content
import dash_bootstrap_components as dbc

from src.queries import (
    get_labels_countries_in_continent_code,
    get_labels_continent_with_country_code,
    get_labels_statements,
    get_labels_continent_with_continent_code,
)

from src.plotting import (
    missing_values_plot,
    statement_response_plot,
    survey_year_plot,
    ques_gender_scatter_plot,
    data_table,
)

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.title = "Violence Against Women Dashboard"

app.layout = dbc.Container(
    fluid=True,
    children=[  # html.Div(id = 'parent', children = [
        dash_sidebar.dash_sidebar,
        dash_content.dash_content,
    ],
    style={"padding-right": "0px"},
)


@app.callback(Output("country-dd", "options"), Input("continent-dd", "value"))
def update_country_dd_options(continent_code):
    return get_labels_countries_in_continent_code(continent_code)


@app.callback(Output("continent-dd", "options"), Input("country-dd", "value"))
def update_continent_dd_options(country_code):
    return get_labels_continent_with_country_code(country_code)


@app.callback(
    Output(component_id="missing_values_plot", component_property="figure"),
    [
        Input(component_id="continent-dd", component_property="value"),
        Input(component_id="country-dd", component_property="value"),
    ],
)
def update_missing_values_plot(continent_value, country_value):
    return missing_values_plot(continent_value, country_value)


@app.callback(
    Output(component_id="survey_year_plot", component_property="figure"),
    [Input(component_id="continent-dd", component_property="value")],
)
def update_survey_year_plot(continent_value):
    return survey_year_plot(continent_code=continent_value)


@app.callback(
    Output(component_id="statement_response_plot", component_property="figure"),
    [
        Input(component_id="continent-dd", component_property="value"),
        Input(component_id="statement-dd", component_property="value"),
    ],
)
def update_statement_response_plot(continent_value, question_value):
    return statement_response_plot(
        continent_code=continent_value, statement_id=question_value
    )


@app.callback(
    Output(component_id="ques_gender_scatter_plot", component_property="figure"),
    [
        Input(component_id="continent-dd", component_property="value"),
        Input(component_id="country-dd", component_property="value"),
        Input(component_id="demographic-dd", component_property="value"),
        Input(component_id="plot-toggle-switch", component_property="value"),
    ],
)
def update_ques_gender_scatter_plot(
    continent_value, country_value, demographic_value, plot_toggle
):
    return ques_gender_scatter_plot(
        continent_value, country_value, demographic_value, plot_toggle
    )


@app.callback(
    [
        Output(component_id="summary_table_women", component_property="data"),
        Output(component_id="summary_table_women", component_property="columns"),
    ],
    [
        Input(component_id="statement-dd", component_property="value"),
        Input(component_id="continent-dd", component_property="value"),
        Input(component_id="demographic-dd", component_property="value"),
    ],
)
def update_summtbl_women(question_value, continent_value, demographic_value):
    return data_table(
        gender="F",
        statement_id=question_value,
        continent_code=continent_value,
        by_demographic=demographic_value,
    )


@app.callback(
    [
        Output(component_id="summary_table_men", component_property="data"),
        Output(component_id="summary_table_men", component_property="columns"),
    ],
    [
        Input(component_id="statement-dd", component_property="value"),
        Input(component_id="continent-dd", component_property="value"),
        Input(component_id="demographic-dd", component_property="value"),
    ],
)
def update_summtbl_men(question_value, continent_value, demographic_value):
    return data_table(
        gender="M",
        statement_id=question_value,
        continent_code=continent_value,
        by_demographic=demographic_value,
    )


@app.callback(
    [
        Output(component_id="statementtext_plot", component_property="children"),
        Output(component_id="statementtext_table", component_property="children"),
    ],
    [Input(component_id="statement-dd", component_property="value")],
)
def update_table_header(question_value):
    label = get_labels_statements(statement_id=question_value)
    return [label, label]


@app.callback(
    Output(component_id="continenttext", component_property="children"),
    [Input(component_id="continent-dd", component_property="value")],
)
def update_continent_header(continent_value):
    return get_labels_continent_with_continent_code(continent_code=continent_value)


if __name__ == "__main__":
    app.run_server()
