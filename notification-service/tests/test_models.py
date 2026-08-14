import pytest
from datetime import datetime
from sqlalchemy import String, Text, Enum
from shared_infrastructure.database.base import TenantBase
from notification_service.modules.notifications.models import NotificationLog
from notification_service.modules.notifications.enums import Channel, NotificationStatus, NotificationType


def test_notification_model_imports_and_registers():
    # 1. Assert registration with TenantBase
    assert "notification_logs" in TenantBase.metadata.tables
    table = TenantBase.metadata.tables["notification_logs"]
    
    # 2. Verify column definitions
    assert "id" in table.columns
    assert "recipient_id" in table.columns
    assert "tenant_id" in table.columns
    assert "channel" in table.columns
    assert "notification_type" in table.columns
    assert "subject" in table.columns
    assert "body" in table.columns
    assert "status" in table.columns
    assert "error_message" in table.columns
    assert "created_at" in table.columns
    assert "sent_at" in table.columns

    # 3. Verify types and constraints
    assert isinstance(table.columns["id"].type, String)
    assert table.columns["id"].primary_key is True
    assert isinstance(table.columns["recipient_id"].type, String)
    assert table.columns["recipient_id"].nullable is False
    assert isinstance(table.columns["tenant_id"].type, String)
    assert table.columns["tenant_id"].nullable is False

    assert isinstance(table.columns["channel"].type, Enum)
    assert isinstance(table.columns["notification_type"].type, Enum)
    assert isinstance(table.columns["status"].type, Enum)

    assert isinstance(table.columns["subject"].type, String)
    assert isinstance(table.columns["body"].type, Text)
    assert table.columns["error_message"].nullable is True


def test_enums_contain_correct_constants():
    assert Channel.EMAIL == "email"
    
    assert NotificationStatus.PENDING == "pending"
    assert NotificationStatus.SENT == "sent"
    assert NotificationStatus.FAILED == "failed"

    assert NotificationType.PASSWORD_RESET == "password_reset"
    assert NotificationType.INVITATION == "invitation"
    assert NotificationType.WORKFLOW_APPROVAL == "workflow_approval"
