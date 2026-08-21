import pytest
import httpx
import uuid
import time
from datetime import datetime
from shared_infrastructure.core.security import create_access_token

HR_SERVICE_URL = "http://localhost:8002"
ANALYTICS_SERVICE_URL = "http://localhost:8007"
IT_SERVICE_URL = "http://localhost:8004"
WORKFLOW_SERVICE_URL = "http://localhost:8006"

@pytest.fixture
def test_tenant_and_token():
    tenant_id = str(uuid.uuid4())
    user_id = str(uuid.uuid4())
    token = create_access_token(data={
        "sub": user_id,
        "tenant_id": tenant_id,
        "schema_name": f"tenant_{tenant_id.replace('-', '_')}",
        "role": "ADMIN",
        "permissions": ["hr:manage", "it:manage", "workflow:manage", "attendance:manage"]
    })
    
    headers = {"Authorization": f"Bearer {token}", "x-tenant-id": tenant_id}
    return tenant_id, user_id, headers

@pytest.mark.asyncio
async def test_hr_attendance_e2e(test_tenant_and_token):
    tenant_id, user_id, headers = test_tenant_and_token
    tenant_schema = f"tenant_{tenant_id.replace('-', '_')}"
    employee_id = str(uuid.uuid4())
    
    async with httpx.AsyncClient() as client:
        # 0. Initialize schemas
        internal_headers = {"x-internal-token": "default_secret"}
        await client.post(
            f"{HR_SERVICE_URL}/internal/employees/tenants/init",
            json={"schema_name": tenant_schema},
            headers=internal_headers
        )
        # Assuming Analytics service also needs schema initialization, wait, Analytics uses TenantBase too. 
        # But Analytics doesn't have an internal router exposed for this yet? Let's just create an employee first.
        # 1. We must mock the employee creation in Analytics DB since HR DB and Analytics DB might not sync instantly if we don't wait.
        # Wait, the HR API will reject attendance check-in if the employee doesn't exist in HR DB!
        # Let's create an employee in HR service first!
        emp_resp = await client.post(
            f"{HR_SERVICE_URL}/employees",
            json={
                "first_name": "E2E",
                "last_name": "User",
                "email": f"e2e_{uuid.uuid4().hex}@example.com",
                "employment_type": "FTE",
                "auth_user_id": user_id
            },
            headers=headers
        )
        # If tenant doesn't exist in HR DB, it might fail? 
        # Actually HR Service has an internal endpoint to init tenant, or it auto-creates schemas on startup.
        
        # If it fails, let's just assert so we know
        assert emp_resp.status_code in (201, 200), f"Failed to create employee: {emp_resp.text}"
        emp_data = emp_resp.json()
        real_emp_id = emp_data["id"]

        # 2. Check In
        att_resp = await client.post(
            f"{HR_SERVICE_URL}/attendance/check-in",
            json={
                "employee_id": real_emp_id,
                "note": "E2E Checkin"
            },
            headers=headers
        )
        assert att_resp.status_code in (200, 201), f"Failed to check in: {att_resp.text}"

        # 3. Wait for FastStream to consume and ETL to load
        time.sleep(2)

        # 4. Check Analytics Service
        analytics_resp = await client.get(
            f"{ANALYTICS_SERVICE_URL}/hr/attendance-summary",
            headers=headers
        )
        assert analytics_resp.status_code == 200, f"Analytics API failed: {analytics_resp.text}"
        
        data = analytics_resp.json()
        assert isinstance(data, list)
        
        # We expect at least one attendance record since we just checked in!
        assert len(data) >= 1
        
        # Look for the status
        statuses = [d.get("status") for d in data]
        assert "CHECK_IN" in statuses or "PRESENT" in statuses
