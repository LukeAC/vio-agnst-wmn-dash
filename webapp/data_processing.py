import pandas as pd
import numpy as np
from pycountry_convert import country_alpha2_to_continent_code, country_name_to_country_alpha2, country_name_to_country_alpha3 
import plotly.express as px

def load_data():
    global raw_data, country_data, country_survey_data
    
    # import data and format survey year
    raw_data = pd.read_csv('data/violence_data.csv')
    raw_data["Survey Year"] = pd.to_datetime(raw_data["Survey Year"]).dt.year

    # clean raw country codes to facilitate iso alpha code lookup
    country_clean_dict = {
        "Congo Democratic Republic": "Democratic Republic of the Congo",
        "Cote d'Ivoire": "Ivory Coast",
        "Timor-Leste": "East Timor"
        }
    
    cleaned_countries = raw_data.Country.drop_duplicates().replace(
            country_clean_dict
        )
    
    # fetch iso alpha2 and iso alpha 3 country codes
    iso_alphas = pd.DataFrame()
    iso_alphas["iso_alpha2"] = pd.Series(
        map(country_name_to_country_alpha2, cleaned_countries)
    )
    iso_alphas["iso_alpha3"] = pd.Series(
        map(country_name_to_country_alpha3, cleaned_countries)
    )
    iso_alphas["iso_alpha2"] = iso_alphas["iso_alpha2"].replace('TL', 'TP')
    iso_alphas.columns = ["iso_alpha2", "iso_alpha3"]

    # fetch iso alpha continent codes
    countries_df = pd.merge(
        cleaned_countries.reset_index().drop('index', axis=1),
        iso_alphas,
        left_index=True,
        right_index=True
    )
    
    continent_codes = pd.Series(map(country_alpha2_to_continent_code, countries_df.iso_alpha2))

    # merge raw data with proper country and continent iso codes
    country_data = pd.DataFrame(
        {
            "Country": countries_df.Country.replace(
                {y: x for x, y in country_clean_dict.items()}
            ),
            "country_code": countries_df.iso_alpha3,
            "continent_code": continent_codes
        }
    )
    country_survey_data = pd.merge(
        raw_data,
        country_data,
        on='Country',
        how='left'
    )

    # add date bins to data
    country_survey_data["date_bins"] = np.where(
        country_survey_data['Survey Year'] < 2005,
        '2000 - 2004',
        np.where(
            country_survey_data['Survey Year'] < 2010,
            '2005 - 2009', 
            np.where(
                country_survey_data['Survey Year'] < 2015,
                '2010 - 2014',
                '2015 - 2018'
            )
        )
    )

    return None
  

def missing_values_plot():
    missing_vals = raw_data.loc[raw_data['Value'].isna()]
    figure = px.bar(missing_vals.Country.value_counts(), orientation='h')
    return figure


def survey_year_plot():
    processed_data = country_survey_data
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
            orientation="h"
        )
    )

    return figure


def question_response_plot(continent_code='All', country_code='All', question=1):
    """
        1 = '... for at least one specific reason'
        2 = '... if she argues with him'
        3 = '... if she burns the food'
        4 = '... if she goes out without telling him'
        5 = '... if she refuses to have sex with him'
        6 = '... if she neglects the children'
    """
    if question == 1:
        filtered_data = country_survey_data.loc[country_survey_data['Question'] == '... for at least one specific reason']
    elif question == 2:
        filtered_data = country_survey_data.loc[country_survey_data['Question'] == '... if she argues with him']
    elif question == 3:
        filtered_data = country_survey_data.loc[country_survey_data['Question'] == '... if she burns the food']
    elif question == 4:
        filtered_data = country_survey_data.loc[country_survey_data['Question'] == '... if she goes out without telling him']
    elif question == 5:
        filtered_data = country_survey_data.loc[country_survey_data['Question'] == '... if she refuses to have sex with him']
    elif question == 6:
        filtered_data = country_survey_data.loc[country_survey_data['Question'] == '... if she neglects the children']
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
        facet_col_wrap=2,
        width=900, 
        height=800
    )

    agreement_across_countries.update_layout(
        margin=dict(l=10, r=10, t=20, b=10),
        legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1)
    )

    return agreement_across_countries


def quesvalue_scatter_plot(continent_code='All', country_code='All', by_demographic='Education'):
    processed_data = country_survey_data
    if continent_code != 'All':
        processed_data = processed_data.loc[processed_data["continent_code"] == continent_code]
    if country_code != 'All':
        processed_data = processed_data.loc[processed_data["country_code"] == country_code]
    
    figure = px.scatter(
        processed_data.loc[processed_data['Demographics Question'] == by_demographic], 
        y="Question", 
        x="Value", 
        color="Gender", 
        symbol="Demographics Response"
        )

    return figure

def get_unique_countries():
    return [{'label': 'All', 'value': 'All'}] + [{'label': x[0], 'value': x[1]} for x in country_survey_data.loc[:, ['Country', 'country_code']].drop_duplicates().values]

def get_demographics():
    return [{'label': x[0], 'value': x[0]} for x in country_survey_data.loc[:, ['Demographics Question']].drop_duplicates().values]

def get_unique_continents():  
    return [{'label': 'All', 'value': 'All'}] + [{'label': x[0], 'value': x[0]} for x in country_survey_data.loc[:, ['continent_code']].drop_duplicates().values]

load_data()