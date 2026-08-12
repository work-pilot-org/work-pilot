import requests
import json
import time
import os
import sys

os.environ["SECRET_KEY"] = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

sys.path.append(os.path.join(os.path.dirname(__file__), 'packages', 'shared-infrastructure', 'src'))
from shared_infrastructure.core.security import create_access_token

AI_URL = "http://localhost:8003/ai/chat"

# Generate token
token = create_access_token({
    "sub": "c62f2df3-2947-4952-ab79-111111111111",
    "tenant_id": "tenant_1",
    "schema_name": "tenant_1",
    "roles": ["TENANT_ADMIN"]
})

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}",
    "x-tenant-id": "tenant_1",
    "x-user-id": "c62f2df3-2947-4952-ab79-111111111111", 
    "x-user-role": "TENANT_ADMIN"
}

TESTS = [
    "hi",
    "Show me the employees.",
    "Allocate 1 day of SICK leave to all employees for the year 2026.",
    "Allocate 10 days of SICK leave to all employees for the year 2026.",
]

def main():
    for prompt in TESTS:
        print(f"\n==========================================")
        print(f"Testing Prompt: '{prompt}'")
        print(f"==========================================")
        
        payload = {
            "message": prompt,
        }
        
        start = time.time()
        try:
            response = requests.post(AI_URL, json=payload, headers=HEADERS)
            elapsed = time.time() - start
            print(f"Status Code: {response.status_code}")
            print(f"Time: {elapsed:.2f}s")
            
            if response.status_code == 200:
                data = response.json()
                print("Response:")
                print(json.dumps(data, indent=2))
            else:
                print("Error Response:")
                try:
                    print(json.dumps(response.json(), indent=2))
                except:
                    print(response.text)
        except Exception as e:
            print(f"Request failed: {e}")

if __name__ == '__main__':
    main()
