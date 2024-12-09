from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, Enum as SQLAlchemyEnum, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from database import new_session, Model
from shemas import TaskStatus
from config import settings
from users import UserOrm


class TaskOrm(Model):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    status: Mapped[TaskStatus] = mapped_column(SQLAlchemyEnum(TaskStatus), default=TaskStatus.PENDING)
    due_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


async def create_tables():
    async with new_session.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def delete_tables():
    async with new_session.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)


async def get_tasks():
    async with new_session() as session:
        query = select(TaskOrm)
        result = await session.execute(query)
        task_models = result.scalars().all()
        return task_models

async def create_user(username: str, password: str):
    async with new_session() as session:
        user = UserOrm(username=username, hashed_password=get_password_hash(password))
        session.add(user)
        await session.commit()