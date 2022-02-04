import json
import requests
from pprint import pprint
import datetime

import config

# Get current time
def get_current_time():
    x = datetime.datetime.now().time()
    return str(x).replace(":","-").replace(".", "-")

# Define the names for the data source, skillset, index and indexer
time_of_run = get_current_time()
datasource_name = "cogsrch-py-datasource-" + time_of_run
skillset_name = "cogsrch-py-skillset-" + time_of_run
index_name = "cogsrch-py-index-" + time_of_run
indexer_name = "cogsrch-py-indexer" + time_of_run

# Setup the endpoint
endpoint = config.COG_SEARCH_END_POINT
headers = config.COG_SEARCH_API_HEADERS
params = config.COG_SEARCH_API_PARAMS

# Retrieve storage conn string from the key vault
storage_conn_str = config.STORAGE_CONN_STR

# Create a data source
datasourceConnectionString = storage_conn_str
datasource_payload = {
    "name": datasource_name,
    "description": "Demo files to demonstrate cognitive search capabilities.",
    "type": "azureblob",
    "credentials": {
        "connectionString": datasourceConnectionString
    },
    "container": {
        "name": config.BLOB_CONTAINER
    }
}
r = requests.put(endpoint + "/datasources/" + datasource_name,
                 data=json.dumps(datasource_payload), headers=headers, params=params)
print(r.text)
print(r.status_code)

# Create a skillset
f = open('./skillset.json')
skillset_payload = json.load(f)
skillset_payload["name"] = skillset_name
r = requests.put(endpoint + "/skillsets/" + skillset_name,
                 data=json.dumps(skillset_payload), headers=headers, params=params)
# print(r.text)
print(r.status_code)

# Create an index
f = open('./index.json')
index_payload = json.load(f)
index_payload["name"] = index_name
r = requests.put(endpoint + "/indexes/" + index_name,
                 data=json.dumps(index_payload), headers=headers, params=params)
# print(r.text)
print(r.status_code)

# Create an indexer
f = open('./indexer.json')
indexer_payload = json.load(f)
indexer_payload["name"] = indexer_name
indexer_payload["dataSourceName"] = datasource_name
indexer_payload["targetIndexName"] = index_name
indexer_payload["skillsetName"] = skillset_name
r = requests.put(endpoint + "/indexers/" + indexer_name,
                 data=json.dumps(indexer_payload), headers=headers, params=params)
# print(r.text)
print(r.status_code)