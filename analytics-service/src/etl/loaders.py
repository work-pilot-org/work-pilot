import uuid
from datetime import datetime
from sqlalchemy.orm import Session

from shared_infrastructure.events import EventEnvelope
from shared_infrastructure.database.tenant_session import set_tenant_schema
from src.etl.schemas import AttendancePayload, LeavePayload, EmployeePayload, TicketPayload, OrganizationPayload, WorkflowEventPayload
from src.etl.schemas import AssetEventPayload
from src.models.facts import FactAttendance, FactLeave, FactITTicket, FactWorkflowExecution, FactWorkflowStep, FactAssetAssignment
from src.models.dimensions import DimEmployee, DimDate, DimTenant, DimDepartment, DimDesignation, DimWorkflow, DimAsset
from src.etl.idempotency import is_event_processed

def load_attendance_event(db: Session, event: EventEnvelope[AttendancePayload]):
    """Loads an attendance event into the Star Schema."""
    
    # 1. Tenant Isolation
    set_tenant_schema(db, event.tenant_id)
    
    # 2. Idempotency Check
    if is_event_processed(db, event.event_id, event.event_type):
        return  # Event already processed
        
    payload = event.payload
    
    # 3. Handle Tenant Dimension
    dim_tenant = db.query(DimTenant).first()
    if not dim_tenant:
        dim_tenant = DimTenant(tenant_id=uuid.uuid4(), company_name=event.tenant_id, status="active")
        db.add(dim_tenant)
        db.flush()
        
    # 4. Handle Date Dimension
    dt = datetime.strptime(payload.attendance_date, "%Y-%m-%d").date()
    dim_date = db.query(DimDate).filter(DimDate.date == dt).first()
    if not dim_date:
        dim_date = DimDate(
            date=dt,
            day=dt.day,
            month=dt.month,
            year=dt.year,
            quarter=(dt.month - 1) // 3 + 1,
            day_of_week=dt.weekday(),
            is_weekend=dt.weekday() >= 5
        )
        db.add(dim_date)
        db.flush()
        
    # 5. Handle Employee Dimension (Skeleton)
    emp_uuid = uuid.UUID(payload.employee_id)
    dim_emp = db.query(DimEmployee).filter(DimEmployee.employee_id == emp_uuid).first()
    if not dim_emp:
        dim_emp = DimEmployee(
            employee_id=emp_uuid,
            tenant_id=dim_tenant.tenant_id,
            first_name="Unknown",
            last_name="Employee",
            employment_type="Unknown",
            status="Unknown"
        )
        db.add(dim_emp)
        db.flush()
        
    # 6. UPSERT Fact Attendance
    fact = db.query(FactAttendance).filter(
        FactAttendance.employee_key == dim_emp.id,
        FactAttendance.date_key == dim_date.id
    ).first()
    
    if not fact:
        fact = FactAttendance(
            tenant_key=dim_tenant.id,
            employee_key=dim_emp.id,
            date_key=dim_date.id,
            attendance_status=payload.status,
            worked_minutes=payload.working_minutes or 0,
            late_minutes=0,
            overtime_minutes=payload.overtime_minutes or 0,
            check_in_time=payload.check_in,
            check_out_time=payload.check_out,
            source_event_id=uuid.UUID(event.event_id)
        )
        db.add(fact)
    else:
        fact.attendance_status = payload.status
        fact.worked_minutes = payload.working_minutes or 0
        fact.overtime_minutes = payload.overtime_minutes or 0
        if payload.check_out:
            fact.check_out_time = payload.check_out
            
    # 7. Commit Transaction
    db.commit()


