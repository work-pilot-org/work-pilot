import os
import re
import json

SERVICES = ["auth-service", "hr-service", "it-service", "workflow-service"]
WORKSPACE = r"d:\work-pilot-clone"

results = {"endpoints": [], "client_calls": []}

def get_endpoints(service_path, service_name):
    for root, dirs, files in os.walk(service_path):
        if "site-packages" in root or ".venv" in root or "__pycache__" in root:
            continue
        for file in files:
            if not file.endswith(".py"):
                continue
            file_path = os.path.join(root, file)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Find routes
            route_matches = re.finditer(r'@(?:router|app)\.(get|post|put|patch|delete)\(\s*["\']([^"\']+)["\']', content)
            for m in route_matches:
                method = m.group(1).upper()
                path = m.group(2)
                results["endpoints"].append({
                    "service": service_name,
                    "method": method,
                    "path": path,
                    "file": file_path
                })

def get_client_calls(service_path, service_name):
    for root, dirs, files in os.walk(service_path):
        if "site-packages" in root or ".venv" in root or "__pycache__" in root:
            continue
        for file in files:
            if not file.endswith(".py"):
                continue
            file_path = os.path.join(root, file)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Find internal calls
            call_matches = re.finditer(r'(hr_client|it_client|auth_client|workflow_client|notification_client)\.(get|post|put|patch|delete)\(\s*f?["\']([^"\']+)["\']', content)
            for m in call_matches:
                client = m.group(1)
                method = m.group(2).upper()
                path = m.group(3)
                
                target_service = client.replace('_client', '-service')
                results["client_calls"].append({
                    "caller_service": service_name,
                    "target_service": target_service,
                    "method": method,
                    "path": path,
                    "file": file_path
                })

for service in SERVICES:
    service_path = os.path.join(WORKSPACE, service)
    get_endpoints(service_path, service)
    get_client_calls(service_path, service)

# Write to JSON
with open(os.path.join(WORKSPACE, "api_analysis.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print("Analysis complete")
