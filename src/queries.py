## Imports
import src.data_processing as dp


def get_labels_countries_in_continent_code(continent_code="All"):
    """
    Returns the labels of all countries within the specified continent argument

    Parameters:
            continent_code (str): a continent code (including "All")

    Returns:
            country label dictionary (dict): label-code dictionary of countries
    """
    all_label = [{"label": "All countries", "value": "All"}]
    if continent_code == "All":
        return all_label + [
            {"label": x[0], "value": x[1]}
            for x in dp.transformed_raw_data.loc[:, ["Country", "country_code"]]
            .drop_duplicates()
            .values
        ]
    else:
        return all_label + [
            {"label": x[0], "value": x[1]}
            for x in dp.transformed_raw_data.loc[:, ["Country", "country_code"]]
            .loc[dp.transformed_raw_data["continent_code"] == continent_code]
            .drop_duplicates()
            .values
        ]


def get_labels_demographics():
    """
    Returns the labels of all demographic groups
    """
    return [
        {"label": x[0], "value": x[0]}
        for x in dp.transformed_raw_data.loc[:, ["Demographics Question"]]
        .drop_duplicates()
        .values
    ]


def get_labels_continent_with_country_code(country_code="All"):
    """
    Returns the label of the continent within which the specified country argument is contained.

    Parameters:
            country_code (str): a country code (including "All")

    Returns:
            continent label dictionary (dict): label-code dictionary of continent
    """
    all_label = [{"label": "All continents", "value": "All"}]
    if country_code == "All":
        return all_label + [
            {"label": x[0], "value": x[1]}
            for x in dp.transformed_raw_data.loc[:, ["Continent", "continent_code"]]
            .drop_duplicates()
            .values
        ]
    else:
        return all_label + [
            {"label": x[0], "value": x[1]}
            for x in dp.transformed_raw_data.loc[:, ["Continent", "continent_code"]]
            .loc[dp.transformed_raw_data["country_code"] == country_code]
            .drop_duplicates()
            .values
        ]


def get_labels_continent_with_continent_code(continent_code="All"):
    """
    Returns string containing continent label given a continent code

    Parameters:
            continent_code (str): a continent code (including "All")

    Returns:
            (str): continent label in formatted string
    """
    prefix = "Continental Summary - {}"
    if continent_code != "All":
        continents = dp.transformed_raw_data.loc[
            :, ["Continent", "continent_code"]
        ].drop_duplicates()
        label = continents.loc[continents["continent_code"] == continent_code][
            "Continent"
        ].values[0]
    else:
        label = "All continents"

    return prefix.format(label)


def get_labels_statements(statement_id=None):
    """
    Returns the formatted label of the statement passed as the argument
    """
    if statement_id != None:
        statements = dp.transformed_raw_data.loc[
            :, ["Statement", "statement_id"]
        ].drop_duplicates()
        label = statements.loc[statements["statement_id"] == statement_id][
            "Statement"
        ].values[0]
        return "Statement: {}".format(label)
    else:
        return


def geo_filter(
    data=dp.transformed_raw_data.copy(), continent_code="All", country_code="All"
):
    """Returns filtered dataset to reflect selected country and continent"""
    if continent_code == "All" and country_code == "All":
        return data

    elif continent_code != "All" and country_code == "All":
        return data.loc[data["continent_code"] == continent_code]

    elif country_code != "All":
        return data.loc[data["country_code"] == country_code]

    else:
        return data


def question_filter(data=dp.transformed_raw_data.copy(), statement_id=1):
    """Returns filtered dataset to reflect selected statement"""
    return data.loc[data["statement_id"] == statement_id]


def demo_filter(data=dp.transformed_raw_data.copy(), by_demographic="Education"):
    """Returns filtered dataset to reflect selected demographic group"""
    return data.loc[data["Demographics Question"] == by_demographic]
