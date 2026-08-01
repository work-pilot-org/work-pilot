import os
import shutil

src_core = "d:/work-pilot-clone/hr-service/src/core"
src_db = "d:/work-pilot-clone/hr-service/src/infrastructure/database"
dest_core = "d:/work-pilot-clone/packages/shared-infrastructure/src/shared_infrastructure/core"
dest_db = "d:/work-pilot-clone/packages/shared-infrastructure/src/shared_infrastructure/database"

os.makedirs(dest_core, exist_ok=True)
os.makedirs(dest_db, exist_ok=True)

for file in ["config.py", "dependencies.py", "exceptions.py", "rbac.py", "security.py"]:
    shutil.copy(os.path.join(src_core, file), os.path.join(dest_core, file))
    
for file in ["base.py", "session.py", "tenant_session.py"]:
    shutil.copy(os.path.join(src_db, file), os.path.join(dest_db, file))

open(os.path.join(dest_core, "__init__.py"), "w").close()
open(os.path.join(dest_db, "__init__.py"), "w").close()

print("Copied files successfully.")
