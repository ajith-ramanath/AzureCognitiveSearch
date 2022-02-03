from os import environ as env
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient

__tenant_id = env.get("AZURE_TENANT_ID", "")
__client_id = env.get("AZURE_CLIENT_ID", "")
__client_secret = env.get("AZURE_CLIENT_SECRET", "")
__key_vault_name = env.get("AZURE_KEYVAULT_NAME", "")

def get_kv_client(kv_uri):
    _credential = ClientSecretCredential(
        tenant_id=__tenant_id,
        client_id=__client_id,
        client_secret=__client_secret
    )
    return SecretClient(vault_url=kv_uri, credential=_credential)

def retreive_secret(key):
    kv_uri = f"https://{__key_vault_name}.vault.azure.net"
    client = get_kv_client(kv_uri)
    return client.get_secret(key).value

COG_SEARCH_KEY = retreive_secret("cog-search-admin-key")
STORAGE_CONN_STR = retreive_secret("storage-conn-string")