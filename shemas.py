from typing import Optional
from pydantic import BaseModel, Field, model_validator
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
    due_date: Optional[str] = Field(None, description="Срок выполнения")  # Оставляем как строку

    @model_validator(mode='before')
    def validate_name(cls, values):
        name = values.get('name')
        if not name or not name.strip():
            raise ValueError('Название не может быть пустым')
        values['name'] = name.strip()
        return values

    @model_validator(mode='before')
    def parse_due_date(cls, values):
        due_date = values.get('due_date')
        if due_date:
            try:
                # Преобразуем дату из формата dd-mm-yyyy в объект datetime
                values['due_date'] = datetime.strptime(due_date, '%d.%m.%Y')
            except ValueError:
                raise ValueError("Invalid date format. Use dd-mm-yyyy.")
        return values

class STask(STaskAdd):
    id: int

    class Config:
        from_attributes = True

class STaskId(BaseModel):
    ok: bool = True
    task_id: int
