from sqlalchemy.orm import DeclarativeBase


class TenantBase(DeclarativeBase):
    """
    Base class for all tenant-specific SQLAlchemy models.

    Models inheriting from this class are mapped using the active
    PostgreSQL schema selected by the TenantMiddleware through
    the search_path.
    """

    pass