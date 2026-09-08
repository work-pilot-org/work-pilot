import re
import os

IT_TOOLS_DIR = r"d:\work-pilot-clone\ai-service\src\modules\it\tools"

def patch_file(filepath, tool_name, fallback_method, requires_assigned_to_check=False):
    with open(filepath, 'r') as f:
        content = f.read()

    # Find the function
    # Example: 
    # async def list_assets(
    # ...
    # ):
    # ...
    #     return await it_client.list_assets(...)
    
    # We want to replace the body of the function with try/except
    
    # This is a bit tricky to regex cleanly, so let's do a simple string replace
    
    if tool_name == "list_assets":
        old_body = """    return await it_client.list_assets(
        category=category,
        status=status,
        assigned_to=assigned_to,
        search=search,
        skip=skip,
        limit=limit,
         headers=headers)"""
         
        new_body = """    try:
        return await it_client.list_assets(
            category=category,
            status=status,
            assigned_to=assigned_to,
            search=search,
            skip=skip,
            limit=limit,
            headers=headers
        )
    except Exception as e:
        if "403" in str(e) and assigned_to is None:
            return await it_client.list_my_assets(
                category=category,
                status=status,
                search=search,
                skip=skip,
                limit=limit,
                headers=headers
            )
        raise e"""
        content = content.replace(old_body, new_body)

    elif tool_name == "list_tickets":
        old_body = """    return await it_client.list_tickets(headers=headers)"""
        new_body = """    try:
        return await it_client.list_tickets(headers=headers)
    except Exception as e:
        if "403" in str(e):
            return await it_client.list_my_tickets(headers=headers)
        raise e"""
        content = content.replace(old_body, new_body)
        
    elif tool_name == "list_access_requests":
        old_body = """    return await it_client.list_access_requests(headers=headers)"""
        new_body = """    try:
        return await it_client.list_access_requests(headers=headers)
    except Exception as e:
        if "403" in str(e):
            return await it_client.list_my_access_requests(headers=headers)
        raise e"""
        content = content.replace(old_body, new_body)
        
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Patched {filepath}")

patch_file(os.path.join(IT_TOOLS_DIR, "assets.py"), "list_assets", "list_my_assets")
patch_file(os.path.join(IT_TOOLS_DIR, "helpdesk.py"), "list_tickets", "list_my_tickets")
patch_file(os.path.join(IT_TOOLS_DIR, "access.py"), "list_access_requests", "list_my_access_requests")

