from collections.abc import Generator

from fastapi import Request
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from it_service.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


def get_db(request: Request = None) -> Generator[Session]:
    """
    Return the SQLAlchemy session for the current request.

    If the TenantMiddleware has already created a session,
    reuse that session.

    Otherwise create a temporary session (used by tests,
    scripts, or background jobs).
    """

    if request and hasattr(request.state, "db"):
        yield request.state.db
        return

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()