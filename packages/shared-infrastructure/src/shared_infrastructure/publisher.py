import logging
import os

from faststream.kafka import KafkaBroker
from shared_infrastructure.events import EventEnvelope

logger = logging.getLogger(__name__)

KAFKA_URL = os.getenv("KAFKA_URL", "redpanda:29092")

broker = KafkaBroker(KAFKA_URL)


async def publish_event(topic: str, event: EventEnvelope) -> None:
    """Publish a standardized event to Kafka."""

    try:
        if not broker.connected:
            await broker.connect()

        await broker.publish(
            event.model_dump(mode="json"),
            topic,
        )

        logger.info(
            "Kafka event published",
            extra={
                "event_id": str(event.event_id),
                "event_type": event.event_type,
                "topic": topic,
                "tenant_id": event.tenant_id,
            },
        )

    except Exception:
        logger.exception(
            "Failed to publish Kafka event",
            extra={
                "event_id": str(event.event_id),
                "event_type": event.event_type,
                "topic": topic,
                "tenant_id": event.tenant_id,
            },
        )
        raise
