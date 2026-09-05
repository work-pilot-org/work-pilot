from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from shared_infrastructure.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo=True,
    pool_pre_ping=True,       # Verifies connection is alive before checking out of pool
    pool_recycle=300,         # Recycles connections every 5 minutes
    pool_size=2,              # Sets base pool size (reduced from 10 for Supabase limits)
    max_overflow=3            # Allows extra connections during spikes (reduced from 20)
)

SessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine,
    expire_on_commit=False
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