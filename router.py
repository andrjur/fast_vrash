from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from auth import get_current_user, User
from repository import TaskRepository
from shemas import STaskAdd, STask, STaskId

router = APIRouter(
    prefix="/tasks",
    tags=["Таски"],
)

@router.post("/", response_model=STaskId)
async def add_task(
    task: Annotated[STaskAdd, Depends()],
    current_user: Annotated[User, Depends(get_current_user)]
) -> STaskId:
  #  try:  # отладочный трай чтобы не падало всё а в норм ответе возврящало в сваггер текст ошибки - убрать при релизе
        task_id = await TaskRepository.add_one(task)
        return {"ok": True, "task_id": task_id}
 #   except Exception as e:
  #      raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[STask])
async def get_tasks(
    current_user: Annotated[User, Depends(get_current_user)]
) -> list[STask]:
    tasks = await TaskRepository.find_all()
    return tasks
