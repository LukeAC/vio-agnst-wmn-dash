import data_processing as dp

def get_countries_in_continent_code(continent_code='All'):
    if continent_code == 'All':
        return [{'label': 'All', 'value': 'All'}] + [{'label': x[0], 'value': x[1]} for x in dp.country_survey_data.loc[:, ['Country', 'country_code']].drop_duplicates().values]
    else:
        return [{'label': 'All', 'value': 'All'}] + [{'label': x[0], 'value': x[1]} for x in dp.country_survey_data.loc[:, ['Country', 'country_code']].loc[dp.country_survey_data['continent_code']==continent_code].drop_duplicates().values]

def get_demographics():
    return [{'label': x[0], 'value': x[0]} for x in dp.country_survey_data.loc[:, ['Demographics Question']].drop_duplicates().values]

def get_continent_with_country_code(country_code='All'): 
    if country_code == 'All':
        return [{'label': 'All', 'value': 'All'}] + [{'label': x[0], 'value': x[0]} for x in dp.country_survey_data.loc[:, ['continent_code']].drop_duplicates().values]
    else:
        return [{'label': 'All', 'value': 'All'}] + [{'label': x[0], 'value': x[0]} for x in dp.country_survey_data.loc[:, ['continent_code']].loc[dp.country_survey_data['country_code']==country_code].drop_duplicates().values]
