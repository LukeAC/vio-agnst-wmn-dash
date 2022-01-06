import data_processing as dp

def get_countries_in_continent_code(continent_code='All'):
    all_label = [{'label': 'All', 'value': 'All'}]
    if continent_code == 'All':
        return all_label + [{'label': x[0], 'value': x[1]} for x in dp.transformed_raw_data.loc[:, ['Country', 'country_code']].drop_duplicates().values]
    else:
        return all_label + [{'label': x[0], 'value': x[1]} for x in dp.transformed_raw_data.loc[:, ['Country', 'country_code']].loc[dp.transformed_raw_data['continent_code']==continent_code].drop_duplicates().values]

def get_demographics():
    return [{'label': x[0], 'value': x[0]} for x in dp.transformed_raw_data.loc[:, ['Demographics Question']].drop_duplicates().values]

def get_continent_with_country_code(country_code='All'):
    all_label = [{'label': 'All', 'value': 'All'}]
    if country_code == 'All':
        return all_label + [{'label': x[0], 'value': x[1]} for x in dp.transformed_raw_data.loc[:, ['Continent', 'continent_code']].drop_duplicates().values]
    else:
        return all_label + [{'label': x[0], 'value': x[1]} for x in dp.transformed_raw_data.loc[:, ['Continent', 'continent_code']].loc[dp.transformed_raw_data['country_code']==country_code].drop_duplicates().values]
