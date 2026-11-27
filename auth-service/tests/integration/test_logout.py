import pytest
from fastapi.testclient import TestClient

from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_logout_invalidates_refresh_token():
    # 1. Register a new tenant to get credentials
    register_response = client.post(
        "/auth/register",
        json={
            "company_name": "Logout Test Inc",
            "full_name": "Logout Tester",
            "email": "logout.test@example.com",
            "password": "Password123!"
        }
    )
    assert register_response.status_code == 201

    # 2. Login to get a refresh token
    login_response = client.post(
        "/auth/login",
        json={
            "email": "logout.test@example.com",
            "password": "Password123!"
        }
    )
    assert login_response.status_code == 200
    
    # Extract the refresh token cookie
    cookies = login_response.cookies
    refresh_token = cookies.get("refresh_token")
    assert refresh_token is not None, "Login should return a refresh_token cookie"

    # 3. Refresh token should work initially
    refresh_response_1 = client.post(
        "/auth/refresh",
        cookies={"refresh_token": refresh_token}
    )
    assert refresh_response_1.status_code == 200, "Refresh token should work before logout"

    # 4. Logout
    logout_response = client.post(
        "/auth/logout",
        cookies={"refresh_token": refresh_token}
    )
    assert logout_response.status_code == 200, "Logout should succeed"

    # 5. Refresh token should NOT work after logout
    refresh_response_2 = client.post(
        "/auth/refresh",
        cookies={"refresh_token": refresh_token}
    )
    assert refresh_response_2.status_code == 401, "Refresh token should be invalid after logout"
    assert "revoked" in refresh_response_2.json()["detail"].lower()
