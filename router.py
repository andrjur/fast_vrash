from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
import logging
from repository import TaskRepository
from shemas import STaskAdd, STask, STaskId

router = APIRouter(
    prefix="/tasks",
    tags=["Таски"],
)

logger = logging.getLogger(__name__)


@router.post("/", response_model=STaskId)
async def add_task(
        task: Annotated[STaskAdd, Depends()],
) -> STaskId:
    try:
        task_id = await TaskRepository.add_one(task)
        logger.info("Task added successfully with id: %s", task_id)
        return STaskId(ok=True, task_id=task_id)
    except Exception as e:
        logger.error("Error adding task: %s", e)
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[STask])
async def get_tasks() -> list[STask]:
    try:
        tasks = await TaskRepository.find_all()
        logger.info("Retrieved %d tasks", len(tasks))
        return tasks
    except Exception as e:
        logger.error("Error retrieving tasks: %s", e)
        raise HTTPException(status_code=500, detail="Error retrieving tasks")
