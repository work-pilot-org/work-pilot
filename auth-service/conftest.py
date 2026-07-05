import os
import sys
from pathlib import Path

# Ensure "src" (and the alembic scripts) are importable regardless of the
# directory pytest is invoked from.
AUTH_SERVICE_ROOT = Path(__file__).resolve().parent
if str(AUTH_SERVICE_ROOT) not in sys.path:
    sys.path.insert(0, str(AUTH_SERVICE_ROOT))

# Provide deterministic settings for tests so they do not depend on the
# developer's local .env file (which may be missing required keys or
# point at a real database).
_DEFAULT_TEST_ENV = {
    "APP_NAME": "Auth Service Test",
    "DEBUG": "True",
    "DATABASE_URL": "postgresql+psycopg://postgres:postgres@localhost:5432/test_db",
    "SECRET_KEY": "test-secret-key",
    "ALGORITHM": "HS256",
    "ACCESS_TOKEN_EXPIRE_MINUTES": "30",
    "REFRESH_TOKEN_EXPIRE_DAYS": "7",
}

for _key, _value in _DEFAULT_TEST_ENV.items():
    os.environ.setdefault(_key, _value)