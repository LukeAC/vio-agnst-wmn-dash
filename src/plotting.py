## Imports
import src.queries as q
import plotly.express as px
import plotly.graph_objects as go

## Styling
margins = dict(l=1, b=10, r=1, t=7)
fig_template = 'plotly_white'
fig_bckg_col = 'rgb(248, 249, 250)'

def missing_values_plot(continent_code='All', country_code='All'):
    """Takes a continent code and country code and returns bar chart object"""

    filtered_data = q.geo_filter(continent_code=continent_code, country_code=country_code)
    missing_vals = filtered_data.loc[filtered_data['Value'].isna()]

    figure = px.bar(
        missing_vals.Country.value_counts()[:11],
        orientation='h',
        height=300,
        template=fig_template
    )
    figure.update_layout(
        showlegend=False, 
        font=dict(size=9),
        margin=dict(l=1, b=10, r=10, t=7),
        paper_bgcolor=fig_bckg_col,
        plot_bgcolor=fig_bckg_col,
        dragmode=False
    )
    figure.update_xaxes(title='Number of missing values', nticks=10)
    figure.update_yaxes(title='')
    
    return figure


def survey_year_plot(continent_code='All', country_code='All'):
    """Takes a continent code and country code and returns choropleth object"""

    filtered_data = q.geo_filter(continent_code=continent_code, country_code=country_code)
    figure = px.choropleth(
        filtered_data, 
        locations="country_code",
        hover_name="Country",
        hover_data=["Survey Year"],
        color = "date_bins",
        category_orders={"date_bins": ["2000 - 2004", "2005 - 2009", "2010 - 2014", "2015 - 2018"]},
        height=300,
        template=fig_template
    )

    figure.update_layout(
        margin = margins,
        font=dict(size=9),
        legend=dict(
            title="Survey conducted in...",
            bgcolor = 'rgba(255,255,255,0.9)',
            yanchor="top",
            y=0.97,
            xanchor="left",
            x=0.07
        ),
        paper_bgcolor=fig_bckg_col,
        plot_bgcolor=fig_bckg_col,
        dragmode=False
    )

    return figure


def statement_response_plot(continent_code='All', country_code='All', statement_id=1):
    """
    Takes a continent code, country code, and a statement id and returns choropleth object
    
    Statements are enumerated as follows:

    A husband is justified in hitting or beating his wife...
        1 = '... for at least one specific reason'
        2 = '... if she argues with him'
        3 = '... if she burns the food'
        4 = '... if she goes out without telling him'
        5 = '... if she refuses to have sex with him'
        6 = '... if she neglects the children'
    """
    filtered_data = q.geo_filter(continent_code=continent_code, country_code=country_code)
    filtered_data = q.question_filter(filtered_data, statement_id)
    country_question = filtered_data.drop(['Survey Year', 'RecordID'], axis=1).groupby([
        "Country",
        "country_code",
        "Statement"
        ]).mean("Value").reset_index()

    agreement_across_countries = px.choropleth(
        country_question, 
        locations="country_code",
        hover_name="Country",
        color="Value",
        height=300,
        template=fig_template
    )

    agreement_across_countries.update_layout(
        font=dict(size=9),
        margin=margins,
        coloraxis_colorbar=dict(
            title="% in Agreement",
            tickmode='array',
            tickvals=[i for i in range(0, 100, 5)],
            ticktext=['{x}%'.format(x=x) for x in range(0, 100, 5)]
        ),
        paper_bgcolor=fig_bckg_col,
        plot_bgcolor=fig_bckg_col
    )

    return agreement_across_countries

def ques_gender_scatter_plot(continent_code='All', country_code='All', 
by_demographic='Education', plot_toggle=True):
    """Takes a continent code,country code, and demographic group and returns boxplot or scatter plot object"""

    filtered_data = q.geo_filter(continent_code=continent_code, country_code=country_code)
    opacity = (1/len(filtered_data)) * 2000
    if plot_toggle is True:
        figure = px.box(
            filtered_data.loc[filtered_data['Demographics Question'] == by_demographic],
            y="Value",  
            x="Demographics Response",
            color="Statement",
            facet_col="Gender",
            height=400,
            hover_data=['Country'],
            template=fig_template
            )
    else:
        figure = px.scatter(
            data_frame=filtered_data.loc[filtered_data['Demographics Question'] == by_demographic], 
            x="Value",
            y="Statement",
            color="Gender",
            custom_data=['Country'],
            facet_col="Demographics Response",
            opacity=opacity if opacity<=1 else 1,
            height=400,
            template=fig_template
            )
        figure.update_yaxes(title=by_demographic)
    
    figure.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

    for axis in figure.layout:
        if type(figure.layout[axis]) == go.layout.XAxis:
            figure.layout[axis].title.text = ''
        if type(figure.layout[axis]) == go.layout.YAxis:
            figure.layout[axis].title.text = ''

    if plot_toggle is True:
        figure.update_layout(
            annotations = list(figure.layout.annotations) + 
            [go.layout.Annotation(
                    x=-0.06,
                    y=0.5,
                    font=dict(
                        size=12
                    ),
                    textangle=-90,
                    showarrow=False,
                    text="Percent Agreement",
                    xref="paper",
                    yref="paper"
                )
            ]
        )
    else:
        figure.update_layout(
            annotations = list(figure.layout.annotations) + 
            [go.layout.Annotation(
                    x=0.5,
                    y=-0.13,
                    font=dict(
                        size=12
                    ),
                    showarrow=False,
                    text="Percent Agreement",
                    xref="paper",
                    yref="paper"
                )
            ]
        )

    figure.update_layout(
        font=dict(size=9),
        margin = dict(l=5, b=10, r=10, t=55),
        legend=dict(
            yanchor="top",
            y=1.06,
            xanchor="left",
            x=1
        ),
        paper_bgcolor=fig_bckg_col,
        plot_bgcolor=fig_bckg_col
    )
    
    figure.update_traces(
        hovertemplate="<br>".join([
            "Value: %{x}",
            "Country: %{customdata[0]}"
        ])
    )

    return figure

def data_table(gender, continent_code='All', country_code='All', 
    by_demographic='Education', statement_id=1):
    """Takes a gender (must be 'F' or 'M'), continent code, country code, demographic group,
    and statement id and returns choropleth object"""
    
    filtered_data = q.geo_filter(continent_code=continent_code, country_code=country_code)
    filtered_data = q.question_filter(filtered_data, statement_id)
    filtered_data = q.demo_filter(filtered_data, by_demographic)
    output_dict = {
        'title': filtered_data['Demographics Question'].unique()[0],
        'values': filtered_data
            .loc[filtered_data['Gender']==gender]
            .groupby(['demo_ordinal', 'Demographics Response'])
            .mean(['Value']).round(2).reset_index()
            .loc[:, ['Demographics Response','Value']]
        }

    columns = [
        {"name": output_dict['title'], "id": 'Demographics Response'},
        {"name": 'Avg. % Agreement', "id": 'Value'}
        ]
    
    data = output_dict['values'].to_dict('records')

    return data, columns

    