## Imports
import pandas as pd
import numpy as np
from pycountry_convert import (
    country_alpha2_to_continent_code,
    country_name_to_country_alpha2,
    country_name_to_country_alpha3,
)


def load_data():
    global transformed_raw_data

    # clean raw country codes to facilitate iso alpha code lookup
    country_clean_dict = {
        "Congo Democratic Republic": "Democratic Republic of the Congo",
        "Cote d'Ivoire": "Ivory Coast",
        "Timor-Leste": "East Timor",
    }

    # provide continent names
    continent_names = {
        "AS": "Asia",
        "EU": "Europe",
        "SA": "South America",
        "NA": "North America",
        "AF": "Africa",
    }

    # import data
    raw_data = pd.read_csv("data/violence_data.csv")
    transformed_raw_data = raw_data.copy()

    # format survey year
    transformed_raw_data["Survey Year"] = pd.to_datetime(
        raw_data["Survey Year"]
    ).dt.year

    # rename column, just for simplicity
    transformed_raw_data["Statement"] = raw_data["Question"]
    transformed_raw_data.drop(columns=["Statement"])

    # format country and continent data
    transformed_raw_data["clean_country"] = (
        transformed_raw_data["Country"].copy().replace(country_clean_dict)
    )

    alpha2_country_codes = (
        transformed_raw_data["clean_country"]
        .copy()
        .map(country_name_to_country_alpha2)
        .replace("TL", "TP")
    )

    transformed_raw_data["country_code"] = (
        transformed_raw_data["clean_country"].copy().map(country_name_to_country_alpha3)
    )
    transformed_raw_data["continent_code"] = alpha2_country_codes.copy().map(
        country_alpha2_to_continent_code
    )
    transformed_raw_data["Continent"] = (
        transformed_raw_data["continent_code"].copy().map(continent_names)
    )

    # format question, statement, and demographic data
    statement_ids = {
        "... for at least one specific reason": 1,
        "... if she argues with him": 2,
        "... if she burns the food": 3,
        "... if she goes out without telling him": 4,
        "... if she refuses to have sex with him": 5,
        "... if she neglects the children": 6,
    }

    demo_ordinal = {
        "Higher": 1,
        "Secondary": 2,
        "Primary": 3,
        "No education": 4,
        "Married or living together": 1,
        "Never married": 2,
        "Widowed, divorced, seperated": 3,
        "Employed for cash": 1,
        "Employed for kind": 2,
        "Unemployed": 3,
        "15-24": 1,
        "25-34": 2,
        "35-49": 3,
        "Urban": 1,
        "Rural": 2,
    }

    transformed_raw_data["statement_id"] = (
        transformed_raw_data["Statement"].copy().map(statement_ids)
    )

    transformed_raw_data["demo_ordinal"] = (
        transformed_raw_data["Demographics Response"].copy().map(demo_ordinal)
    )

    # bin survey years
    transformed_raw_data["date_bins"] = np.where(
        transformed_raw_data["Survey Year"] < 2005,
        "2000 - 2004",
        np.where(
            transformed_raw_data["Survey Year"] < 2010,
            "2005 - 2009",
            np.where(
                transformed_raw_data["Survey Year"] < 2015, "2010 - 2014", "2015 - 2018"
            ),
        ),
    )

    return None


load_data()