def load_leave_event(db: Session, event: EventEnvelope[LeavePayload]):
    """Loads a leave event into the Star Schema."""
    
    set_tenant_schema(db, event.tenant_id)
    
    if is_event_processed(db, event.event_id, event.event_type):
        return
        
    payload = event.payload
    
    # Ensure DimTenant
    dim_tenant = db.query(DimTenant).first()
    if not dim_tenant:
        dim_tenant = DimTenant(tenant_id=uuid.uuid4(), company_name=event.tenant_id, status="active")
        db.add(dim_tenant)
        db.flush()
        
    # Handle Date Dimension
    dt = datetime.strptime(payload.start_date, "%Y-%m-%d").date()
    dim_date = db.query(DimDate).filter(DimDate.date == dt).first()
    if not dim_date:
        dim_date = DimDate(
            date=dt,
            day=dt.day,
            month=dt.month,
            year=dt.year,
            quarter=(dt.month - 1) // 3 + 1,
            day_of_week=dt.weekday(),
            is_weekend=dt.weekday() >= 5
        )
        db.add(dim_date)
        db.flush()
        
    # Handle Employee Dimension (Skeleton)
    emp_uuid = uuid.UUID(payload.employee_id)
    dim_emp = db.query(DimEmployee).filter(DimEmployee.employee_id == emp_uuid).first()
    if not dim_emp:
        dim_emp = DimEmployee(
            employee_id=emp_uuid,
            tenant_id=dim_tenant.tenant_id,
            first_name="Unknown",
            last_name="Employee",
            employment_type="Unknown",
            status="Unknown"
        )
        db.add(dim_emp)
        db.flush()
        
    # UPSERT Fact Leave
    leave_uuid = uuid.UUID(payload.leave_request_id)
    fact = db.query(FactLeave).filter(
        FactLeave.source_event_id == leave_uuid
    ).first()
    
    if not fact:
        fact = FactLeave(
            tenant_key=dim_tenant.id,
            employee_key=dim_emp.id,
            date_key=dim_date.id,
            source_event_id=leave_uuid,
            leave_days_requested=int(payload.total_days),
            leave_status=payload.status,
            leave_type=payload.leave_type
        )
        db.add(fact)
    else:
        fact.leave_status = payload.status
        fact.leave_days_requested = int(payload.total_days)
            
    db.commit()


def load_employee_event(db: Session, event: EventEnvelope[EmployeePayload]):
    """Loads an employee event to update DimEmployee (SCD Type 1 for now)."""
    
    set_tenant_schema(db, event.tenant_id)
    
    if is_event_processed(db, event.event_id, event.event_type):
        return
        
    payload = event.payload
    
    # Ensure DimTenant
    dim_tenant = db.query(DimTenant).first()
    if not dim_tenant:
        dim_tenant = DimTenant(tenant_id=uuid.uuid4(), company_name=event.tenant_id, status="active")
        db.add(dim_tenant)
        db.flush()
        
    emp_uuid = uuid.UUID(payload.employee_id)
    dim_emp = db.query(DimEmployee).filter(DimEmployee.employee_id == emp_uuid).first()
    
    if not dim_emp:
        dim_emp = DimEmployee(
            employee_id=emp_uuid,
            tenant_id=dim_tenant.tenant_id,
            first_name=payload.first_name,
            last_name=payload.last_name,
            employment_type=payload.employment_type,
            status=payload.status
        )
        db.add(dim_emp)
    else:
        # Update existing employee details
        dim_emp.first_name = payload.first_name
        dim_emp.last_name = payload.last_name
        dim_emp.employment_type = payload.employment_type
        dim_emp.status = payload.status
        
    db.commit()


def load_ticket_event(db: Session, event: EventEnvelope[TicketPayload]):
    """Loads an IT ticket event into the Star Schema."""
    
    set_tenant_schema(db, event.tenant_id)
    
    if is_event_processed(db, event.event_id, event.event_type):
        return
        
    payload = event.payload
    
    # Ensure DimTenant
    dim_tenant = db.query(DimTenant).first()
    if not dim_tenant:
        dim_tenant = DimTenant(tenant_id=uuid.uuid4(), company_name=event.tenant_id, status="active")
        db.add(dim_tenant)
        db.flush()
        
    # Handle Date Dimension
    dt = datetime.fromisoformat(payload.created_at).date()
    dim_date = db.query(DimDate).filter(DimDate.date == dt).first()
    if not dim_date:
        dim_date = DimDate(
            date=dt,
            day=dt.day,
            month=dt.month,
            year=dt.year,
            quarter=(dt.month - 1) // 3 + 1,
            day_of_week=dt.weekday(),
            is_weekend=dt.weekday() >= 5
        )
        db.add(dim_date)
        db.flush()
        
    # Handle Requester Dimension (Skeleton)
    req_uuid = uuid.UUID(payload.requester_id)
    dim_req = db.query(DimEmployee).filter(DimEmployee.employee_id == req_uuid).first()
    if not dim_req:
        dim_req = DimEmployee(
            employee_id=req_uuid,
            tenant_key=dim_tenant.id,
            name="Unknown",
            email="unknown@example.com",
            status="active"
        )
        db.add(dim_req)
        db.flush()
        
    # UPSERT Fact IT Ticket
    ticket_uuid = uuid.UUID(payload.ticket_id)
    fact = db.query(FactITTicket).filter(
        FactITTicket.source_ticket_id == ticket_uuid
    ).first()
    
    if not fact:
        fact = FactITTicket(
            tenant_key=dim_tenant.id,
            requester_key=dim_req.id,
            assigned_to_key=None,
            date_key=dim_date.id,
            source_ticket_id=ticket_uuid,
            ticket_category=payload.category,
            ticket_priority=payload.priority,
            ticket_status=payload.status,
            resolution_time_minutes=None
        )
        db.add(fact)
    else:
        fact.ticket_status = payload.status
        fact.ticket_priority = payload.priority
        fact.ticket_category = payload.category
            
    db.commit()


