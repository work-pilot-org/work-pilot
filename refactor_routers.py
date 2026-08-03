import os
import re

services = [
    "auth-service",
    "hr-service",
    "workflow-service",
    "ai-service",
    "it-service"
]

def extract_methods(service_path):
    methods = []
    with open(service_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Very naive regex to find method signatures in the Service class
    class_match = re.search(r'class \w+Service[^:]*:', content)
    if not class_match:
        return []
    
    # Extract methods
    method_matches = re.finditer(r'def\s+([a-zA-Z0-9_]+)\s*\([^)]*\)[^:]*:', content)
    for match in method_matches:
        name = match.group(1)
        if name != "__init__":
            methods.append(name)
    return methods

for service in services:
    src_dir = f"d:/work-pilot-clone/{service}/src"
    if service == "it-service":
        src_dir = f"d:/work-pilot-clone/{service}/src/it_service"
    
    modules_dir = os.path.join(src_dir, "modules")
    if not os.path.exists(modules_dir):
        continue
        
    for module in os.listdir(modules_dir):
        module_path = os.path.join(modules_dir, module)
        if not os.path.isdir(module_path):
            continue
            
        service_path = os.path.join(module_path, "service.py")
        router_path = os.path.join(module_path, "router.py")
        usecase_path = os.path.join(module_path, "use_cases.py")
        
        if os.path.exists(service_path) and os.path.exists(router_path):
            # Parse service.py to find the class name
            with open(service_path, "r", encoding="utf-8") as f:
                svc_content = f.read()
            svc_class_match = re.search(r'class (\w+Service)', svc_content)
            if not svc_class_match:
                continue
            svc_class_name = svc_class_match.group(1)
            usecase_class_name = svc_class_name.replace("Service", "UseCases")
            
            # Rewrite router to use UseCases
            with open(router_path, "r", encoding="utf-8") as f:
                router_content = f.read()
            
            router_content = router_content.replace(f"from .service import {svc_class_name}", f"from .use_cases import {usecase_class_name}")
            # Also replace any absolute imports
            router_content = re.sub(rf'from (src|it_service)\.modules\.{module}\.service import {svc_class_name}', rf'from \1.modules.{module}.use_cases import {usecase_class_name}', router_content)
            
            router_content = re.sub(rf'\b{svc_class_name}\b', usecase_class_name, router_content)
            
            with open(router_path, "w", encoding="utf-8") as f:
                f.write(router_content)
            print(f"Updated {router_path}")

print("Router refactoring to UseCases completed (Pass 1).")
