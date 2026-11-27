from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from shared_infrastructure.core.dependencies import require_permissions
from shared_infrastructure.core.rbac import Permission
from shared_infrastructure.database.session import get_db
from src.modules.onboarding.schemas import OnboardingTaskCreate, OnboardingTaskUpdate, OnboardingTaskResponse
from src.modules.onboarding.service import OnboardingService

router = APIRouter(
    prefix="/onboarding",
    tags=["Onboarding"],
    dependencies=[Depends(require_permissions([Permission.HR_MANAGE]))]
)

@router.post("/tasks", response_model=OnboardingTaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task: OnboardingTaskCreate,
    db: Session = Depends(get_db)
):
    service = OnboardingService(db)
    return service.create_task(task)

@router.get("/tasks/{employee_id}", response_model=List[OnboardingTaskResponse])
def get_employee_tasks(
    employee_id: UUID,
    db: Session = Depends(get_db)
):
    service = OnboardingService(db)
    return service.get_tasks_by_employee(employee_id)

@router.patch("/tasks/{task_id}", response_model=OnboardingTaskResponse)
def update_task(
    task_id: UUID,
    task: OnboardingTaskUpdate,
    db: Session = Depends(get_db)
):
    service = OnboardingService(db)
    return service.update_task(task_id, task)

@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: UUID,
    db: Session = Depends(get_db)
):
    service = OnboardingService(db)
    service.delete_task(task_id)
