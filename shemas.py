from typing import Optional
from pydantic import BaseModel, Field, model_validator
from enum import Enum
from datetime import datetime

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

def parse_date(date_str: str) -> datetime:
    # Список форматов для попытки парсинга
    date_formats = ["%d.%m.%Y", "%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"]
    strip_str = date_str.strip()
    for fmt in date_formats:
        try:
            return datetime.strptime(strip_str, fmt)
        except ValueError:
            continue
    raise ValueError("Invalid date format. Use DD.MM.YYYY or other supported formats.")

class STaskAdd(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, description="Название задачи")
    description: Optional[str] = Field(None, max_length=500, description="Описание задачи")
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    due_date: Optional[datetime] = Field(None, description="Срок выполнения")

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
        if isinstance(due_date, str):  # Проверяем, является ли due_date строкой
            values['due_date'] = parse_date(due_date)  # Используем функцию для парсинга
        return values

class STask(STaskAdd):
    id: int

    class Config:
        from_attributes = True

class STaskId(BaseModel):
    ok: bool = True
    task_id: int
