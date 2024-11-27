from fastapi import FastAPI

from contextlib import asynccontextmanager

from datab import create_tables, delete_tables

from router import router as tasks_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    print("База")
    await create_tables()
    print("=+++=")
    yield
    print("ooout")


app = FastAPI(lifespan=lifespan)
app.include_router(tasks_router)


