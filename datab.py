from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, Enum as SQLAlchemyEnum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from shemas import TaskStatus
from config import settings

engine = create_async_engine(settings.DATABASE_URL)
new_session = async_sessionmaker(engine, expire_on_commit=False)


class Model(DeclarativeBase):
    pass


class TaskOrm(Model):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    status: Mapped[TaskStatus] = mapped_column(SQLAlchemyEnum(TaskStatus), default=TaskStatus.PENDING)
    due_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class UserOrm(Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(100))


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)


async def get_tasks():
    async with new_session() as session:
        query = select(TaskOrm)
        result = await session.execute(query)
        task_models = result.scalars().all()
        return task_models
