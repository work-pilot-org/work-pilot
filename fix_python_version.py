import os
import re

directories = [
    ".",
    "ai-service",
    "auth-service",
    "hr-service",
    "it-service",
    "workflow-service",
    "packages/shared-infrastructure"
]

for d in directories:
    path = os.path.join(d, "pyproject.toml")
    if os.path.exists(path):
        with open(path, "r") as f:
            content = f.read()
        
        # Replace requires-python
        content = re.sub(r'requires-python = ">=3\.\d+"', 'requires-python = ">=3.13"', content)
        
        with open(path, "w") as f:
            f.write(content)
            
print("Standardized requires-python to >=3.13 in all pyproject.toml files.")
