import os
import re

HR_TOOLS_DIR = r"d:\work-pilot-clone\ai-service\src\modules\hr\tools"

HELPER_CODE = """
    if employee_id is None:
        me = await hr_client.get_my_employee(headers=headers)
        if not me or "id" not in me:
            return {"error": "[STATUS: FAILED] I couldn't find an employee profile linked to your account. Please contact HR."}
        employee_id = me["id"]
"""

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Find functions with employee_id: UUID
    # async def get_employee_leave_requests(
    #     employee_id: UUID,
    #     headers: dict[str, str] | None = None,
    # ):

    pattern = re.compile(
        r'(async def [a-zA-Z0-9_]+\(.*?\b)(employee_id):\s*UUID\b([^)]*\):)',
        re.DOTALL
    )

    def replacer(match):
        start = match.group(1)
        param = match.group(2)
        end = match.group(3)
        return f"{start}{param}: UUID | None = None{end}"

    content = pattern.sub(replacer, content)

    # Now inject the helper code into the body of these functions
    
    # We find all async defs that have employee_id: UUID | None = None
    # and inject the code right after the docstring or at the start of the function body.
    
    body_pattern = re.compile(
        r'(async def [a-zA-Z0-9_]+\(.*?\bemployee_id:\s*UUID\s*\|\s*None\s*=\s*None.*?\):\n(?:\s*""".*?"""\n)?)',
        re.DOTALL
    )
    
    def body_replacer(match):
        header = match.group(1)
        return f"{header}{HELPER_CODE}"
        
    new_content = body_pattern.sub(body_replacer, content)

    if new_content != content:
        print(f"Updated {filepath}")
        with open(filepath, 'w') as f:
            f.write(new_content)

for root, _, files in os.walk(HR_TOOLS_DIR):
    for file in files:
        if file.endswith('.py') and file != "__init__.py":
            process_file(os.path.join(root, file))

