from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from database import Model
from typing import Optional
from datetime import datetime

class UserOrm(Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(100))

class TaskOrm(Model):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="pending")  # Добавлено поле status
    #due_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)  # Добавлено поле due_date
