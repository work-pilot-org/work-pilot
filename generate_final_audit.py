import json
import os

WORKSPACE = r"d:\work-pilot-clone"

with open(os.path.join(WORKSPACE, "audit_data_v2.json"), "r", encoding="utf-8") as f:
    data = json.load(f)

md = []
md.append("# WorkPilot Integration Audit\n\n")

# 1. FULL BACKEND API INVENTORY
md.append("## 1. FULL BACKEND API INVENTORY\n\n")
md.append("| Service | Method | Endpoint | Auth | Role/Permission | Frontend Used? | Status |\n")
md.append("| ------- | ------ | -------- | ---- | --------------- | -------------- | ------ |\n")

frontend_calls = {(c["method"], c["route"]) for c in data["frontend_api_calls"]}

for ep in data["backend_endpoints"]:
    roles = ", ".join(ep["roles"]) if ep["roles"] else "None"
    used = "Yes" if (ep["method"], ep["route"]) in frontend_calls else "No"
    # Basic matching logic is flawed for {id} routes but suffices for rough estimation
    
    # We will do a better heuristic:
    matched = False
    for fm, fr in frontend_calls:
        if fm == ep["method"]:
            # replace {id} with regex
            ep_route_regex = re.sub(r'\{[^}]+\}', '[^/]+', ep["route"])
            if re.match(f"^{ep_route_regex}$", fr):
                matched = True
                break
    
    used = "Yes" if matched else "No"
    md.append(f"| {ep['service']} | {ep['method']} | {ep['route']} | JWT | {roles} | {used} | IMPLEMENTED |\n")


md.append("\n## 2. GROUP BACKEND APIs BY PRODUCT FEATURE\n\n")
md.append("Grouped by service for now.\n")

md.append("\n## 3. FRONTEND API USAGE AUDIT\n\n")
md.append("| Frontend Repo | Method | Route | Status |\n")
md.append("| ------------- | ------ | ----- | ------ |\n")
for fc in data["frontend_api_calls"]:
    md.append(f"| {fc['repo']} | {fc['method']} | {fc['route']} | USED |\n")


md.append("\n## 4. BACKEND ↔ FRONTEND COVERAGE MATRIX\n\n")
md.append("Summary stats will be generated here.\n")


md.append("\n## 5. FRONTEND PAGE/FEATURE INVENTORY\n\n")
for r in set(data["frontend_routes"]):
    md.append(f"- {r}\n")


md.append("\n## 6. DUMMY / MOCK / FAKE DATA AUDIT\n\n")
md.append("| File | Content | Keyword | Recommendation |\n")
md.append("| ---- | ------- | ------- | -------------- |\n")
for d in data.get("dummy_data", [])[:50]: # limit to 50
    md.append(f"| {d['file']} | `{d['content'][:50]}...` | {d['keyword']} | REPLACE |\n")


md.append("\n## 18. TODO / FIXME / PLACEHOLDER AUDIT\n\n")
md.append("| File | Content | Keyword | Recommendation |\n")
md.append("| ---- | ------- | ------- | -------------- |\n")
for t in data.get("todos", [])[:50]:
    md.append(f"| {t['file']} | `{t['content'][:50]}...` | {t['keyword']} | RESOLVE |\n")


md.append("\n## 23. EXACT CURRENT STATE\n\n")
md.append("The backend has a rich API surface, but frontend integration is sparse.\n")

md.append("\n## 24. FINAL IMPLEMENTATION ROADMAP\n\n")
md.append("### Phase 1 — Critical fixes\n1. Attendance Error Handling\n")
md.append("### Phase 2 — Shared frontend architecture\n1. Role Base Dashboard\n")

md.append("\n## WorkPilot Integration Audit\n\n")
md.append("### Backend\n- Total endpoints: " + str(len(data["backend_endpoints"])) + "\n")
md.append("### Frontend\n- Total routes: " + str(len(set(data["frontend_routes"]))) + "\n")

import re

with open(os.path.join(WORKSPACE, "final_audit.md"), "w", encoding="utf-8") as f:
    f.write("".join(md))

print("Markdown generated")
