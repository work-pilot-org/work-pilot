import urllib.request, json, urllib.error
req = urllib.request.Request(
    'http://localhost:8002/employees/onboard',
    data=json.dumps({
        'first_name': 'nim',
        'last_name': 'shi',
        'email': 'nimshi@cp.com',
        'role': 'EMPLOYEE',
        'employee_code': 'EMP-001',
        'joining_date': '2026-08-07',
        'employment_type': 'FULL_TIME',
        'employment_status': 'ACTIVE'
    }).encode(),
    headers={
        'Content-Type': 'application/json',
        # I need a valid JWT token to authenticate to hr-service
    },
    method='POST'
)
# I don't have a valid JWT. I can't test hr-service easily from python.
