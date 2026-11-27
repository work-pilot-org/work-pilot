from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from shared_infrastructure.core.dependencies import require_permissions
from shared_infrastructure.core.rbac import Permission
from shared_infrastructure.database.session import get_db
from src.modules.offboarding.schemas import OffboardingTaskCreate, OffboardingTaskUpdate, OffboardingTaskResponse
from src.modules.offboarding.service import OffboardingService

router = APIRouter(
    prefix="/offboarding",
    tags=["Offboarding"],
    dependencies=[Depends(require_permissions([Permission.HR_MANAGE]))]
)

@router.post("/tasks", response_model=OffboardingTaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task: OffboardingTaskCreate,
    db: Session = Depends(get_db)
):
    service = OffboardingService(db)
    return service.create_task(task)

@router.get("/tasks/{employee_id}", response_model=List[OffboardingTaskResponse])
def get_employee_tasks(
    employee_id: UUID,
    db: Session = Depends(get_db)
):
    service = OffboardingService(db)
    return service.get_tasks_by_employee(employee_id)

@router.patch("/tasks/{task_id}", response_model=OffboardingTaskResponse)
def update_task(
    task_id: UUID,
    task: OffboardingTaskUpdate,
    db: Session = Depends(get_db)
):
    service = OffboardingService(db)
    return service.update_task(task_id, task)

@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: UUID,
    db: Session = Depends(get_db)
):
    service = OffboardingService(db)
    service.delete_task(task_id)
