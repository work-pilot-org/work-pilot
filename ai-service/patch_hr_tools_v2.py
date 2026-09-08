import os

HR_TOOLS_DIR = r"d:\work-pilot-clone\ai-service\src\modules\hr\tools"

HELPER_CODE = """
    if employee_id is None:
        me = await hr_client.get_my_employee(headers=headers)
        if not me or "id" not in me:
            return {"error": "[STATUS: FAILED] I couldn't find an employee profile linked to your account. Please contact HR."}
        employee_id = me["id"]"""

def patch_tool(filepath, tool_name, old_sig, new_sig):
    with open(filepath, 'r') as f:
        content = f.read()

    # Find the function signature and add the helper code right after it
    # We look for the exact signature, and append the helper code
    
    if old_sig in content:
        # Check if already patched
        if new_sig in content:
            return
            
        # Replace signature
        content = content.replace(old_sig, new_sig)
        
        # Now find where to insert the helper code
        # The new signature ends with '):' or ':\n'
        # We will split by new_sig and add the helper code
        parts = content.split(new_sig)
        if len(parts) == 2:
            # Check if there's a docstring immediately after
            after = parts[1]
            if after.lstrip().startswith('"""'):
                # Find the end of the docstring
                doc_end = after.find('"""', after.find('"""') + 3) + 3
                parts[1] = after[:doc_end] + "\n" + HELPER_CODE + after[doc_end:]
            else:
                parts[1] = HELPER_CODE + parts[1]
            
            content = new_sig + parts[1]
            content = parts[0] + content
            
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Patched {tool_name} in {filepath}")
    else:
        print(f"Warning: could not find old_sig in {filepath} for {tool_name}")


patch_tool(
    os.path.join(HR_TOOLS_DIR, "leave.py"),
    "get_employee_leave_requests",
    "async def get_employee_leave_requests(\n    employee_id: UUID,\n    headers: dict[str, str] | None = None,\n):",
    "async def get_employee_leave_requests(\n    employee_id: UUID | None = None,\n    headers: dict[str, str] | None = None,\n):"
)

patch_tool(
    os.path.join(HR_TOOLS_DIR, "leave.py"),
    "get_employee_leave_balance",
    "async def get_employee_leave_balance(\n    employee_id: UUID,\n    headers: dict[str, str] | None = None,\n):",
    "async def get_employee_leave_balance(\n    employee_id: UUID | None = None,\n    headers: dict[str, str] | None = None,\n):"
)

patch_tool(
    os.path.join(HR_TOOLS_DIR, "leave.py"),
    "get_employee_leave_summary",
    "async def get_employee_leave_summary(\n    employee_id: UUID,\n    headers: dict[str, str] | None = None,\n):",
    "async def get_employee_leave_summary(\n    employee_id: UUID | None = None,\n    headers: dict[str, str] | None = None,\n):"
)

patch_tool(
    os.path.join(HR_TOOLS_DIR, "attendance.py"),
    "get_employee_attendance",
    "async def get_employee_attendance(\n    employee_id: UUID,\n    headers: dict[str, str] | None = None,\n):",
    "async def get_employee_attendance(\n    employee_id: UUID | None = None,\n    headers: dict[str, str] | None = None,\n):"
)

# For employee.py, we only patch get_employee_profile, get_documents.
# We do not patch update_employee_profile because it might have a payload that would cause SyntaxError, or we can just swap it here safely.
patch_tool(
    os.path.join(HR_TOOLS_DIR, "employee.py"),
    "get_employee_profile",
    "async def get_employee_profile(\n    employee_id: str,\n    headers: dict[str, str] | None = None,\n):",
    "async def get_employee_profile(\n    employee_id: str | None = None,\n    headers: dict[str, str] | None = None,\n):"
)

patch_tool(
    os.path.join(HR_TOOLS_DIR, "employee.py"),
    "get_documents",
    "async def get_documents(\n    employee_id: str,\n    headers: dict[str, str] | None = None,\n):",
    "async def get_documents(\n    employee_id: str | None = None,\n    headers: dict[str, str] | None = None,\n):"
)

patch_tool(
    os.path.join(HR_TOOLS_DIR, "employee.py"),
    "update_employee_profile",
    "async def update_employee_profile(\n    employee_id: str,\n    payload: UpdateEmployeeProfileToolInput,\n    headers: dict[str, str] | None = None,\n):",
    "async def update_employee_profile(\n    payload: UpdateEmployeeProfileToolInput,\n    employee_id: str | None = None,\n    headers: dict[str, str] | None = None,\n):"
)

