import re

path = "d:/work-pilot-clone/hr-service/src/modules/attendance/router.py"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("AttendanceService", "AttendanceUseCases")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated router.py")
