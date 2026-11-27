from datetime import datetime, timezone
import uuid
from typing import Generic, TypeVar, Any
from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")

class EventEnvelope(BaseModel, Generic[T]):
    """Standardized event envelope for all Kafka messages in WorkPilot."""
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique identifier for the event")
    event_type: str = Field(..., description="The type of event (e.g., 'attendance.created')")
    event_version: int = Field(default=1, description="Schema version of the payload")
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="When the event occurred")
    source: str = Field(..., description="The service that emitted this event (e.g., 'hr-service')")
    tenant_id: str = Field(..., description="The tenant this event belongs to")
    payload: T = Field(..., description="The actual event data payload")

    model_config = ConfigDict(populate_by_name=True)
