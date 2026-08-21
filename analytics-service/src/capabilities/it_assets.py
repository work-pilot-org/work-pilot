from typing import Any, Dict

from shared_infrastructure.database.tenant_session import get_tenant_db_for_service
from src.api.it_analytics import get_asset_assignments

class ITAssetCapabilities:
    """Capabilities related to IT Assets and Assignments."""

    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        
        self.current_user = {"schema_name": tenant_id}

    def execute_assignment_query(self, filters: Dict[str, Any]) -> Any:
        with get_tenant_db_for_service(self.tenant_id) as db:
            return get_asset_assignments(
                status=filters.get("status"),
                category=filters.get("category"),
                db=db,
                current_user=self.current_user,
            )
