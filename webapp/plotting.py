import queries as q
import plotly.express as px
import plotly.graph_objects as go

margins = dict(l=5, b=10, r=10)

def missing_values_plot(continent_code='All', country_code='All'):
    filtered_data = q.geo_filter(continent_code=continent_code, country_code=country_code)
    
    missing_vals = filtered_data.loc[filtered_data['Value'].isna()]

    figure = px.bar(
        missing_vals.Country.value_counts()[:11],
        title='Missing values in source data',
        orientation='h',
        height=400
    )
    figure.update_layout(
        showlegend=False, 
        font=dict(size=9),
        margin=margins,
        title=dict(y=0.85)
    )
    figure.update_xaxes(title='Number of missing values', nticks=10)
    figure.update_yaxes(title='')
    
    return figure


def survey_year_plot(continent_code='All', country_code='All'):
    filtered_data = q.geo_filter(continent_code=continent_code, country_code=country_code) # no filter applied
    figure = px.choropleth(
        filtered_data, 
        locations="country_code",
        hover_name="Country",
        hover_data=["Survey Year"],
        color = "date_bins",
        title='Survey Year',
        category_orders={"date_bins": ["2000 - 2004", "2005 - 2009", "2010 - 2014", "2015 - 2018"]}
    )

    figure.update_layout(
        margin = dict(l=5, b=10, r=10, t=30),
        font=dict(size=9),
        title=dict(yref='paper', yanchor='bottom', y=0.9),
        legend=dict(
            title="Survey conducted in...",
            bgcolor = 'rgba(255,255,255,0.9)',
            yanchor="top",
            y=0.8,
            xanchor="left",
            x=0.01
        )
    )

    return figure


def statement_response_plot(continent_code='All', country_code='All', statement_id=1):
    """
    A husband is justified in hitting or beating his wife
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
        facet_col="Statement",
        facet_col_wrap=1,
        title="Percent of surveyed pop. that agrees with statement averaged over demographic and gender"
    )

    agreement_across_countries.update_layout(
        font=dict(size=9),
        margin=margins,
        coloraxis_colorbar=dict(
            title="% in Agreement",
            tickmode='array',
            tickvals=[i for i in range(0, 100, 5)],
            ticktext=['{x}%'.format(x=x) for x in range(0, 100, 5)]
        )
    )

    agreement_across_countries.for_each_annotation(
        lambda a: a.update(
            text='A husband is justified in hitting or beating his wife' + a.text.split("=")[-1]
        )
    )

    return agreement_across_countries

def ques_gender_scatter_plot(continent_code='All', country_code='All', 
by_demographic='Education', plot_toggle=False):

    filtered_data = q.geo_filter(continent_code=continent_code, country_code=country_code)
    
    if plot_toggle is False:
        figure = px.scatter(
            filtered_data.loc[filtered_data['Demographics Question'] == by_demographic], 
            x="Value",
            y="Statement",
            color="Gender",
            facet_col="Demographics Response",
            title='Agreement as a function of demographic and gender'
            )
    if plot_toggle is True:
        figure = px.box(
            filtered_data.loc[filtered_data['Demographics Question'] == by_demographic],
            x="Value",  
            y="Statement",
            color="Gender",
            facet_col="Demographics Response",
            title='Agreement as a function of demographic and gender'
            )
    
    figure.update_xaxes(title='Percent Agreement')
    figure.for_each_annotation(lambda a: a.update(text=by_demographic + ' = ' + a.text.split("=")[-1]))
    # figure.add_annotation(text="Absolutely-positioned annotation",
    #               xref="paper", yref="paper",
    #               x=0.3, y=0.3, showarrow=False, textangle=-90,
    #               font=dict(size=9), xshift=-200)
    figure.update_layout(
        font=dict(size=9),
        margin = margins
        # legend=dict(
        #     orientation="h",
        #     yanchor="bottom",
        #     y=1,
        #     xanchor="right",
        #     x=0)
        )

    return figure