import pandas as pd
import numpy as np
from pycountry_convert import country_alpha2_to_continent_code, country_name_to_country_alpha2, country_name_to_country_alpha3 


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

load_data()