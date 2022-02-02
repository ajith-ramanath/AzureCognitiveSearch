from os import environ as env
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient

TENANT_ID = env.get("AZURE_TENANT_ID", "")
CLIENT_ID = env.get("AZURE_CLIENT_ID", "")
CLIENT_SECRET = env.get("AZURE_CLIENT_SECRET", "")
KEYVAULT_NAME = env.get("AZURE_KEYVAULT_NAME", "")

def get_kv_client(kv_uri):
    _credential = ClientSecretCredential(
        tenant_id=TENANT_ID,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET
    )
    return SecretClient(vault_url=kv_uri, credential=_credential)

def retreive_secret(key):
    kv_uri = f"https://{KEYVAULT_NAME}.vault.azure.net"
    client = get_kv_client(kv_uri)
    return client.get_secret(key).value