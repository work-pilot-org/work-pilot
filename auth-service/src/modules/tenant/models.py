from datetime import datetime
from enum import Enum

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum as SqlEnum,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.base import PublicBase


class TenantStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"


class Tenant(PublicBase):
    __tablename__ = "tenants"
    __table_args__ = {"schema": "public"}

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )
# company name
    company_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )

    schema_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
        index=True,
    )

    status: Mapped[TenantStatus] = mapped_column(
        SqlEnum(TenantStatus),
        default=TenantStatus.ACTIVE,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    # Relationship with Domain
    domains: Mapped[list["Domain"]] = relationship(
        "Domain",
        back_populates="tenant",
        cascade="all, delete-orphan",
    )


class Domain(PublicBase):
    __tablename__ = "domains"
    __table_args__ = {"schema": "public"}

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    domain: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        index=True,
    )

    tenant_id: Mapped[int] = mapped_column(
        ForeignKey("public.tenants.id", ondelete="CASCADE"),
        nullable=False,
    )

    is_primary: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    tenant: Mapped["Tenant"] = relationship(
        "Tenant",
        back_populates="domains",
    )