
import requests
import json

print("Testing Auth")
auth_url = "http://localhost:8001/auth/login"
payload = {"email": "elon@tesla.com", "password": "password123"}
r = requests.post(auth_url, json=payload)
if r.status_code == 200:
    token = r.json()["access_token"]
    print("Got token")
else:
    print("Failed to get token:", r.text)
    exit(1)

print("Testing AI Chat")
ai_url = "http://localhost:8003/ai/chat"
headers = {"Authorization": f"Bearer {token}"}
r2 = requests.post(ai_url, json={"message": "Hello"}, headers=headers)
print("AI Status:", r2.status_code)
print("AI Response:", r2.text)

