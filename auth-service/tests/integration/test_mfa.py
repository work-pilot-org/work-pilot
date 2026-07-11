import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from src.main import app
from src.infrastructure.database.session import SessionLocal
import pyotp
import uuid

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="module")
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def mock_user_payload():
    unique_id = str(uuid.uuid4())[:8]
    return {
        "company_name": f"Test Company {unique_id}",
        "full_name": "John Doe",
        "email": f"testmfa_{unique_id}@example.com",
        "password": "Password123!",
        "confirm_password": "Password123!"
    }

def test_mfa_flow(client: TestClient, db: Session, mock_user_payload):
    # 1. Register User
    response = client.post("/auth/register", json=mock_user_payload)
    assert response.status_code == 201

    # 2. Login to get token
    login_data = {
        "email": mock_user_payload["email"],
        "password": mock_user_payload["password"]
    }
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    access_token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    # 3. Setup MFA
    response = client.post("/auth/mfa/setup", headers=headers)
    assert response.status_code == 200, f"Setup MFA failed: {response.json()}"
    mfa_data = response.json()
    secret = mfa_data["secret"]
    assert secret is not None
    assert "provisioning_uri" in mfa_data

    # 4. Enable MFA with invalid code
    response = client.post("/auth/mfa/enable", headers=headers, json={"code": "000000"})
    assert response.status_code == 400

    # 5. Enable MFA with valid code
    totp = pyotp.TOTP(secret)
    valid_code = totp.now()
    response = client.post("/auth/mfa/enable", headers=headers, json={"code": valid_code})
    assert response.status_code == 200, f"Expected 200, got {response.status_code} with detail: {response.json()}"

    # 6. Login again, expecting preauth token
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    assert "preauth_token" in response.json()
    assert "access_token" not in response.json()
    preauth_token = response.json()["preauth_token"]

    # 7. Complete MFA Login with invalid code
    response = client.post("/auth/login/mfa", json={
        "preauth_token": preauth_token,
        "code": "000000"
    })
    assert response.status_code == 400

    # 8. Complete MFA Login with valid code
    valid_code_2 = pyotp.TOTP(secret).now()
    response = client.post("/auth/login/mfa", json={
        "preauth_token": preauth_token,
        "code": valid_code_2
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

    # 9. Disable MFA
    final_access_token = response.json()["access_token"]
    final_headers = {"Authorization": f"Bearer {final_access_token}"}
    
    valid_code_3 = pyotp.TOTP(secret).now()
    response = client.post("/auth/mfa/disable", headers=final_headers, json={
        "password": "Password123!",
        "code": valid_code_3
    })
    assert response.status_code == 200

    # 10. Login again, expecting normal login
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "preauth_token" not in response.json()
