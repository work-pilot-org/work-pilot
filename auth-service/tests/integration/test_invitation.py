from fastapi.testclient import TestClient
from src.main import app
from unittest.mock import patch
import uuid
import pytest

client = TestClient(app)

def test_invitation_email_failure():
    # Register and login admin
    register_response = client.post(
        "/auth/register",
        json={
            "company_name": f"Invite Test {uuid.uuid4()}",
            "full_name": "Admin User",
            "email": f"admin_{uuid.uuid4()}@example.com",
            "password": "Password123!"
        }
    )
    assert register_response.status_code == 201
    
    login_response = client.post(
        "/auth/login",
        json={
            "email": register_response.json()["email"],
            "password": "Password123!"
        }
    )
    access_token = login_response.json()["access_token"]
    
    # 1. Test: Invitation creation when email provider fails
    emp_email = f"emp_{uuid.uuid4()}@example.com"
    with patch("resend.Emails.send") as mock_send:
        # Mock Resend API failure
        class MockResendException(Exception):
            pass
        
        mock_send.side_effect = MockResendException("Rate limit exceeded")
        
        invite_response = client.post(
            "/invitations",
            json={
                "email": emp_email,
                "role": "EMPLOYEE",
                "employee_id": str(uuid.uuid4())
            },
            headers={"Authorization": f"Bearer {access_token}"}
        )
        
        # Must return 200/201 but with email_sent=False
        assert invite_response.status_code in (200, 201)
        data = invite_response.json()
        assert data["email_sent"] is False
        assert "invite_link" in data
        assert data["invite_link"] is not None
        assert data["status"] == "PENDING"
        
        invitation_id = data["id"]
        
    # 2. Test: Resend invitation when email provider fails
    with patch("resend.Emails.send") as mock_send:
        mock_send.side_effect = MockResendException("Rate limit exceeded")
        
        resend_response = client.post(
            f"/invitations/{invitation_id}/resend",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        
        assert resend_response.status_code == 200
        resend_data = resend_response.json()
        assert resend_data["email_sent"] is False
        assert resend_data["invite_link"] is not None
        assert resend_data["status"] == "PENDING"

    # 3. Test: Successful email delivery for Resend
    with patch("resend.Emails.send") as mock_send:
        # Mock successful send
        mock_send.return_value = {"id": "mock_email_id_123"}
        
        resend_success_response = client.post(
            f"/invitations/{invitation_id}/resend",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        
        assert resend_success_response.status_code == 200
        success_data = resend_success_response.json()
        assert success_data["email_sent"] is True
        assert success_data["invite_link"] is None
