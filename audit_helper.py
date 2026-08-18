import os
import glob
import re

services = [
    "auth-service",
    "hr-service",
    "it-service",
    "workflow-service",
    "notification-service",
    "ai-service"
]

def find_routers(service):
    path = f"d:/workpilot/{service}/**/*.py"
    routers = []
    for filepath in glob.glob(path, recursive=True):
        if "router.py" in filepath:
            routers.append(filepath)
    return routers

print("=== OPERATIONAL SERVICES AUDIT ===")
for service in services:
    print(f"\nService: {service}")
    routers = find_routers(service)
    
    for r in routers:
        with open(r, "r", encoding="utf-8") as f:
            content = f.read()
            endpoints = re.findall(r'@router\.(get|post|put|patch|delete)\(.*?\"(.*?)\"', content, re.DOTALL)
            has_publish = "publish_event" in content
            
            print(f"  Module: {os.path.basename(os.path.dirname(r))}")
            print(f"    Publishes events? {'YES' if has_publish else 'NO'}")
            if endpoints:
                for method, path in endpoints:
                    path = path.replace("\n", "").strip()
                    print(f"    - {method.upper()} {path}")
