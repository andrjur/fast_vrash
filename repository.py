from sqlalchemy import select
import logging
from database import new_session
from models import TaskOrm
from shemas import STaskAdd, STask
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)


class TaskNotFoundError(Exception):
    pass

class RepositoryError(Exception):
    pass

class TaskRepository:
    @classmethod
    async def add_one(cls, task: STaskAdd) -> int:
        async with new_session() as session:
            task_dict = task.model_dump()
            task = TaskOrm(**task_dict)
            session.add(task)
            await session.commit()
            return task.id

    @classmethod
    async def find_all(cls) -> list[TaskOrm]:
        async with new_session() as session:
            query = select(TaskOrm)
            result = await session.execute(query)
            task_models = result.scalars().all()
            return task_models
