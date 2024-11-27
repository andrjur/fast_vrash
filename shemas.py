from typing import Optional
from pydantic import BaseModel, Field


class STaskAdd(BaseModel):
    name: str = Field(..., description="Название задачи")
    description: Optional[str] = Field(None, description="Описание задачи")


class STask(STaskAdd):
    id: int

    class Config:
        from_attributes = True


class STaskId(BaseModel):
    ok: bool = True
    task_id: int
