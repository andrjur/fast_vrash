from sqlalchemy import select
import logging
from datab import new_session, TaskOrm
from shemas import STaskAdd, STask

logger = logging.getLogger(__name__)


class TaskRepository:
    @classmethod
    async def add_one(cls, data: STaskAdd) -> int:
        async with new_session() as session:
            task_dict = data.model_dump()

            task = TaskOrm(**task_dict)
            session.add(task)
            await session.flush()
            await session.commit()
            logger.info("Added task with id: %s", task.id)
            return task.id

    @classmethod
    async def find_all(cls) -> list[STask]:
        async with new_session() as session:
            query = select(TaskOrm)
            result = await session.execute(query)
            task_models = result.scalars().all()
            task_shemas = [STask.model_validate(task_model) for task_model in task_models]
            logger.info("Found %d tasks", len(task_models))
            return task_models
