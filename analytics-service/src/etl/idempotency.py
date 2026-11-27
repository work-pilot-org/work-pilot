from sqlalchemy.orm import Session
from src.models.events import ProcessedEvent

def is_event_processed(db: Session, event_id: str, event_type: str) -> bool:
    """
    Checks if an event has already been processed to ensure idempotency.
    If it hasn't, it records it in the current transaction.
    
    Returns:
        True: If the event was already processed (consumer should skip).
        False: If the event is new (consumer should process it).
        
    Note: The caller MUST commit the session to persist this record alongside the ETL data.
    """
    existing = db.query(ProcessedEvent).filter(ProcessedEvent.event_id == event_id).first()
    if existing:
        return True
    
    new_event = ProcessedEvent(event_id=event_id, event_type=event_type)
    db.add(new_event)
    return False
