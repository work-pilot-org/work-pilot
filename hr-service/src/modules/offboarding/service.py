from uuid import UUID
from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.modules.offboarding.models import OffboardingTask
from src.modules.offboarding.schemas import OffboardingTaskCreate, OffboardingTaskUpdate

class OffboardingService:
    def __init__(self, db: Session):
        self.db = db

    def create_task(self, task: OffboardingTaskCreate) -> OffboardingTask:
        db_task = OffboardingTask(**task.model_dump())
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def get_tasks_by_employee(self, employee_id: UUID) -> List[OffboardingTask]:
        return self.db.query(OffboardingTask).filter(
            OffboardingTask.employee_id == employee_id
        ).all()

    def update_task(self, task_id: UUID, task: OffboardingTaskUpdate) -> OffboardingTask:
        db_task = self.db.query(OffboardingTask).filter(
            OffboardingTask.id == task_id
        ).first()
        if not db_task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

        update_data = task.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_task, key, value)

        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def delete_task(self, task_id: UUID):
        db_task = self.db.query(OffboardingTask).filter(
            OffboardingTask.id == task_id
        ).first()
        if not db_task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        
        self.db.delete(db_task)
        self.db.commit()
