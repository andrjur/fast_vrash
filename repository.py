from sqlalchemy import select
import logging
from datab import new_session, TaskOrm
from shemas import STaskAdd, STask
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)


class TaskNotFoundError(Exception):
    pass

class RepositoryError(Exception):
    pass

class TaskRepository:
    @classmethod
    async def add_one(cls, data: STaskAdd) -> int:
        async with new_session() as session:
            try:
                task_dict = data.model_dump()
                task = TaskOrm(**task_dict)
                session.add(task)
                await session.commit()
                logger.info("Added task with id: %s", task.id)
                return task.id
            except SQLAlchemyError as e:
                await session.rollback()
                logger.error("Error adding task: %s", str(e))
                raise

    @classmethod
    async def find_all(cls, skip: int = 0, limit: int = 10) -> list[STask]:
        async with new_session() as session:
            try:
                query = select(TaskOrm).offset(skip).limit(limit)
                result = await session.execute(query)
                task_models = result.scalars().all()
                return [STask.model_validate(task) for task in task_models]
            except SQLAlchemyError as e:
                logger.error("Database error: %s", str(e))
                raise
