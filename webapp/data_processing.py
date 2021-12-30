import altair as alt
import pandas as pd
import numpy as np
from IPython.display import display
from pycountry_convert import country_alpha2_to_continent_code, country_name_to_country_alpha2, country_name_to_country_alpha3 
import plotly.express as px

alt.data_transformers.disable_max_rows()

## load in the data and take a look at categorical data

raw_data = pd.read_csv('webapp/data/violence_data.csv')
raw_data["Survey Year"] = pd.to_datetime(raw_data["Survey Year"]).dt.year


## TO DO
## Make this into a function that returns a plotly figure
missing_vals = raw_data.loc[raw_data['Value'].isna()]
missing_vals.Country.value_counts().plot.barh(figsize=(8, 8)).invert_yaxis()
##

def get_country_data(countries, undo_clean=True):
    """
    Input:
    Takes pd.Series of countries

    Performs:
    Fetch geocode information for survey locations in dataset
    Clean data
    Format location output

    Returns:
    Countries with lat/long data
    """
    country_clean_dict = {
        'Congo Democratic Republic': 'Democratic Republic of the Congo',
        "Cote d'Ivoire": "Ivory Coast",
        "Timor-Leste": "East Timor"
        }

    def clean_country_data(data):
        cleaned = data.drop_duplicates().replace(
            country_clean_dict
        )

        return cleaned

    def undo_clean_country_data(data):
        uncleaned = data.replace(
            {y: x for x, y in country_clean_dict.items()}
        )

        return uncleaned

    def generate_iso_codes():
        cleaned_countries = clean_country_data(countries)
        iso_alphas = pd.DataFrame()
        iso_alphas["iso_alpha2"] = pd.Series(
            map(country_name_to_country_alpha2, cleaned_countries)
        )
        iso_alphas["iso_alpha3"] = pd.Series(
            map(country_name_to_country_alpha3, cleaned_countries)
        )
        iso_alphas["iso_alpha2"] = iso_alphas["iso_alpha2"].replace('TL', 'TP')
        iso_alphas.columns = ["iso_alpha2", "iso_alpha3"]

        output = pd.merge(
            cleaned_countries.reset_index().drop('index', axis=1),
            iso_alphas,
            left_index=True,
            right_index=True
            )

        return output

    def transform():
        countries_df = generate_iso_codes()
        continent_codes = pd.Series(map(country_alpha2_to_continent_code, countries_df.iso_alpha2))
        if undo_clean:
            country_data = pd.DataFrame({"Country": undo_clean_country_data(countries_df.Country),
                                        "country_code": countries_df.iso_alpha3,
                                        "continent_code": continent_codes})
            return country_data

        country_data = pd.DataFrame({"Country": countries_df.Country,
                                     "country_code": countries_df.iso_alpha3,
                                     "continent_code": continent_codes})
        return country_data

    return transform()


#####


country_data = get_country_data(raw_data.Country)

country_survey_data = pd.merge(
    raw_data,
    country_data,
    on='Country',
    how='left'
)

#####

def survey_year_plot():
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

    fig = px.choropleth(
        country_survey_data, 
        locations="country_code",
        hover_name="Country",
        hover_data=["Survey Year"],
        color = "date_bins",
        category_orders={"date_bins": ["2000 - 2004", "2005 - 2009", "2010 - 2014", "2015 - 2018"]}
    )

    fig.update_layout(
        margin=dict(l=20, r=30, t=20, b=20),
        legend=dict(
            title="Survey conducted in...",
            orientation="h"
        )
    )
    #fig.show()
    return fig



#################


country_question = country_survey_data.drop(['Survey Year', 'RecordID'], axis=1).groupby([
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

agreement_across_countries.show()

###################


asia_data = country_survey_data.loc[country_survey_data["country_code"] == "AFG"]

asia_data

alt.Chart(asia_data.loc[asia_data['Demographics Question']=='Education']).mark_point(opacity=0.6).encode(
    alt.X('Value'),
    alt.Y('Question'),
    color='Demographics Response'
)