import os
import re
import json

SERVICES = ["auth-service", "hr-service", "it-service", "workflow-service"]
WORKSPACE = r"d:\work-pilot-clone"

results = {}

for service in SERVICES:
    service_path = os.path.join(WORKSPACE, service)
    routes = []
    internal_calls = []
    
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
            # Pattern: @router.post("/path", ...)
            # def func_name(...)
            route_matches = re.finditer(r'@(?:router|app)\.(get|post|put|patch|delete)\(\s*["\']([^"\']+)["\']', content)
            for m in route_matches:
                method = m.group(1).upper()
                path = m.group(2)
                
                # Try to find the function name and if it has get_current_user
                func_start = content.find("def ", m.end())
                func_end = content.find(":", func_start)
                func_sig = content[func_start:func_end]
                
                is_public = "get_current_user" not in func_sig
                
                module = os.path.basename(os.path.dirname(file_path))
                if file == "main.py":
                    module = "Core"
                    
                routes.append({
                    "method": method,
                    "path": path,
                    "module": module,
                    "is_public": is_public,
                    "file": file_path
                })
                
            # Find internal calls
            # e.g. hr_client.post(f"/api/v1/...")
            call_matches = re.finditer(r'(hr_client|it_client|auth_client|workflow_client|notification_client)\.(get|post|put|patch|delete)\(\s*f?["\']([^"\']+)["\']', content)
            for m in call_matches:
                client = m.group(1)
                call_method = m.group(2).upper()
                call_path = m.group(3)
                internal_calls.append({
                    "client": client,
                    "method": call_method,
                    "path": call_path,
                    "from_file": file_path
                })
                
    results[service] = {
        "routes": routes,
        "internal_calls": internal_calls
    }

with open(os.path.join(WORKSPACE, "audit_results.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print("Done")
