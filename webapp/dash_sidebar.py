import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
from queries import get_labels_countries_in_continent_code, \
                    get_labels_continent_with_country_code, \
                    get_labels_demographics, \
                    get_labels_statements

# the style arguments for the main content page.

controls = dbc.FormGroup(
    [   
        html.P('Continent Selection', className="app-sidebar-dd-label"),
        
        dcc.Dropdown(
            id = 'continent-dd',
            options = get_labels_continent_with_country_code(),
            value = 'All',
            clearable=False,
            className='dropdown'
        ),
                
        html.P('Country Selection', className="app-sidebar-dd-label"),
        
        dcc.Dropdown(
            id = 'country-dd',
            options = get_labels_countries_in_continent_code(),
            value = 'All',
            clearable=False,
            className='dropdown'
        ),

        html.P('Statement', className="app-sidebar-dd-label"),
        
        dcc.Dropdown(
            id = 'statement-dd',
            options = get_labels_statements(),
            value = 1,
            clearable=False,
            className='dropdown'
        ),
                
        html.P('Demographic', className="app-sidebar-dd-label"),

        dcc.Dropdown(
            id = 'demographic-dd',
            options = get_labels_demographics(),
            value = 'Education',
            clearable=False,
            className='dropdown'
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
