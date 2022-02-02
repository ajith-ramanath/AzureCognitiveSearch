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

# Retrieve the cog search admin key from key vault
cog_search_key = config.retreive_secret("cog-search-admin-key")

# Setup the endpoint
endpoint = 'https://team6textanalytics-asbwqm5wr7ncmbs.search.windows.net/'
headers = {'Content-Type': 'application/json',
           'api-key': cog_search_key}
params = {
    'api-version': '2020-06-30'
}

# Retrieve storage conn string from the key vault
storage_conn_str = config.retreive_secret("storage-conn-string")

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
        "name": "collateral"
    }
}
r = requests.put(endpoint + "/datasources/" + datasource_name,
                 data=json.dumps(datasource_payload), headers=headers, params=params)
# print(r.text)
print(r.status_code)

# Create a skillset
skillset_payload = {
    "name": skillset_name,
    "description":
    "Extract entities, detect language and extract key-phrases",
    "skills":
    [
        {
            "@odata.type": "#Microsoft.Skills.Text.V3.EntityRecognitionSkill",
            "categories": ["Organization"],
            "defaultLanguageCode": "en",
            "inputs": [
                {
                    "name": "text", 
                    "source": "/document/content"
                }
            ],
            "outputs": [
                {
                    "name": "organizations", 
                    "targetName": "organizations"
                }
            ]
        },
        {
            "@odata.type": "#Microsoft.Skills.Text.LanguageDetectionSkill",
            "inputs": [
                {
                    "name": "text", 
                    "source": "/document/content"
                }
            ],
            "outputs": [
                {
                    "name": "languageCode",
                    "targetName": "languageCode"
                }
            ]
        },
        {
            "@odata.type": "#Microsoft.Skills.Text.SplitSkill",
            "textSplitMode": "pages",
            "maximumPageLength": 4000,
            "inputs": [
                {
                    "name": "text",
                    "source": "/document/content"
                },
                {
                    "name": "languageCode",
                    "source": "/document/languageCode"
                }
            ],
            "outputs": [
                {
                    "name": "textItems",
                    "targetName": "pages"
                }
            ]
        },
        {
            "@odata.type": "#Microsoft.Skills.Text.KeyPhraseExtractionSkill",
            "context": "/document/pages/*",
            "inputs": [
                {
                    "name": "text", 
                    "source": "/document/pages/*"
                },
                {
                    "name": "languageCode", 
                    "source": "/document/languageCode"
                }
            ],
            "outputs": [
                {
                    "name": "keyPhrases",
                    "targetName": "keyPhrases"
                }
            ]
        }
    ]
}

r = requests.put(endpoint + "/skillsets/" + skillset_name,
                 data=json.dumps(skillset_payload), headers=headers, params=params)
# print(r.text)
print(r.status_code)

# Create an index
index_payload = {
    "name": index_name,
    "fields": [
        {
            "name": "id",
            "type": "Edm.String",
            "key": "true",
            "searchable": "true",
            "filterable": "false",
            "facetable": "false",
            "sortable": "true"
        },
        {
            "name": "content",
            "type": "Edm.String",
            "sortable": "false",
            "searchable": "true",
            "filterable": "false",
            "facetable": "false"
        },
        {
            "name": "url",
            "type": "Edm.String",
            "searchable": "true",
            "filterable": "false",
            "facetable": "false"
        },
        {
            "name": "file_name",
            "type": "Edm.String",
            "searchable": "true",
            "filterable": "false",
            "facetable": "false"
        },
        { 
            "name": "metadata_storage_name", 
            "type": "Edm.String", 
            "searchable": "false", 
            "filterable": "true", 
            "sortable": "true"  
        },
        { 
            "name": "metadata_storage_size", 
            "type": "Edm.Int64", 
            "searchable": "false", 
            "filterable": "true", 
            "sortable": "true"  
        },
        { 
            "name": "metadata_creation_date", 
            "type": "Edm.DateTimeOffset", 
            "searchable": "false",
            "filterable": "true",
            "sortable": "true"
        }
    ]
}

r = requests.put(endpoint + "/indexes/" + index_name,
                 data=json.dumps(index_payload), headers=headers, params=params)
# print(r.text)
print(r.status_code)

# Create an indexer
indexer_payload = {
    "name": indexer_name,
    "dataSourceName": datasource_name,
    "targetIndexName": index_name,
    "skillsetName": skillset_name,
    "fieldMappings": [
        {
            "sourceFieldName": "metadata_storage_path",
            "targetFieldName": "id",
            "mappingFunction":
            {"name": "base64Encode"}
        },
        {
            "sourceFieldName": "content",
            "targetFieldName": "content"
        }
    ],
    "outputFieldMappings":
    [
        {
            "sourceFieldName": "/document/metadata_storage_path",
            "targetFieldName": "url"
        },
        {
            "sourceFieldName": "/document/metadata_storage_name",
            "targetFieldName": "file_name"
        }
    ],
    "parameters":
    {
        "maxFailedItems": -1,
        "maxFailedItemsPerBatch": -1,
        "configuration":
        {
            "dataToExtract": "contentAndMetadata",
            "imageAction": "generateNormalizedImages"
        }
    }
}

r = requests.put(endpoint + "/indexers/" + indexer_name,
                 data=json.dumps(indexer_payload), headers=headers, params=params)
# print(r.text)
print(r.status_code)