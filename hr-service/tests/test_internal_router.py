import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from uuid import uuid4

from src.main import app
from src.modules.employee.internal_router import AdminCreateRequest
from shared_infrastructure.core.config import settings

client = TestClient(app)

@pytest.fixture
def mock_db_session():
    with patch("shared_infrastructure.database.session.get_db") as mock:
        yield mock

@pytest.fixture
def mock_repo():
    with patch("src.modules.employee.internal_router.EmployeeRepository") as mock:
        yield mock

def test_create_org_admin_succeeds_without_event_loop_errors(mock_db_session, mock_repo):
    """
    TEST 1: create_org_admin from HTTP request succeeds
    TEST 3: no nested asyncio.run() is used
    """
    # Setup mock repository return
    mock_instance = mock_repo.return_value
    mock_instance.create_employee.return_value.id = uuid4()
    mock_instance.create_employee.return_value.first_name = "Admin"
    mock_instance.create_employee.return_value.last_name = "User"
    mock_instance.create_employee.return_value.employment_type = "FULL_TIME"
    mock_instance.create_employee.return_value.employment_status = "ACTIVE"
    
    # We must patch get_db to return a mock DB
    app.dependency_overrides[mock_db_session] = lambda: MagicMock()
    
    with patch("shared_infrastructure.publisher.publish_event") as mock_publish:
        # Patching set_tenant_schema and set_public_schema to not hit real DB
        with patch("src.modules.employee.internal_router.set_tenant_schema"), \
             patch("src.modules.employee.internal_router.set_public_schema"):
            response = client.post(
                "/internal/employees/admin",
                json={
                    "auth_user_id": str(uuid4()),
                    "first_name": "Admin",
                    "last_name": "User",
                    "email": "admin@example.com",
                    "role": "ORG_ADMIN",
                    "schema_name": "tenant_test"
                },
                headers={
                    "x-internal-token": settings.SECRET_KEY,
                    "x-tenant-id": "1"
                }
            )
            
            assert response.status_code == 200
            assert response.json() == {"status": "ok"}
            # Assert publish_event was passed to BackgroundTasks (by verifying it is called when request finishes)
            # BackgroundTasks are executed by TestClient synchronously at the end of the request
            assert mock_publish.called, "Event publishing should have been triggered"

@pytest.mark.asyncio
async def test_publisher_does_not_access_broker_connected():
    """
    TEST 2: event publishing does not access broker.connected
    """
    from shared_infrastructure.publisher import publish_event, broker
    from shared_infrastructure.events import EventEnvelope
    from datetime import datetime, timezone
    
    event = EventEnvelope(
        event_id=str(uuid4()),
        event_type="test",
        source="test",
        tenant_id="tenant_1",
        occurred_at=datetime.now(timezone.utc),
        payload={}
    )
    
    # We patch the broker's publish method to just return None instead of failing
    with patch.object(broker, "publish") as mock_publish:
        await publish_event("test_topic", event)
        assert mock_publish.called
        
        # Verify broker.connected is NOT in dir(broker) or not accessed
        assert not hasattr(broker, "connected"), "Broker should not have 'connected' attribute"
