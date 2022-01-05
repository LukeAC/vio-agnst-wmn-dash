import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
from queries import get_countries_in_continent_code, \
                    get_continent_with_country_code, \
                    get_demographics

# the style arguments for the sidebar.
SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '20%',
    'padding': '20px 10px',
    'background-color': '#f8f9fa'
}

# the style arguments for the main content page.

TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#191970'
}

CARD_TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#0074D9'
}

controls = dbc.FormGroup(
    [
        html.P('Question', style={
            'textAlign': 'center'
        }),
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
        html.Br(),
        html.P('Continent Selection', style={
            'textAlign': 'center'
        }),
        dcc.Dropdown(
                    id = 'continent-dd',
                    options = get_continent_with_country_code(),
                    value = 'All',
        ),
        html.Br(),
        html.P('Country Selection', style={
            'textAlign': 'center'
        }),
        dcc.Dropdown(
                    id = 'country-dd',
                    options = get_countries_in_continent_code(),
                    value = 'All',
        ),
        dcc.Dropdown(
                    id = 'demographic-dd',
                    options = get_demographics(),
                    value = 'Education'
        ),
        daq.ToggleSwitch(
        id='plot-toggle-switch',
        label='Scatter plot / Box Plot',
        value=False
    ),
    ])

dash_sidebar = html.Div(
    [
        html.H2('Parameters', style=TEXT_STYLE),
        html.Hr(),
        controls
    ],
    style=SIDEBAR_STYLE,
)
