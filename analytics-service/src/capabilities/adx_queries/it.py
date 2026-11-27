from typing import Any, Dict
from azure.kusto.data import ClientRequestProperties
from azure.kusto.data.helpers import dataframe_from_result_table
from src.infrastructure.adx_client import get_kusto_client, ADX_DATABASE_NAME

def get_ticket_summary_adx(tenant_id: str, category: str = None) -> Dict[str, Any]:
    """Execute KQL query for IT ticket summary."""
    client = get_kusto_client()
    
    query = """
    declare query_parameters(tenantId:string);
    TicketEvents
    | where TenantId == tenantId
    | summarize tickets = count() by Status, Priority
    """
    props = ClientRequestProperties()
    props.set_parameter("tenantId", tenant_id)
    
    response = client.execute(ADX_DATABASE_NAME, query, properties=props)
    
    if not response.primary_results:
        return {"tenant_id": tenant_id, "summary": []}
        
    df = dataframe_from_result_table(response.primary_results[0])
    
    summary = []
    for _, row in df.iterrows():
        summary.append({
            "status": row.get("Status"),
            "priority": row.get("Priority"),
            "tickets": row.get("tickets")
        })
        
    return {"tenant_id": tenant_id, "summary": summary}

def get_asset_assignments_adx(tenant_id: str, status: str = None, category: str = None) -> Dict[str, Any]:
    """Execute KQL query for IT asset assignments."""
    client = get_kusto_client()
    
    # We use arg_max on EventTime to get the latest assignment status per AssetId/AssignmentId combination
    query = """
    declare query_parameters(tenantId:string, filterStatus:string, filterCategory:string);
    AssetEvents
    | where TenantId == tenantId
    | summarize arg_max(EventTime, *) by AssignmentId
    """
    
    if status:
        query += "\n| where AssignmentStatus == filterStatus"
    if category:
        query += "\n| where Category == filterCategory"
        
    props = ClientRequestProperties()
    props.set_parameter("tenantId", tenant_id)
    if status:
        props.set_parameter("filterStatus", status.upper())
    if category:
        props.set_parameter("filterCategory", category)
        
    response = client.execute(ADX_DATABASE_NAME, query, properties=props)
    
    if not response.primary_results:
        return {"tenant_id": tenant_id, "assignments": []}
        
    df = dataframe_from_result_table(response.primary_results[0])
    
    assignments = []
    for _, row in df.iterrows():
        assignments.append({
            "assignment_id": row.get("AssignmentId"),
            "status": row.get("AssignmentStatus"),
            "asset_name": row.get("AssetName"),
            "asset_category": row.get("Category"),
            "asset_current_status": row.get("AssetStatus"),
            # Placeholder/Dummy for missing ADX resolution fields right now
            "assigned_at": str(row.get("EventTime")), 
            "returned_at": None,
            "duration_days": 0,
            "employee_name": "Unknown",
            "employee_email": "Unknown"
        })
        
    return {"tenant_id": tenant_id, "assignments": assignments}
