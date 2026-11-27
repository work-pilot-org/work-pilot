from fastapi.testclient import TestClient
from src.main import app
import pytest
from unittest.mock import patch
import uuid

client = TestClient(app)

def test_invitation_acceptance_and_role_assignment():
    """
    Critical production test: Verify invitation acceptance
    correctly creates a user and assigns the role.
    """
    # Create tenant
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
    
    # Login as admin
    login_response = client.post(
        "/auth/login",
        json={
            "email": register_response.json()["email"],
            "password": "Password123!"
        }
    )
    access_token = login_response.json()["access_token"]
    
    # Send Invitation
    emp_email = f"emp_{uuid.uuid4()}@example.com"
    invite_response = client.post(
        "/auth/invitations",
        json={
            "email": emp_email,
            "role": "EMPLOYEE",
            "employee_id": str(uuid.uuid4())
        },
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert invite_response.status_code == 200
    token = invite_response.json()["invitation_token"]

    # Accept Invitation
    with patch("httpx.post") as mock_hr:
        mock_hr.return_value.status_code = 200
        accept_response = client.post(
            "/auth/accept-invitation",
            json={
                "token": token,
                "password": "Password123!",
                "full_name": "New Employee"
            }
        )
        assert accept_response.status_code == 200

    # Employee Login
    emp_login = client.post(
        "/auth/login",
        json={
            "email": emp_email,
            "password": "Password123!"
        }
    )
    assert emp_login.status_code == 200
    
    # Verify Roles
    me_response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {emp_login.json()['access_token']}"}
    )
    assert me_response.status_code == 200
    roles = me_response.json()["roles"]
    assert "EMPLOYEE" in roles
    assert "TENANT_ADMIN" not in roles
