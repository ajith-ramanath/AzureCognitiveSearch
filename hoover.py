from sys import api_version
from webbrowser import get
import requests, json
import config

# Setup the endpoint
endpoint = config.COG_SEARCH_END_POINT
api_version_str = config.COG_SEARCH_API_VERSION
headers = config.COG_SEARCH_API_HEADERS

def delete_indexer(idxr):
    delete_uri = endpoint + "/indexers/" + idxr["name"] + api_version_str
    r = requests.delete(delete_uri, headers=headers)
    print(r.status_code)

def delete_data_source(ds):
    delete_uri = endpoint + "/datasources/" + ds["name"] + api_version_str
    r = requests.delete(delete_uri, headers=headers)
    print(r.status_code)

def delete_index(idx):
    delete_uri = endpoint + "/indexes/" + idx["name"] + api_version_str
    r = requests.delete(delete_uri, headers=headers)
    print(r.status_code)

def delete_all_data_sources():
    get_uri = endpoint + "/datasources" + api_version_str
    response_json = json.loads(requests.get(get_uri, headers=headers).text)
    for source in response_json['value']:
        delete_data_source(source)

def delete_all_indexes():
    get_uri = endpoint + "/indexes" + api_version_str
    response_json = json.loads(requests.get(get_uri, headers=headers).text)
    for source in response_json['value']:
        delete_index(source)

def delete_all_indexers():
    get_uri = endpoint + "/indexers" + api_version_str
    print(get_uri)
    response_json = json.loads(requests.get(get_uri, headers=headers).text)
    for source in response_json['value']:
        delete_index(source)

delete_all_indexers()
delete_all_indexes()
delete_all_data_sources()

## Do some fancy arg parsing here and call appropriate 
## functions above. TBD