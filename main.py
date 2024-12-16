import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from contextlib import asynccontextmanager

from starlette.responses import HTMLResponse

from logger import setup_logger
from config import settings
from datab import create_tables, delete_tables, create_user
from router import router
from auth import Token, authenticate_user, create_access_token
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm

logger = setup_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    await create_tables()
    await create_user("root", "root")
    await create_user("An", "123")
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

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>FastAPI Documentation</title>
        </head>
        <body>
            <h1>Welcome to FastAPI</h1>
            <p>Navigate to <a href="/docs">/docs</a> for API documentation.</p>
        </body>
    </html>
    """

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)