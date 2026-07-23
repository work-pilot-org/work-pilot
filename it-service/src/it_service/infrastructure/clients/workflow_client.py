import httpx
from typing import Optional, Any
from uuid import UUID

from it_service.core.config import settings

class WorkflowClient:
    def __init__(self):
        self.base_url = settings.WORKFLOW_SERVICE_URL if hasattr(settings, "WORKFLOW_SERVICE_URL") else "http://workflow-service:8000"

    def start_workflow(self, entity_id: UUID, entity_type: str, workflow_name: str, requested_by: str, token: Optional[str] = None) -> Any:
        """
        Start a workflow execution via the Workflow Service.
        """
        payload = {
            "workflow_id": workflow_name,
            "entity_id": str(entity_id),
            "entity_type": entity_type,
            "started_by": str(requested_by)
        }
        
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        
        with httpx.Client(base_url=self.base_url) as client:
            try:
                response = client.post("/workflow-executions", json=payload, headers=headers, timeout=10.0)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                print(f"Failed to start workflow for {entity_type} {entity_id}: {e}")
                return None

workflow_client = WorkflowClient()
