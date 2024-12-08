import pytest
from httpx import AsyncClient
from main import app
from datab import create_tables, delete_tables

@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        await delete_tables()
        await create_tables()
        yield client

@pytest.mark.asyncio
async def test_create_task(async_client):
    response = await async_client.post(
        "/tasks/",
        json={
            "name": "Test Task",
            "description": "Test Description",
            "status": "pending"
        }
    )
    assert response.status_code == 200
    assert response.json()["ok"] is True
    assert "task_id" in response.json()

@pytest.mark.asyncio
async def test_get_tasks(async_client):
    response = await async_client.get("/tasks/")
    assert response.status_code == 200
    assert isinstance(response.json(), list) 