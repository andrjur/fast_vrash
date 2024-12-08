from fastapi import FastAPI
from contextlib import asynccontextmanager
from logger import setup_logger
from config import settings
from datab import create_tables, delete_tables
from router import router

logger = setup_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    await create_tables()
    logger.info("Application startup completed")
    yield
    logger.info("Application shutdown completed")

app = FastAPI(
    title="Task Management API",
    description="API для управления задачами",
    version="1.0.0",
    lifespan=lifespan,
    debug=settings.DEBUG
)

app.include_router(router)