def load_asset_event(db: Session, event: EventEnvelope[AssetEventPayload]):
    """Loads an IT asset lifecycle event."""
    
    set_tenant_schema(db, event.tenant_id)
    if is_event_processed(db, event.event_id, event.event_type):
        return
        
    payload = event.payload
    
    # 1. Tenant
    dim_tenant = db.query(DimTenant).first()
    if not dim_tenant:
        dim_tenant = DimTenant(tenant_id=uuid.UUID(event.tenant_id) if isinstance(event.tenant_id, str) else event.tenant_id, company_name=event.tenant_id, status="active")
        db.add(dim_tenant)
        db.flush()
        
    # 2. Date
    event_dt = datetime.fromisoformat(str(event.occurred_at).replace('Z', '+00:00')) if isinstance(event.occurred_at, str) else event.occurred_at
    event_date = event_dt.date()
    dim_date = db.query(DimDate).filter(DimDate.date == event_date).first()
    if not dim_date:
        dim_date = DimDate(
            date=event_date,
            day=event_date.day,
            month=event_date.month,
            year=event_date.year,
            quarter=(event_date.month - 1) // 3 + 1,
            day_of_week=event_date.weekday(),
            is_weekend=event_date.weekday() >= 5
        )
        db.add(dim_date)
        db.flush()
        
    # 3. Employee (for assignments)
    dim_emp = None
    if payload.employee_id:
        emp_uuid = payload.employee_id
        dim_emp = db.query(DimEmployee).filter(DimEmployee.employee_id == emp_uuid).first()
        if not dim_emp:
            dim_emp = DimEmployee(
                employee_id=emp_uuid,
                tenant_id=uuid.UUID(event.tenant_id) if isinstance(event.tenant_id, str) else event.tenant_id,
                first_name="Unknown",
                last_name="Unknown",
                status="active"
            )
            db.add(dim_emp)
            db.flush()
            
    # 4. Asset Dimension
    asset_uuid = payload.asset_id
    dim_asset = db.query(DimAsset).filter(DimAsset.asset_id == asset_uuid).first()
    
    if event.event_type in ["it.asset.created", "it.asset.updated"]:
        if not dim_asset:
            dim_asset = DimAsset(
                asset_id=asset_uuid,
                tenant_id=uuid.UUID(event.tenant_id) if isinstance(event.tenant_id, str) else event.tenant_id,
                name=payload.name or "Unknown",
                category=payload.category or "UNKNOWN",
                status=payload.status or "UNKNOWN"
            )
            db.add(dim_asset)
        else:
            if payload.name:
                dim_asset.name = payload.name
            if payload.category:
                dim_asset.category = payload.category
            if payload.status:
                dim_asset.status = payload.status
        db.flush()
        return  # created/updated only affect the dimension for now.
        
    if not dim_asset:
        # Fallback skeleton if assignment event arrives before creation (shouldn't happen)
        dim_asset = DimAsset(
            asset_id=asset_uuid,
            tenant_id=uuid.UUID(event.tenant_id) if isinstance(event.tenant_id, str) else event.tenant_id,
            name="Unknown",
            category="UNKNOWN",
            status="UNKNOWN"
        )
        db.add(dim_asset)
        db.flush()

    # 5. Assignment Facts
    if not payload.assignment_id:
        return # Can't record assignment without assignment ID
        
    assignment_uuid = uuid.UUID(payload.assignment_id) if isinstance(payload.assignment_id, str) else payload.assignment_id
    
    # Check if fact already exists
    fact = db.query(FactAssetAssignment).filter(FactAssetAssignment.assignment_id == assignment_uuid).first()
    
    if event.event_type == "it.asset.assigned":
        if not fact:
            fact = FactAssetAssignment(
                assignment_id=assignment_uuid,
                tenant_key=dim_tenant.id,
                date_key=dim_date.id,
                asset_key=dim_asset.id,
                employee_key=dim_emp.id if dim_emp else 0, # Should have an employee
                source_event_id=uuid.UUID(event.event_id) if isinstance(event.event_id, str) else event.event_id,
                last_event_occurred_at=event_dt,
                assigned_at=event_dt,
                assignment_status="ACTIVE"
            )
            db.add(fact)
        else:
            # Out of order handling
            if event_dt > fact.last_event_occurred_at:
                fact.assigned_at = event_dt
                fact.last_event_occurred_at = event_dt
                fact.source_event_id = uuid.UUID(event.event_id) if isinstance(event.event_id, str) else event.event_id

    elif event.event_type == "it.asset.returned":
        if not fact:
            # Out of order: return arrived before assign.
            # We must reject this and rely on Kafka retries / DLQ to process it later.
            raise ValueError(f"Assignment {assignment_uuid} does not exist. Cannot process return event out of order.")

        else:
            # Normal return
            if event_dt > fact.last_event_occurred_at or fact.assignment_status == "ACTIVE":
                fact.returned_at = event_dt
                fact.assignment_status = "RETURNED"
                fact.last_event_occurred_at = max(fact.last_event_occurred_at, event_dt)
                fact.source_event_id = uuid.UUID(event.event_id) if isinstance(event.event_id, str) else event.event_id
                
                # Calculate duration
                if fact.assigned_at:
                    delta = event_dt - fact.assigned_at
                    fact.assignment_duration_days = max(0, delta.days)

    db.flush()
        
