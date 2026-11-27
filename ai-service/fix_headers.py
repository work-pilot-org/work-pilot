import os
import re
import ast

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # We will use regex to find client calls.
    # Pattern looks for something_client.something( ... )
    # Since Python regex doesn't handle nested parentheses easily, 
    # we'll use a simpler heuristic: find 'client.' and then look for the closing parenthesis of the call.
    
    # Actually, a simpler regex replacement for these specific files:
    # Most calls look like:
    # return await it_client.create_asset(
    #     payload=payload,
    # )
    
    # Let's replace ',\n    )' with ',\n        headers=headers,\n    )'
    # and '\n    )' with '\n        headers=headers,\n    )' where it's part of a client call.
    
    # Better approach: parse with AST to find line numbers, but AST modifying and unparsing drops comments.
    
    # Let's do a simple regex:
    # We want to find: \b\w+_client\.\w+\(
    # and then find the balancing parenthesis.
    
    def repl(m):
        # m.group(0) is the entire match
        s = m.group(0)
        if 'headers=headers' in s or 'headers=' in s:
            return s
        # insert headers=headers before the last closing parenthesis
        # but what about trailing commas?
        if s.endswith(',)'):
            return s[:-2] + ', headers=headers)'
        elif s.endswith(', )'):
            return s[:-3] + ', headers=headers)'
        elif s.endswith('\n)'):
            return s[:-2] + ',\n        headers=headers\n)'
        elif s.endswith('\n    )'):
            return s[:-6] + ',\n        headers=headers,\n    )'
        elif s.endswith('\n        )'):
            return s[:-10] + ',\n            headers=headers,\n        )'
        else:
            return s[:-1] + ', headers=headers)'

    # A poor man's parenthesis matcher for python source
    out = []
    idx = 0
    client_pattern = re.compile(r'\b\w+_client\.\w+\(')
    
    changed = False
    
    while idx < len(content):
        match = client_pattern.search(content, idx)
        if not match:
            out.append(content[idx:])
            break
            
        start = match.start()
        out.append(content[idx:start])
        
        # find matching parenthesis
        p_count = 1
        curr = match.end()
        while curr < len(content) and p_count > 0:
            if content[curr] == '(':
                p_count += 1
            elif content[curr] == ')':
                p_count -= 1
            curr += 1
            
        call_str = content[start:curr]
        
        if 'headers=headers' not in call_str and 'headers=' not in call_str:
            # Add headers=headers
            # Check if there are other arguments
            # We insert it right before the last ')'
            last_paren = call_str.rfind(')')
            before = call_str[:last_paren]
            
            # if the before ends with space/newline, we might want to put comma earlier
            if before.strip().endswith(','):
                new_call = before + ' headers=headers' + call_str[last_paren:]
            elif before.strip().endswith('('):
                new_call = before + 'headers=headers' + call_str[last_paren:]
            else:
                new_call = before + ', headers=headers' + call_str[last_paren:]
                
            out.append(new_call)
            changed = True
        else:
            out.append(call_str)
            
        idx = curr

    if changed:
        new_content = "".join(out)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filepath}")


for root, _, files in os.walk('d:/work-pilot-clone/ai-service/src/modules'):
    if 'tools' in root:
        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                process_file(os.path.join(root, file))
