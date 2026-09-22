from typing import Any, List
from azure.kusto.data import ClientRequestProperties
from azure.kusto.data.helpers import dataframe_from_result_table
from src.infrastructure.adx_client import get_kusto_client, ADX_DATABASE_NAME

def get_workflow_performance_adx(tenant_id: str, workflow_id: str = None, execution_status: str = None) -> List[Dict[str, Any]]:
    """Execute KQL query for workflow performance."""
    client = get_kusto_client()
    
    query = """
    declare query_parameters(tenantId:string, wId:string, eStatus:string);
    WorkflowExecutionEvents
    | where TenantId == tenantId
    """
    if workflow_id:
        query += "\n| where WorkflowId == wId"
    if execution_status:
        query += "\n| where ExecutionStatus == eStatus"
        
    query += """
    | summarize 
        total_executions = count(),
        avg_completion_minutes = avg(CompletionMinutes),
        max_completion_minutes = max(CompletionMinutes)
      by WorkflowName, WorkflowType, ExecutionStatus
    """
    
    props = ClientRequestProperties()
    props.set_parameter("tenantId", tenant_id)
    if workflow_id:
        props.set_parameter("wId", workflow_id)
    if execution_status:
        props.set_parameter("eStatus", execution_status)
        
    response = client.execute(ADX_DATABASE_NAME, query, properties=props)
    
    if not response.primary_results:
        return []
        
    df = dataframe_from_result_table(response.primary_results[0])
    
    results = []
    for _, row in df.iterrows():
        results.append({
            "workflow_name": row.get("WorkflowName"),
            "workflow_type": row.get("WorkflowType"),
            "execution_status": row.get("ExecutionStatus"),
            "total_executions": row.get("total_executions"),
            "avg_completion_minutes": round(row.get("avg_completion_minutes") or 0, 1),
            "max_completion_minutes": row.get("max_completion_minutes") or 0,
        })
        
    return results