def load_organization_event(db: Session, event: EventEnvelope[OrganizationPayload]):
    """Loads an HR organization event into the Star Schema."""
    
    set_tenant_schema(db, event.tenant_id)
    
    if is_event_processed(db, event.event_id, event.event_type):
        return
        
    payload = event.payload
    
    # Ensure DimTenant
    dim_tenant = db.query(DimTenant).first()
    if not dim_tenant:
        dim_tenant = DimTenant(tenant_id=uuid.uuid4(), company_name=event.tenant_id, status="active")
        db.add(dim_tenant)
        db.flush()

    entity_uuid = uuid.UUID(payload.id)
        
    if payload.entity_type == "department":
        dim_dept = db.query(DimDepartment).filter(DimDepartment.department_id == entity_uuid).first()
        if not dim_dept:
            dim_dept = DimDepartment(
                department_id=entity_uuid,
                tenant_id=dim_tenant.tenant_id,
                name=payload.name,
                status=payload.status
            )
            db.add(dim_dept)
        else:
            dim_dept.name = payload.name
            dim_dept.status = payload.status
            
    elif payload.entity_type == "designation":
        dim_desig = db.query(DimDesignation).filter(DimDesignation.designation_id == entity_uuid).first()
        if not dim_desig:
            dim_desig = DimDesignation(
                designation_id=entity_uuid,
                tenant_id=dim_tenant.tenant_id,
                name=payload.name,
                level=None
            )
            db.add(dim_desig)
        else:
            dim_desig.name = payload.name
            
    db.commit()


