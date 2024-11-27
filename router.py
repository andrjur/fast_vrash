
from fastapi import APIRouter

router = APIRouter(
    prefix="/tasks"
)
@router.post("/")
async def add_task(
        task: Annotated[STaskAdd, Depends()],
):
    tasks.append(task)
    return {"data": task, "ok": True}

# @app.get("/tasks")
# def get_tasks():
#     task = STask(name="Угу")
#     return {"data": task}
