import os
import re
import json

WORKSPACE = r"d:\work-pilot-clone"
SERVICES = ["auth-service", "hr-service", "it-service", "workflow-service", "ai-service"]

data = {
    "backend_endpoints": [],
    "frontend_api_calls": [],
    "frontend_routes": [],
    "dummy_data": [],
    "todos": []
}

# 1. Backend Endpoints
for svc in SERVICES:
    svc_path = os.path.join(WORKSPACE, svc)
    if not os.path.exists(svc_path):
        continue
    for root, dirs, files in os.walk(svc_path):
        if "site-packages" in root or ".venv" in root or "__pycache__" in root:
            continue
        for file in files:
            if not file.endswith(".py"):
                continue
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Find routes
            route_matches = re.finditer(r'@(?:router|app)\.(get|post|put|patch|delete)\(\s*["\']([^"\']+)["\']', content)
            for m in route_matches:
                method = m.group(1).upper()
                route = m.group(2)
                
                # Check for RequireRole or similar
                roles = []
                func_start = content.find("def ", m.end())
                if func_start != -1:
                    func_end = content.find(":", func_start)
                    func_sig = content[func_start:func_end]
                    
                    role_match = re.search(r'RequireRole\(\[([^\]]+)\]\)', func_sig)
                    if role_match:
                        roles = [r.strip(' "\'') for r in role_match.group(1).split(',')]
                        
                data["backend_endpoints"].append({
                    "service": svc,
                    "file": file,
                    "method": method,
                    "route": route,
                    "roles": roles
                })

# 2. Frontend API Calls
repo_path = os.path.join(WORKSPACE, "frontend", "repositories")
if os.path.exists(repo_path):
    for file in os.listdir(repo_path):
        if not file.endswith(".ts"): continue
        path = os.path.join(repo_path, file)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
            
        call_matches = re.finditer(r'(?:api|hrApi|itApi|aiApi|workflowApi)\.(get|post|put|patch|delete)\(\s*[`"\']([^`"\']+)[`"\']', content)
        for m in call_matches:
            data["frontend_api_calls"].append({
                "repo": file,
                "method": m.group(1).upper(),
                "route": m.group(2)
            })

# 3. Frontend Routes
app_path = os.path.join(WORKSPACE, "frontend", "app")
if os.path.exists(app_path):
    for root, dirs, files in os.walk(app_path):
        for file in files:
            if file == "page.tsx":
                rel_path = os.path.relpath(root, app_path)
                data["frontend_routes"].append("/" + (rel_path if rel_path != "." else ""))

# 4 & 5. Dummy Data & TODOs
frontend_path = os.path.join(WORKSPACE, "frontend")
dummy_keywords = ["dummy", "fake", "mock", "lorem", "john doe", "jane doe", "placeholder", "hardcode"]
todo_keywords = ["todo", "fixme", "hack", "temp"]

if os.path.exists(frontend_path):
    for root, dirs, files in os.walk(frontend_path):
        if "node_modules" in root or ".next" in root: continue
        for file in files:
            if not file.endswith((".tsx", ".ts", ".css")): continue
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    for i, line in enumerate(f):
                        line_lower = line.lower()
                        for kw in dummy_keywords:
                            if kw in line_lower:
                                data["dummy_data"].append({"file": os.path.relpath(path, frontend_path), "line": i+1, "keyword": kw, "content": line.strip()})
                                break
                        for kw in todo_keywords:
                            if kw in line_lower:
                                data["todos"].append({"file": os.path.relpath(path, frontend_path), "line": i+1, "keyword": kw, "content": line.strip()})
                                break
            except UnicodeDecodeError:
                pass

with open(os.path.join(WORKSPACE, "audit_data_v2.json"), "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("Data gathered")
