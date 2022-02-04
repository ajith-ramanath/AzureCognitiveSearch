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

def delete_indexer(idxr):
    pass

def delete_data_source(ds):
    delete_uri = endpoint + "datasources/" + ds["name"] + api_version_str
    r = requests.delete(delete_uri, headers=headers)
    print(r.status_code)

def delete_index(idx):
    delete_uri = endpoint + "datasources/" + idx["name"] + api_version_str
    r = requests.delete(delete_uri, headers=headers)
    print(r.status_code)

# Deal with data sources
def delete_all_data_sources():
    get_uri = endpoint + "datasources" + api_version_str
    response_json = json.loads(requests.get(get_uri, headers=headers).text)
    for source in response_json['value']:
        delete_data_source(source)


def delete_all_indexes():
    get_uri = endpoint + "indexes" + api_version_str
    response_json = json.loads(requests.get(get_uri, headers=headers).text)
    for source in response_json['value']:
        delete_data_source(source)


def delete_all_indexers():
    pass


