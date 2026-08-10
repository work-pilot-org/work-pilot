import urllib.request, json, urllib.error
req = urllib.request.Request(
    'http://localhost:8001/internal/invitations',
    data=json.dumps({
        'email': 'nimshi@cp.com',
        'role': 'EMPLOYEE',
        'employee_id': '00000000-0000-0000-0000-000000000000'
    }).encode(),
    headers={
        'Content-Type': 'application/json',
        'X-Internal-Token': '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7',
        'X-Tenant-Id': '1',
        'X-Actor-Id': '00000000-0000-0000-0000-000000000000'
    },
    method='POST'
)
try:
    print(urllib.request.urlopen(req).read().decode())
except urllib.error.HTTPError as e:
    print(e.read().decode())
