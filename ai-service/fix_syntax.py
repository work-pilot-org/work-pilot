import os
import re

HR_TOOLS_DIR = r"d:\work-pilot-clone\ai-service\src\modules\hr\tools"

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # We are looking for something like:
    #     employee_id: UUID | None = None,
    #     payload: SomePayloadType,
    
    # We want to swap them.
    pattern = re.compile(
        r'(\s+)(employee_id:\s*UUID\s*\|\s*None\s*=\s*None,)\s+(\w+:\s*[A-Za-z0-9_]+,)',
        re.DOTALL
    )
    
    def replacer(match):
        indent = match.group(1)
        employee_param = match.group(2)
        payload_param = match.group(3)
        return f"{indent}{payload_param}{indent}{employee_param}"

    new_content = pattern.sub(replacer, content)

    # Let's check for any other parameters without default that follow employee_id
    pattern2 = re.compile(
        r'(\s+)(employee_id:\s*UUID\s*\|\s*None\s*=\s*None,)\s+([a-zA-Z0-9_]+:\s*[a-zA-Z0-9_\[\]\| ]+(?!=\s*None),)',
        re.DOTALL
    )

    new_content2 = new_content
    while True:
        temp = pattern2.sub(replacer, new_content2)
        if temp == new_content2:
            break
        new_content2 = temp

    if new_content2 != content:
        print(f"Fixed {filepath}")
        with open(filepath, 'w') as f:
            f.write(new_content2)

for root, _, files in os.walk(HR_TOOLS_DIR):
    for file in files:
        if file.endswith('.py'):
            fix_file(os.path.join(root, file))

