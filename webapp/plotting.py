import data_processing as dp
import plotly.express as px
import plotly.graph_objects as go

def missing_values_plot(continent_code='All', country_code='All'):
    if continent_code != 'All':
        filtered_data = dp.transformed_raw_data.loc[dp.transformed_raw_data["continent_code"] == continent_code]
    elif country_code != 'All':
        filtered_data = dp.transformed_raw_data.loc[dp.transformed_raw_data["country_code"] == country_code]
    else:
        filtered_data = dp.transformed_raw_data
    missing_vals = filtered_data.loc[filtered_data['Value'].isna()]
    figure = px.bar(missing_vals.Country.value_counts(), orientation='h')
    figure.update_layout(showlegend=False, font=dict(size=9))
    figure.update_xaxes(title='Number of missing values')
    figure.update_yaxes(title='')
    
    return figure


def survey_year_plot():
    processed_data = dp.transformed_raw_data
    figure = px.choropleth(
        processed_data, 
        locations="country_code",
        hover_name="Country",
        hover_data=["Survey Year"],
        color = "date_bins",
        category_orders={"date_bins": ["2000 - 2004", "2005 - 2009", "2010 - 2014", "2015 - 2018"]}
    )

    figure.update_layout(
        margin=dict(l=20, r=30, t=20, b=20),
        legend=dict(
            title="Survey conducted in...",
            orientation="h",
            font=dict(size=9)
        )
    )

    return figure


def question_response_plot(continent_code='All', country_code='All', question=1):
    """
    A husband is justified in hitting or beating his wife
        1 = '... for at least one specific reason'
        2 = '... if she argues with him'
        3 = '... if she burns the food'
        4 = '... if she goes out without telling him'
        5 = '... if she refuses to have sex with him'
        6 = '... if she neglects the children'
    """
    if question == 1:
        filtered_data = dp.transformed_raw_data.loc[dp.transformed_raw_data['Question'] == '... for at least one specific reason']
    elif question == 2:
        filtered_data = dp.transformed_raw_data.loc[dp.transformed_raw_data['Question'] == '... if she argues with him']
    elif question == 3:
        filtered_data = dp.transformed_raw_data.loc[dp.transformed_raw_data['Question'] == '... if she burns the food']
    elif question == 4:
        filtered_data = dp.transformed_raw_data.loc[dp.transformed_raw_data['Question'] == '... if she goes out without telling him']
    elif question == 5:
        filtered_data = dp.transformed_raw_data.loc[dp.transformed_raw_data['Question'] == '... if she refuses to have sex with him']
    elif question == 6:
        filtered_data = dp.transformed_raw_data.loc[dp.transformed_raw_data['Question'] == '... if she neglects the children']
    else:
        raise ValueError("The requested question does not exist. Valid value for question argument is integer between 1 and 6.")
    
    if continent_code != 'All':
        filtered_data = filtered_data.loc[filtered_data["continent_code"] == continent_code]
    if country_code != 'All':
        filtered_data = filtered_data.loc[filtered_data["country_code"] == country_code]
    
    country_question = filtered_data.drop(['Survey Year', 'RecordID'], axis=1).groupby([
        "Country",
        "country_code",
        "Question",
        "Demographics Response"
        ]).mean("Value").reset_index()

    agreement_across_countries = px.choropleth(
        country_question, 
        locations="country_code",
        hover_name="Country",
        color="Value",
        facet_col="Question",
        facet_col_wrap=1,
    )

    agreement_across_countries.update_layout(
        legend=dict(
            title="Percent agreement",
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=9)
        )
    )

    agreement_across_countries.for_each_annotation(
        lambda a: a.update(
            text= 'A husband is justified in hitting or beating his wife' + a.text.split("=")[-1]
        )
    )

    return agreement_across_countries

def ques_gender_scatter_plot(continent_code='All', country_code='All', 
by_demographic='Education', plot_toggle=False):

    processed_data = dp.transformed_raw_data
    if continent_code != 'All':
        processed_data = processed_data.loc[processed_data["continent_code"] == continent_code]
    if country_code != 'All':
        processed_data = processed_data.loc[processed_data["country_code"] == country_code]
    
    
    if plot_toggle is False:
        figure = px.scatter(
            processed_data.loc[processed_data['Demographics Question'] == by_demographic], 
            x="Value",
            y="Question",
            color="Gender",
            facet_col="Demographics Response",
            title='Agreement as a function of demographic and gender'
            )
    if plot_toggle is True:
        figure = px.box(
            processed_data.loc[processed_data['Demographics Question'] == by_demographic],
            x="Value",  
            y="Question",
            color="Gender",
            facet_col="Demographics Response",
            title='Agreement as a function of demographic and gender'
            )
    
    figure.update_xaxes(title='Percent Agreement')
    figure.for_each_annotation(lambda a: a.update(text=by_demographic + ' = ' + a.text.split("=")[-1]))
    figure.update_layout(
        font=dict(size=9),
        # legend=dict(
        #     orientation="h",
        #     yanchor="bottom",
        #     y=1,
        #     xanchor="right",
        #     x=0)
        )

    return figure