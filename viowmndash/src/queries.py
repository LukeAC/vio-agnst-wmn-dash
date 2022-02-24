import src.data_processing as dp


def get_labels_countries_in_continent_code(continent_code="All"):
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
    return [
        {"label": x[0], "value": x[0]}
        for x in dp.transformed_raw_data.loc[:, ["Demographics Question"]]
        .drop_duplicates()
        .values
    ]


def get_labels_continent_with_country_code(country_code="All"):
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
    if statement_id == None:
        return [
            {"label": x[0], "value": x[1]}
            for x in dp.transformed_raw_data.loc[:, ["Statement", "statement_id"]]
            .drop_duplicates()
            .values
        ]
    else:
        statements = dp.transformed_raw_data.loc[
            :, ["Statement", "statement_id"]
        ].drop_duplicates()
        label = statements.loc[statements["statement_id"] == statement_id][
            "Statement"
        ].values[0]
        return "Statement: {}".format(label)


def geo_filter(
    data=dp.transformed_raw_data.copy(), continent_code="All", country_code="All"
):
    if continent_code == "All" and country_code == "All":
        return data

    elif continent_code != "All" and country_code == "All":
        return data.loc[data["continent_code"] == continent_code]

    elif country_code != "All":
        return data.loc[data["country_code"] == country_code]

    else:
        return data


def question_filter(data=dp.transformed_raw_data.copy(), statement_id=1):
    return data.loc[data["statement_id"] == statement_id]


def demo_filter(data=dp.transformed_raw_data.copy(), by_demographic="Education"):
    return data.loc[data["Demographics Question"] == by_demographic]
