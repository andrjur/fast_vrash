from fastapi import FastAPI
import logging
from contextlib import asynccontextmanager

from starlette.responses import HTMLResponse

from datab import create_tables, delete_tables
from router import router as tasks_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    logger.info("Deleted tables")
    await create_tables()
    logger.info("Created tables")
    yield
    logger.info("Application shutdown")


app = FastAPI(
    title="Task Management API",
    description="API для управления задачами",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/", response_class=HTMLResponse)
async def root():
    html_content = """
    <html>
        <body>
            <p>Welcome to the Task Management API</p>
            <p>Go to <a href="http://127.0.0.1:8000/docs">API documentation</a></p>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

app.include_router(tasks_router)
