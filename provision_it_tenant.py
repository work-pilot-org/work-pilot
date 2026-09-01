"""
One-shot script to provision IT-service tenant tables for the existing
tenant_ashif schema. Run this once after deploying the code fix.

Usage:
  python provision_it_tenant.py [schema_name]

Defaults to tenant_ashif if no argument provided.
"""
import sys
import os
import httpx

SCHEMA_NAME = sys.argv[1] if len(sys.argv) > 1 else "tenant_ashif"
IT_SERVICE_URL = os.getenv("IT_SERVICE_URL", "http://localhost:8004")
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7",
)

url = f"{IT_SERVICE_URL}/internal/tickets/tenants/init"
print(f"Provisioning IT tables for schema '{SCHEMA_NAME}' via {url} ...")

response = httpx.post(
    url,
    json={"schema_name": SCHEMA_NAME},
    headers={"X-Internal-Token": SECRET_KEY},
    timeout=120.0,
)

print(f"Status: {response.status_code}")
print(f"Body:   {response.text}")

if response.status_code in (200, 201):
    print("✓ IT-service tables created successfully.")
else:
    print("✗ Failed. Check IT service logs.")
    sys.exit(1)
