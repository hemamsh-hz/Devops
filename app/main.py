"""A small in-memory task management REST API for the DevOps assignment."""
from typing import List

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="Task Management API",
    description="A small REST API used to demonstrate a Git-to-Kubernetes DevOps pipeline.",
    version="1.0.0",
)


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=120, examples=["Finish DevOps assignment"])
    completed: bool = False


class Task(TaskCreate):
    id: int


_tasks: List[Task] = []
_next_id = 1


@app.get("/", tags=["info"])
def root() -> dict:
    return {"service": "task-api", "message": "Task Management API is running", "docs": "/docs"}


@app.get("/health", tags=["health"])
def health() -> dict:
    """Kubernetes liveness/readiness endpoint."""
    return {"status": "ok"}


@app.get("/todos", response_model=List[Task], tags=["tasks"])
def list_tasks() -> List[Task]:
    return _tasks


@app.post("/todos", response_model=Task, status_code=status.HTTP_201_CREATED, tags=["tasks"])
def create_task(payload: TaskCreate) -> Task:
    global _next_id
    normalized_title = payload.title.strip()
    if not normalized_title:
        raise HTTPException(status_code=422, detail="title must not be blank")
    item = Task(id=_next_id, title=normalized_title, completed=payload.completed)
    _tasks.append(item)
    _next_id += 1
    return item


@app.get("/todos/{task_id}", response_model=Task, tags=["tasks"])
def get_task(task_id: int) -> Task:
    for item in _tasks:
        if item.id == task_id:
            return item
    raise HTTPException(status_code=404, detail="Task not found")
