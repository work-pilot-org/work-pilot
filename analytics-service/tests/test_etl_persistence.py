import asyncio
import pytest
import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from shared_infrastructure.events import EventEnvelope
from shared_infrastructure.core.config import settings
from src.etl.consumers import handle_attendance_event
from src.etl.schemas import AttendancePayload
from src.models.facts import FactAttendance
from src.models.dimensions import DimTenant, DimEmployee, DimDate
from shared_infrastructure.database.session import SessionLocal
from unittest.mock import patch

@pytest.mark.asyncio
async def test_etl_transaction_persistence():
    """
    Verify that FastStream consumer handlers actually commit transactions to the database.
    Session A: Run the handler (which opens its own session internally).
    Session B: Query the database to ensure the data is persisted.
    """
    
    # Setup test identifiers
    tenant_uuid = uuid.uuid4()
    tenant_str = str(tenant_uuid)
    employee_uuid = uuid.uuid4()
    event_id = str(uuid.uuid4())
    occurred_at = datetime.now(timezone.utc)
    
    # 1. Pre-seed required dimensions in a fresh session (Session 0)
    db_setup = SessionLocal()
    try:
        # Seed Tenant
        tenant = DimTenant(tenant_id=tenant_uuid, company_name="Persistence Test Tenant", status="active")
        db_setup.add(tenant)
        
        # Seed Employee
        employee = DimEmployee(
            employee_id=employee_uuid, 
            tenant_id=tenant_uuid,
            first_name="Test",
            last_name="User",
            employment_type="FTE",
            status="active"
        )
        db_setup.add(employee)
        
        # Seed Date (if missing)
        date_int = int(occurred_at.strftime("%Y%m%d"))
        if not db_setup.query(DimDate).filter_by(id=date_int).first():
            db_setup.add(DimDate(
                id=date_int,
                date=occurred_at.date(),
                day=occurred_at.day,
                month=occurred_at.month,
                year=occurred_at.year,
                quarter=(occurred_at.month - 1) // 3 + 1,
                day_of_week=occurred_at.isoweekday(),
                is_weekend=occurred_at.isoweekday() >= 6
            ))
            
        db_setup.commit()
    finally:
        db_setup.close()

    # 2. Create the Event
    payload = AttendancePayload(
        attendance_id=12345,
        employee_id=str(employee_uuid),
        status="CHECK_IN",
        attendance_date=occurred_at.date().isoformat(),
        timestamp=occurred_at
    )
    
    event = EventEnvelope(
        event_id=event_id,
        event_type="attendance.created",
        source="test",
        tenant_id=tenant_str,
        occurred_at=occurred_at,
        payload=payload
    )

    class MockLogger:
        def info(self, msg): pass
        def error(self, msg): pass

    # 3. Process the event (Session A is created inside here)
    with patch("src.etl.loaders.set_tenant_schema"):
        await handle_attendance_event(event, logger=MockLogger())

    # 4. Verification in a BRAND NEW Session (Session B)
    db_verify = SessionLocal()
    try:
        fact = db_verify.query(FactAttendance).filter(FactAttendance.source_event_id == event_id).first()
        assert fact is not None, "Transaction failed to persist! db.commit() is missing or failing."
        assert fact.attendance_status == "CHECK_IN"
        
        # Cleanup
        db_verify.delete(fact)
        db_verify.query(DimEmployee).filter_by(employee_id=employee_uuid).delete()
        db_verify.query(DimTenant).filter_by(tenant_id=tenant_uuid).delete()
        db_verify.commit()
    finally:
        db_verify.close()
