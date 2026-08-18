from datetime import datetime, timezone
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import TenantBase

class ProcessedEvent(TenantBase):
    """
    Idempotency table to track which events have already been successfully processed by the ETL pipeline.
    """
    __tablename__ = "processed_events"

    event_id: Mapped[str] = mapped_column(String, primary_key=True)
    event_type: Mapped[str] = mapped_column(String, nullable=False, index=True)
    processed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class DlqEvent(TenantBase):
    """
    Secondary PostgreSQL fallback for Dead Letter Queue if Kafka publishing fails.
    """
    __tablename__ = "dlq_events"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    event_id: Mapped[str] = mapped_column(String, index=True)
    event_type: Mapped[str] = mapped_column(String)
    topic: Mapped[str] = mapped_column(String)
    payload: Mapped[str] = mapped_column(String)
    error_message: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

