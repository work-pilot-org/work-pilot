import os
from typing import Optional

from azure.kusto.data import KustoClient, KustoConnectionStringBuilder
from azure.kusto.ingest import QueuedIngestClient, IngestionProperties
from azure.kusto.data.helpers import dataframe_from_result_table
from azure.identity import DefaultAzureCredential

# For development, allow using client credentials if set, otherwise fallback to DefaultAzureCredential
ADX_CLUSTER_URI = os.getenv("ADX_CLUSTER_URI", "https://adxworkpilotdev.eastus.kusto.windows.net")
ADX_INGEST_URI = os.getenv("ADX_INGEST_URI", "https://ingest-adxworkpilotdev.eastus.kusto.windows.net")
ADX_DATABASE_NAME = os.getenv("ADX_DATABASE_NAME", "workpilot_analytics")

_kusto_client: Optional[KustoClient] = None
_ingest_client: Optional[QueuedIngestClient] = None

def get_kusto_connection_string(uri: str) -> KustoConnectionStringBuilder:
    """Builds a Kusto connection string using AAD application auth or DefaultAzureCredential."""
    tenant_id = os.getenv("AZURE_TENANT_ID")
    client_id = os.getenv("AZURE_CLIENT_ID")
    client_secret = os.getenv("AZURE_CLIENT_SECRET")

    if tenant_id and client_id and client_secret:
        return KustoConnectionStringBuilder.with_aad_application_key_authentication(
            uri, client_id, client_secret, tenant_id
        )
    
    # Fallback to DefaultAzureCredential (Managed Identity, Azure CLI, etc)
    credential = DefaultAzureCredential()
    return KustoConnectionStringBuilder.with_azure_token_credential(uri, credential)

def get_kusto_client() -> KustoClient:
    """Returns a singleton KustoClient instance for querying data."""
    global _kusto_client
    if _kusto_client is None:
        kcsb = get_kusto_connection_string(ADX_CLUSTER_URI)
        _kusto_client = KustoClient(kcsb)
    return _kusto_client

def get_ingest_client() -> QueuedIngestClient:
    """Returns a singleton QueuedIngestClient instance for ingesting data."""
    global _ingest_client
    if _ingest_client is None:
        kcsb = get_kusto_connection_string(ADX_INGEST_URI)
        _ingest_client = QueuedIngestClient(kcsb)
    return _ingest_client

def get_ingestion_properties(table_name: str, format="json", mapping_reference=None) -> IngestionProperties:
    """Helper to create ingestion properties for a specific table."""
    return IngestionProperties(
        database=ADX_DATABASE_NAME,
        table=table_name,
        data_format=format,
        ingestion_mapping_reference=mapping_reference
    )
