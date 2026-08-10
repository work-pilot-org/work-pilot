import urllib.request
import urllib.error
import json

data = json.dumps({
    'company_name': 'testcomp',
    'full_name': 'Test User',
    'email': 'test123456789@test.com',
    'password': 'Password@123',
    'confirm_password': 'Password@123'
}).encode('utf-8')

req = urllib.request.Request(
    'http://localhost:8001/auth/register',
    data=data,
    headers={'Content-Type': 'application/json', 'Host': 'localhost'}
)

try:
    resp = urllib.request.urlopen(req)
    print(resp.read().decode('utf-8'))
except urllib.error.HTTPError as e:
    print(f'HTTP {e.code}')
    print(e.read().decode('utf-8'))
