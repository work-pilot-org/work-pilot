from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo=True
)

SessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine
)


from fastapi import Request

def get_db(request: Request = None):
    # If middleware already created the session, use it
    if request and hasattr(request.state, "db"):
        yield request.state.db
    else:
        # Fallback for scripts/tests that bypass middleware
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()