def load_workflow_event(db: Session, event: EventEnvelope[WorkflowEventPayload]):
    """Loads workflow events into FactWorkflowExecution and FactWorkflowStep."""
    
    set_tenant_schema(db, event.tenant_id)
    if is_event_processed(db, event.event_id, event.event_type):
        return
        
    payload = event.payload
    
    # 1. Resolve DimTenant
    try:
        tenant_uuid = uuid.UUID(event.tenant_id)
    except ValueError:
        tenant_uuid = uuid.uuid4()
        
    dim_tenant = db.query(DimTenant).filter(DimTenant.tenant_id == tenant_uuid).first()
    if not dim_tenant:
        dim_tenant = DimTenant(tenant_id=tenant_uuid, company_name=event.tenant_id, status="active")
        db.add(dim_tenant)
        db.flush()
        
    # 2. Resolve DimWorkflow
    workflow_uuid = uuid.UUID(payload.workflow_id)
    dim_workflow = db.query(DimWorkflow).filter(DimWorkflow.workflow_id == workflow_uuid).first()
    if not dim_workflow:
        dim_workflow = DimWorkflow(
            workflow_id=workflow_uuid,
            tenant_id=dim_tenant.tenant_id,
            name=payload.workflow_name or "Unknown",
            workflow_type=payload.entity_type
        )
        db.add(dim_workflow)
        db.flush()

    # 3. Resolve DimDate
    event_date = event.occurred_at.date()
    date_id = int(event_date.strftime("%Y%m%d"))
    dim_date = db.query(DimDate).filter(DimDate.id == date_id).first()
    if not dim_date:
        dim_date = DimDate(
            id=date_id,
            date=event_date,
            day=event_date.day,
            month=event_date.month,
            year=event_date.year,
            quarter=(event_date.month - 1) // 3 + 1,
            day_of_week=event_date.weekday(),
            is_weekend=event_date.weekday() >= 5
        )
        db.add(dim_date)
        db.flush()

    execution_uuid = uuid.UUID(payload.execution_id)

    # FactWorkflowExecution
    if event.event_type.startswith("workflow.execution."):
        fact_exec = db.query(FactWorkflowExecution).filter(FactWorkflowExecution.source_event_id == execution_uuid).first()
        if not fact_exec:
            # We use source_event_id as the execution_uuid for uniqueness
            fact_exec = FactWorkflowExecution(
                tenant_key=dim_tenant.id,
                date_key=dim_date.id,
                employee_key=1, # Default placeholder if started_by is missing
                workflow_key=dim_workflow.id,
                source_event_id=execution_uuid,
                execution_status=payload.status,
                created_at=event.occurred_at
            )
            db.add(fact_exec)
        else:
            fact_exec.execution_status = payload.status
            if payload.status in ["completed", "cancelled", "rejected"]:
                duration = int((event.occurred_at.replace(tzinfo=None) - fact_exec.created_at).total_seconds() / 60)
                fact_exec.total_completion_minutes = duration

    # FactWorkflowStep
    if event.event_type.startswith("workflow.step.") and payload.step_id:
        step_uuid = uuid.UUID(payload.step_id)
        
        # Resolve Approver if present
        approver_key = None
        if payload.approver_id:
            try:
                emp_uuid = uuid.UUID(payload.approver_id)
                dim_emp = db.query(DimEmployee).filter(DimEmployee.employee_id == emp_uuid).first()
                if dim_emp:
                    approver_key = dim_emp.id
            except ValueError:
                pass
                
        fact_step = db.query(FactWorkflowStep).filter(
            FactWorkflowStep.execution_id == execution_uuid,
            FactWorkflowStep.workflow_step_id == step_uuid
        ).first()
        
        if not fact_step:
            fact_step = FactWorkflowStep(
                execution_id=execution_uuid,
                workflow_step_id=step_uuid,
                tenant_key=dim_tenant.id,
                date_key=dim_date.id,
                workflow_key=dim_workflow.id,
                approver_key=approver_key,
                source_event_id=uuid.UUID(event.event_id),
                step_order=payload.step_order or 1,
                entity_type=payload.entity_type,
                status=payload.decision or "pending",
                created_at=None,
                decided_at=None,
                decision_duration_seconds=None
            )
            db.add(fact_step)
            
        # Update out-of-order safe fields
        if event.event_type == "workflow.step.created":
            # Using payload.created_at or event.occurred_at
            from datetime import datetime
            
            created_at_dt = event.occurred_at.replace(tzinfo=None)
            if payload.created_at:
                try:
                    created_at_dt = datetime.fromisoformat(payload.created_at).replace(tzinfo=None)
                except:
                    pass
            fact_step.created_at = created_at_dt
            
        elif event.event_type in ["workflow.step.approved", "workflow.step.rejected"]:
            fact_step.status = payload.decision
            
            from datetime import datetime
            decided_at_dt = event.occurred_at.replace(tzinfo=None)
            if payload.decided_at:
                try:
                    decided_at_dt = datetime.fromisoformat(payload.decided_at).replace(tzinfo=None)
                except:
                    pass
            fact_step.decided_at = decided_at_dt
            
        # Calculate duration if both are present
        if fact_step.created_at and fact_step.decided_at:
            dur = (fact_step.decided_at - fact_step.created_at).total_seconds()
            fact_step.decision_duration_seconds = max(0, int(dur))

    db.commit()
