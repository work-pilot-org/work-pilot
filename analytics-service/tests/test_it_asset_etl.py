import unittest
import uuid
from datetime import datetime, timedelta
from unittest.mock import patch
import itertools

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from src.models.base import TenantBase
from src.models.dimensions import DimAsset, DimEmployee, DimTenant, DimDate
from src.models.facts import FactAssetAssignment
from src.etl.loaders import load_asset_event
from src.etl.schemas import AssetEventPayload
from shared_infrastructure.events import EventEnvelope

class TestITAssetETL(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        TenantBase.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.db = Session()
        self.tenant_id = str(uuid.uuid4())
        
        self.id_counter = itertools.count(100)
        def set_sqlite_id(mapper, connection, target):
            if hasattr(target, 'id') and target.id is None:
                target.id = next(self.id_counter)
                
        event.listen(TenantBase, 'before_insert', set_sqlite_id, propagate=True)
        self.set_sqlite_id_func = set_sqlite_id
        
        # Pre-seed DimTenant and DimDate
        self.db.add(DimTenant(id=1, tenant_id=uuid.UUID(self.tenant_id) if isinstance(self.tenant_id, str) else self.tenant_id, company_name="tenant_test", status="active"))
        self.db.add(DimDate(
            id=1,
            date=datetime.utcnow().date(),
            day=datetime.utcnow().day,
            month=datetime.utcnow().month,
            year=datetime.utcnow().year,
            quarter=1,
            day_of_week=1,
            is_weekend=False
        ))
        self.db.commit()
        
        self.patcher_schema = patch("src.etl.loaders.set_tenant_schema")
        self.mock_schema = self.patcher_schema.start()
        
        self.patcher_idempotent = patch("src.etl.loaders.is_event_processed", return_value=False)
        self.mock_idempotent = self.patcher_idempotent.start()

    def tearDown(self):
        event.remove(TenantBase, 'before_insert', self.set_sqlite_id_func)
        self.db.close()
        self.patcher_schema.stop()
        self.patcher_idempotent.stop()

    def create_event(self, event_type: str, payload: dict, occurred_at=None) -> EventEnvelope:
        if not occurred_at:
            occurred_at = datetime.utcnow()
        
        return EventEnvelope(
            event_id=str(uuid.uuid4()),
            event_type=event_type,
            tenant_id=self.tenant_id,
            source="test",
            occurred_at=occurred_at,
            payload=AssetEventPayload(**payload)
        )

    def test_asset_lifecycle(self):
        asset_id = uuid.uuid4()
        employee_id = uuid.uuid4()
        assignment_id = uuid.uuid4()
        
        # 1. Asset Created
        created_event = self.create_event("it.asset.created", {
            "asset_id": asset_id,
            "category": "LAPTOP",
            "name": "MacBook Pro",
            "status": "AVAILABLE"
        })
        load_asset_event(self.db, created_event)
        
        dim_asset = self.db.query(DimAsset).filter_by(asset_id=asset_id).first()
        self.assertIsNotNone(dim_asset)
        self.assertEqual(dim_asset.category, "LAPTOP")
        self.assertEqual(dim_asset.name, "MacBook Pro")
        
        # 2. Asset Assigned
        assigned_time = datetime.utcnow()
        assigned_event = self.create_event("it.asset.assigned", {
            "asset_id": asset_id,
            "employee_id": employee_id,
            "assignment_id": assignment_id
        }, occurred_at=assigned_time)
        load_asset_event(self.db, assigned_event)
        
        fact = self.db.query(FactAssetAssignment).filter_by(assignment_id=assignment_id).first()
        self.assertIsNotNone(fact)
        self.assertEqual(fact.assignment_status, "ACTIVE")
        self.assertIsNone(fact.returned_at)
        self.assertIsNone(fact.assignment_duration_days)
        
        # 3. Asset Returned
        returned_time = assigned_time + timedelta(days=5)
        returned_event = self.create_event("it.asset.returned", {
            "asset_id": asset_id,
            "employee_id": employee_id,
            "assignment_id": assignment_id
        }, occurred_at=returned_time)
        load_asset_event(self.db, returned_event)
        
        fact = self.db.query(FactAssetAssignment).filter_by(assignment_id=assignment_id).first()
        self.assertEqual(fact.assignment_status, "RETURNED")
        self.assertEqual(fact.assignment_duration_days, 5)

    def test_asset_out_of_order_events(self):
        asset_id = uuid.uuid4()
        assignment_id = uuid.uuid4()
        
        assigned_time = datetime.utcnow()
        returned_time = assigned_time + timedelta(days=10)
        
        # 1. Return event arrives FIRST - should raise ValueError (DLQ pattern)
        returned_event = self.create_event("it.asset.returned", {
            "asset_id": asset_id,
            "assignment_id": assignment_id
        }, occurred_at=returned_time)
        
        with self.assertRaises(ValueError):
            load_asset_event(self.db, returned_event)
