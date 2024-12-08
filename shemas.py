from typing import Optional
from pydantic import BaseModel, Field, validator
from enum import Enum
from datetime import datetime


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class STaskAdd(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, description="Название задачи")
    description: Optional[str] = Field(None, max_length=500, description="Описание задачи")
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    due_date: Optional[datetime] = Field(None, description="Срок выполнения")

    @validator('name')
    def name_must_be_valid(cls, v):
        if not v.strip():
            raise ValueError('Название не может быть пустым')
        return v.strip()


class STask(STaskAdd):
    id: int

    class Config:
        from_attributes = True


class STaskId(BaseModel):
    ok: bool = True
    task_id: int
