from uuid import UUID
from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.modules.onboarding.models import OnboardingTask
from src.modules.onboarding.schemas import OnboardingTaskCreate, OnboardingTaskUpdate

class OnboardingService:
    def __init__(self, db: Session):
        self.db = db

    def create_task(self, task: OnboardingTaskCreate) -> OnboardingTask:
        db_task = OnboardingTask(**task.model_dump())
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def get_tasks_by_employee(self, employee_id: UUID) -> List[OnboardingTask]:
        return self.db.query(OnboardingTask).filter(
            OnboardingTask.employee_id == employee_id
        ).all()

    def update_task(self, task_id: UUID, task: OnboardingTaskUpdate) -> OnboardingTask:
        db_task = self.db.query(OnboardingTask).filter(
            OnboardingTask.id == task_id
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
        db_task = self.db.query(OnboardingTask).filter(
            OnboardingTask.id == task_id
        ).first()
        if not db_task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        
        self.db.delete(db_task)
        self.db.commit()
