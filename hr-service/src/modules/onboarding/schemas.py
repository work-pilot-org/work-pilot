from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional

class OnboardingTaskBase(BaseModel):
    task_name: str
    description: Optional[str] = None
    is_completed: bool = False

class OnboardingTaskCreate(OnboardingTaskBase):
    employee_id: UUID

class OnboardingTaskUpdate(BaseModel):
    task_name: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None

class OnboardingTaskResponse(OnboardingTaskBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    employee_id: UUID
    created_at: datetime
    updated_at: datetime
