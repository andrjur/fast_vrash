from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
import logging
from repository import TaskRepository
from shemas import STaskAdd, STask, STaskId
from auth import get_current_user, User

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)

logger = logging.getLogger(__name__)

@router.post("/", response_model=STaskId)
async def add_task(
    task: STaskAdd,
    current_user: Annotated[User, Depends(get_current_user)]
):
    try:
        task_id = await TaskRepository.add_one(task)
        return STaskId(ok=True, task_id=task_id)
    except Exception as e:
        logger.error("Error adding task: %s", e)
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[STask])
async def get_tasks(
    skip: int = 0,
    limit: int = 10,
    current_user: Annotated[User, Depends(get_current_user)]
):
    try:
        return await TaskRepository.find_all(skip=skip, limit=limit)
    except Exception as e:
        logger.error("Error retrieving tasks: %s", e)
        raise HTTPException(status_code=500, detail="Error retrieving tasks")
