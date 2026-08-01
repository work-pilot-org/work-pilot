import os
import re

base_dir = "d:/work-pilot-clone/packages/shared-infrastructure/src/shared_infrastructure"

for root, _, files in os.walk(base_dir):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            with open(path, "r") as f:
                content = f.read()
            
            # Replace `from src.core` with `from shared_infrastructure.core`
            content = re.sub(r'from src\.core', 'from shared_infrastructure.core', content)
            # Replace `from src.infrastructure.database` with `from shared_infrastructure.database`
            content = re.sub(r'from src\.infrastructure\.database', 'from shared_infrastructure.database', content)
            
            with open(path, "w") as f:
                f.write(content)

print("Imports updated in shared-infrastructure.")
