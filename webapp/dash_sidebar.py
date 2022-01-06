import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
from queries import get_countries_in_continent_code, \
                    get_continent_with_country_code, \
                    get_demographics

# the style arguments for the main content page.

controls = dbc.FormGroup(
    [   
        html.P('Continent Selection', className="app-sidebar-dd-label"),
        
        dcc.Dropdown(
            id = 'continent-dd',
            options = get_continent_with_country_code(),
            value = 'All',
            clearable=False
        ),
        
        html.Br(),
        
        html.P('Country Selection', className="app-sidebar-dd-label"),
        
        dcc.Dropdown(
            id = 'country-dd',
            options = get_countries_in_continent_code(),
            value = 'All',
            clearable=False
        ),

        html.Br(),

        html.P('Question', className="app-sidebar-dd-label"),
        
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
            value = 1,
            clearable=False
        ),
        
        html.Br(),
        
        html.P('Demographic', className="app-sidebar-dd-label"),

        dcc.Dropdown(
            id = 'demographic-dd',
            options = get_demographics(),
            value = 'Education',
            clearable=False
        )
    ])

dash_sidebar = html.Div(
    id = 'sidebar',
    children=[
        html.H2('Parameters', className="app-header"),
        html.Hr(),
        controls
    ],
    className="app-sidebar"
)
