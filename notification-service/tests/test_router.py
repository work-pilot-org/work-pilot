from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from notification_service.main import app
from notification_service.modules.notifications.router import (
    get_notification_service,
)
from shared_infrastructure.core.dependencies import (
    get_current_user_and_set_schema,
)
from shared_infrastructure.database.session import get_db


client = TestClient(app)


@pytest.fixture
def mock_db():
    db = MagicMock()
    return db


@pytest.fixture
def mock_notification_service():
    service = MagicMock()
    return service


@pytest.fixture(autouse=True)
def override_dependencies(mock_db, mock_notification_service):
    def override_auth():
        return {
            "sub": "user-123",
            "tenant_id": "tenant-123",
            "schema_name": "tenant_123",
            "roles": ["employee"],
        }

    def override_db():
        yield mock_db

    def override_service():
        return mock_notification_service

    app.dependency_overrides[
        get_current_user_and_set_schema
    ] = override_auth

    app.dependency_overrides[get_db] = override_db

    app.dependency_overrides[
        get_notification_service
    ] = override_service

    yield

    app.dependency_overrides.clear()


def valid_payload():
    return {
        "recipient_id": "user-456",
        "recipient_email": "recipient@example.com",
        "channel": "email",
        "notification_type": "workflow_approval",
        "subject": "Approval Required",
        "body": "<p>Please approve this request.</p>",
    }


def test_send_notification_returns_201(
    mock_notification_service,
):
    mock_notification_service.send_notification.return_value = MagicMock(
        id="notification-123",
        recipient_id="user-456",
        channel="email",
        notification_type="workflow_approval",
        subject="Approval Required",
        status="sent",
        created_at="2026-08-11T10:00:00+00:00",
        sent_at="2026-08-11T10:00:01+00:00",
    )

    response = client.post(
        "/notifications",
        json=valid_payload(),
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == "notification-123"
    assert data["recipient_id"] == "user-456"
    assert data["channel"] == "email"
    assert data["notification_type"] == "workflow_approval"
    assert data["status"] == "sent"

    mock_notification_service.send_notification.assert_called_once()

    call_kwargs = (
        mock_notification_service
        .send_notification
        .call_args.kwargs
    )

    assert call_kwargs["tenant_id"] == "tenant-123"


def test_tenant_id_comes_from_authenticated_user(
    mock_notification_service,
):
    mock_notification_service.send_notification.return_value = MagicMock(
        id="notification-123",
        recipient_id="user-456",
        channel="email",
        notification_type="workflow_approval",
        subject="Approval Required",
        status="sent",
        created_at="2026-08-11T10:00:00+00:00",
        sent_at="2026-08-11T10:00:01+00:00",
    )

    payload = valid_payload()

    # Even if a client tries to inject tenant_id,
    # it is not part of NotificationCreate.
    payload["tenant_id"] = "attacker-tenant"

    response = client.post(
        "/notifications",
        json=payload,
    )

    assert response.status_code == 201

    call_kwargs = (
        mock_notification_service
        .send_notification
        .call_args.kwargs
    )

    assert call_kwargs["tenant_id"] == "tenant-123"
    assert call_kwargs["tenant_id"] != "attacker-tenant"


def test_missing_tenant_id_returns_401(
    mock_notification_service,
):
    def override_auth_without_tenant():
        return {
            "sub": "user-123",
            "schema_name": "tenant_123",
            "roles": ["employee"],
        }

    app.dependency_overrides[
        get_current_user_and_set_schema
    ] = override_auth_without_tenant

    response = client.post(
        "/notifications",
        json=valid_payload(),
    )

    assert response.status_code == 401

    data = response.json()

    assert data["detail"] == (
        "Tenant ID is missing from credentials."
    )

    mock_notification_service.send_notification.assert_not_called()


def test_invalid_email_returns_422(
    mock_notification_service,
):
    payload = valid_payload()
    payload["recipient_email"] = "not-an-email"

    response = client.post(
        "/notifications",
        json=payload,
    )

    assert response.status_code == 422

    mock_notification_service.send_notification.assert_not_called()


def test_missing_required_field_returns_422(
    mock_notification_service,
):
    payload = valid_payload()

    del payload["subject"]

    response = client.post(
        "/notifications",
        json=payload,
    )

    assert response.status_code == 422

    mock_notification_service.send_notification.assert_not_called()


def test_invalid_notification_type_returns_422(
    mock_notification_service,
):
    payload = valid_payload()
    payload["notification_type"] = "invalid_type"

    response = client.post(
        "/notifications",
        json=payload,
    )

    assert response.status_code == 422

    mock_notification_service.send_notification.assert_not_called()


def test_service_value_error_returns_400(
    mock_notification_service,
):
    mock_notification_service.send_notification.side_effect = ValueError(
        "Tenant ID is required."
    )

    response = client.post(
        "/notifications",
        json=valid_payload(),
    )

    assert response.status_code == 400

    data = response.json()

    assert data["detail"] == "Tenant ID is required."


def test_internal_init_tenant_unauthorized():
    response = client.post(
        "/internal/notifications/tenants/init",
        json={"schema_name": "tenant_test"},
        headers={"x-internal-token": "wrong-token"},
    )
    assert response.status_code == 403


def test_internal_init_tenant_invalid_schema():
    # Schema name must contain only letters, numbers, and underscores
    from shared_infrastructure.core.config import settings
    response = client.post(
        "/internal/notifications/tenants/init",
        json={"schema_name": "tenant-invalid; DROP TABLE users;"},
        headers={"x-internal-token": settings.SECRET_KEY},
    )
    assert response.status_code == 422


def test_internal_init_tenant_success(mock_db):
    from shared_infrastructure.core.config import settings
    
    # Mock connection execution context
    mock_connection = MagicMock()
    mock_db.connection.return_value = mock_connection
    
    response = client.post(
        "/internal/notifications/tenants/init",
        json={"schema_name": "tenant_test"},
        headers={"x-internal-token": settings.SECRET_KEY},
    )
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    mock_db.commit.assert_called_once()