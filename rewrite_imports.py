import os
import re

services = [
    "auth-service",
    "hr-service",
    "workflow-service",
    "ai-service",
    "it-service"
]

replacements = [
    (r'from (?:src|it_service)\.core\.config import', r'from shared_infrastructure.core.config import'),
    (r'from (?:src|it_service)\.core\.dependencies import', r'from shared_infrastructure.core.dependencies import'),
    (r'from (?:src|it_service)\.core\.exceptions import', r'from shared_infrastructure.core.exceptions import'),
    (r'from (?:src|it_service)\.core\.rbac import', r'from shared_infrastructure.core.rbac import'),
    (r'from (?:src|it_service)\.core\.security import', r'from shared_infrastructure.core.security import'),
    (r'from (?:src|it_service)\.infrastructure\.database\.session import', r'from shared_infrastructure.database.session import'),
    (r'from (?:src|it_service)\.infrastructure\.database\.tenant_session import', r'from shared_infrastructure.database.tenant_session import'),
    (r'from (?:src|it_service)\.infrastructure\.database\.base import', r'from shared_infrastructure.database.base import'),
]

for service in services:
    src_dir = f"d:/work-pilot-clone/{service}/src"
    if not os.path.exists(src_dir):
        print(f"Skipping {service}, no src dir")
        continue
        
    for root, _, files in os.walk(src_dir):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                original_content = content
                for old_pattern, new_text in replacements:
                    content = re.sub(old_pattern, new_text, content)
                
                if content != original_content:
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(content)

print("Finished updating imports across microservices.")
