from sqlalchemy.orm import DeclarativeBase


class PublicBase(DeclarativeBase):
    pass


class TenantBase(DeclarativeBase):
    pass