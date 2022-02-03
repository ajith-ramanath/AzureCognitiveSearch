from sys import api_version
import requests, json
import config

# Retrieve the cog search admin key from key vault
cog_search_key = config.COG_SEARCH_KEY

# Setup the endpoint
endpoint = 'https://team6textanalytics-asbwqm5wr7ncmbs.search.windows.net/'
api_version_str = "?api-version=2020-06-30"
headers = {'Content-Type': 'application/json',
           'api-key': cog_search_key}

def cleanup_all_data_sources():
    # Deal with data sources
    get_uri = endpoint + "datasources" + api_version_str
    response_json = json.loads(requests.get(get_uri, headers=headers).text)

    for source in response_json['value']:
        delete_uri = endpoint + "datasources/" + source["name"] + api_version_str
        r = requests.delete(delete_uri, headers=headers)
        print(r.status_code)

def cleanup_all_indexes():
    pass


def cleanup_all_indexers():
    pass