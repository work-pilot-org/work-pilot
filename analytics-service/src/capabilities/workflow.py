from typing import Any, Dict

from shared_infrastructure.database.tenant_session import get_tenant_db_for_service
from src.api.workflow_analytics import get_workflow_performance, get_workflow_bottlenecks


class WorkflowCapabilities:
    """Capabilities related to Workflow execution and bottlenecks."""

    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        
        # In a real setup, you'd get the actual user token or context
        self.current_user = {"schema_name": tenant_id}

    def execute_performance_query(self, filters: Dict[str, Any]) -> Any:
        with get_tenant_db_for_service(self.tenant_id) as db:
            return get_workflow_performance(
                workflow_id=filters.get("workflow_id"),
                execution_status=filters.get("execution_status"),
                db=db,
                current_user=self.current_user,
            )

    def execute_bottleneck_query(self, filters: Dict[str, Any]) -> Any:
        with get_tenant_db_for_service(self.tenant_id) as db:
            return get_workflow_bottlenecks(
                workflow_id=filters.get("workflow_id"),
                step_order=filters.get("step_order"),
                status=filters.get("status"),
                db=db,
                current_user=self.current_user,
            )
