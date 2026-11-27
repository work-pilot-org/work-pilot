import sys
import os
sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, r'D:\work-pilot-clone\packages\shared-infrastructure\src')
# Force 'src' to be analytics-service/src
import importlib.util
spec = importlib.util.spec_from_file_location('src', r'D:\work-pilot-clone\analytics-service\src\__init__.py')
src = importlib.util.module_from_spec(spec)
sys.modules['src'] = src
spec.loader.exec_module(src)

import alembic.config
alembic.config.main(argv=['--raiseerr', 'upgrade', 'head'])
