import os
from faststream.kafka import KafkaBroker
from faststream import Logger

from shared_infrastructure.events import EventEnvelope
from shared_infrastructure.database.session import SessionLocal
from src.etl.schemas import AttendancePayload, LeavePayload, EmployeePayload, TicketPayload, OrganizationPayload, WorkflowEventPayload
from src.etl.schemas import AssetEventPayload
from src.etl.loaders import load_attendance_event, load_leave_event, load_employee_event, load_ticket_event, load_organization_event, load_workflow_event, load_asset_event

KAFKA_URL = os.getenv("KAFKA_URL", "redpanda:29092")

# We instantiate the broker here, it will be started during FastAPI lifespan
broker = KafkaBroker(KAFKA_URL)

@broker.subscriber("hr.attendance")
async def handle_attendance_event(event: EventEnvelope[AttendancePayload], logger: Logger):
    """
    Consumes hr.attendance events from Kafka and processes them via the ETL pipeline.
    """
    logger.info(f"Received {event.event_type} event: {event.event_id}")
    
    with SessionLocal() as db:
        try:
            load_attendance_event(db, event)
            db.commit()
            logger.info(f"Successfully processed event: {event.event_id}")
        except Exception as e:
            logger.error(f"Failed to process event {event.event_id}: {str(e)}")
            import traceback
            traceback.print_exc()
            db.rollback()
            # Raising the exception ensures Kafka does not commit the offset, 
            # or triggers DLQ if configured in FastStream
            raise e

@broker.subscriber("hr.leave")
async def handle_leave_event(event: EventEnvelope[LeavePayload], logger: Logger):
    """
    Consumes hr.leave events from Kafka and processes them via the ETL pipeline.
    """
    logger.info(f"Received {event.event_type} event: {event.event_id}")
    
    with SessionLocal() as db:
        try:
            load_leave_event(db, event)
            db.commit()
            logger.info(f"Successfully processed event: {event.event_id}")
        except Exception as e:
            logger.error(f"Failed to process event {event.event_id}: {str(e)}")
            import traceback
            traceback.print_exc()
            db.rollback()
            raise e

@broker.subscriber("hr.employee")
async def handle_employee_event(event: EventEnvelope[EmployeePayload], logger: Logger):
    """
    Consumes hr.employee events from Kafka to keep DimEmployee updated.
    """
    logger.info(f"Received {event.event_type} event: {event.event_id}")
    
    with SessionLocal() as db:
        try:
            load_employee_event(db, event)
            db.commit()
            logger.info(f"Successfully processed event: {event.event_id}")
        except Exception as e:
            logger.error(f"Failed to process event {event.event_id}: {str(e)}")
            import traceback
            traceback.print_exc()
            db.rollback()
            raise e

@broker.subscriber("it.ticket")
async def handle_ticket_event(event: EventEnvelope[TicketPayload], logger: Logger):
    """
    Consumes it.ticket events from Kafka to populate FactITTicket.
    """
    logger.info(f"Received {event.event_type} event: {event.event_id}")
    
    with SessionLocal() as db:
        try:
            load_ticket_event(db, event)
            db.commit()
            logger.info(f"Successfully processed event: {event.event_id}")
        except Exception as e:
            logger.error(f"Failed to process event {event.event_id}: {str(e)}")
            import traceback
            traceback.print_exc()
            db.rollback()
            raise e

@broker.subscriber("hr.organization")
async def handle_organization_event(event: EventEnvelope[OrganizationPayload], logger: Logger):
    """
    Consumes hr.organization events from Kafka to update DimDepartment and DimDesignation.
    """
    logger.info(f"Received {event.event_type} event: {event.event_id}")
    
    with SessionLocal() as db:
        try:
            load_organization_event(db, event)
            db.commit()
            logger.info(f"Successfully processed event: {event.event_id}")
        except Exception as e:
            logger.error(f"Failed to process event {event.event_id}: {str(e)}")
            import traceback
            traceback.print_exc()
            db.rollback()
            raise e

@broker.subscriber("workflow.execution")
async def handle_workflow_event(event: EventEnvelope[WorkflowEventPayload], logger: Logger):
    """
    Consumes workflow.execution events from Kafka to update FactWorkflowExecution and FactWorkflowStep.
    """
    logger.info(f"Received {event.event_type} event: {event.event_id}")
    
    with SessionLocal() as db:
        try:
            load_workflow_event(db, event)
            db.commit()
            logger.info(f"Successfully processed event: {event.event_id}")
        except Exception as e:
            logger.error(f"Failed to process event {event.event_id}: {str(e)}")
            import traceback
            traceback.print_exc()
            db.rollback()
            raise e

@broker.subscriber("it.asset")
async def handle_asset_event(event: EventEnvelope[AssetEventPayload], logger: Logger):
    """
    Consumes it.asset events from Kafka to update DimAsset.
    """
    logger.info(f"Received {event.event_type} event: {event.event_id}")
    
    with SessionLocal() as db:
        try:
            load_asset_event(db, event)
            db.commit()
            logger.info(f"Successfully processed event: {event.event_id}")
        except Exception as e:
            logger.error(f"Failed to process event {event.event_id}: {str(e)}")
            import traceback
            traceback.print_exc()
            db.rollback()
            raise e
