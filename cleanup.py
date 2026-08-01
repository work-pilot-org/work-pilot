import os

services = [
    "auth-service",
    "hr-service",
    "workflow-service",
    "ai-service",
    "it-service"
]

files_to_delete = {
    "core": ["config.py", "dependencies.py", "exceptions.py", "rbac.py", "security.py"],
    "database": ["base.py", "session.py", "tenant_session.py"]
}

for service in services:
    src_dir = f"d:/work-pilot-clone/{service}/src"
    if service == "it-service":
        src_dir = f"d:/work-pilot-clone/{service}/src/it_service"
    
    for category, files in files_to_delete.items():
        if category == "core":
            folder_path = os.path.join(src_dir, "core")
        else:
            folder_path = os.path.join(src_dir, "infrastructure", "database")
            
        for file in files:
            path = os.path.join(folder_path, file)
            if os.path.exists(path):
                os.remove(path)
                print(f"Deleted {path}")

print("Cleaned up duplicated files.")
