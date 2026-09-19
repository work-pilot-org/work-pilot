from typing import Any, Dict
from azure.kusto.data import ClientRequestProperties
from azure.kusto.data.helpers import dataframe_from_result_table
from src.infrastructure.adx_client import get_kusto_client, ADX_DATABASE_NAME

def get_attendance_summary_adx(tenant_id: str) -> Dict[str, Any]:
    """Execute KQL query for attendance summary."""
    client = get_kusto_client()
    query = """
    declare query_parameters(tenantId:string);
    AttendanceEvents
    | where TenantId == tenantId
    | summarize 
        total_worked_minutes = sum(WorkedMinutes),
        total_overtime_minutes = sum(OvertimeMinutes),
        total_records = count()
      by Status
    """
    props = ClientRequestProperties()
    props.set_parameter("tenantId", tenant_id)
    
    response = client.execute(ADX_DATABASE_NAME, query, properties=props)
    
    # Safely handle empty results
    if not response.primary_results:
        return {"tenant_id": tenant_id, "summary": []}
        
    df = dataframe_from_result_table(response.primary_results[0])
    
    summary = []
    for _, row in df.iterrows():
        summary.append({
            "status": row.get("Status"),
            "worked_hours": round((row.get("total_worked_minutes") or 0) / 60, 2),
            "overtime_hours": round((row.get("total_overtime_minutes") or 0) / 60, 2),
            "records": row.get("total_records")
        })
        
    return {"tenant_id": tenant_id, "summary": summary}


def get_leave_utilization_adx(tenant_id: str, department: str = None) -> Dict[str, Any]:
    """Execute KQL query for leave utilization."""
    client = get_kusto_client()
    
    query = """
    declare query_parameters(tenantId:string);
    LeaveEvents
    | where TenantId == tenantId
    | summarize 
        total_days = sum(RequestedDays), 
        total_requests = count() 
      by Status
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
            "total_days": row.get("total_days") or 0,
            "requests": row.get("total_requests")
        })
        
    return {"tenant_id": tenant_id, "summary": summary}
