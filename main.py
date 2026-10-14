"""My first FastAPI application — Task Manager API.

Run with:
    uvicorn main:app --reload

Endpoints:
    GET    /              — root
    GET    /health        — health check
    GET    /tasks         — list all tasks
    GET    /tasks/{id}    — get one task
    POST   /tasks         — create a new task
    PUT    /tasks/{id}    — update a task
    DELETE /tasks/{id}    — delete a task
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Task Manager API")


# --- Data model ---

class Task(BaseModel):
    """A task with a title and completion status."""

    title: str
    done: bool = False


class TaskUpdate(BaseModel):
    """Fields allowed when updating a task (all optional)."""

    title: str | None = None
    done: bool | None = None


# --- In-memory storage ---

tasks: list[Task] = []


# --- Endpoints ---

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/tasks")
def list_tasks():
    """List all tasks."""
    return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    """Get one task by ID. Returns 404 if not found."""
    if task_id < 0 or task_id >= len(tasks):
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]


@app.post("/tasks", status_code=201)
def create_task(task: Task):
    """Create a new task."""
    tasks.append(task)
    return {"id": len(tasks) - 1, **task.model_dump()}


@app.put("/tasks/{task_id}")
def update_task(task_id: int, update: TaskUpdate):
    """Update an existing task (partial update)."""
    if task_id < 0 or task_id >= len(tasks):
        raise HTTPException(status_code=404, detail="Task not found")

    current = tasks[task_id]
    if update.title is not None:
        current.title = update.title
    if update.done is not None:
        current.done = update.done

    return {"id": task_id, **current.model_dump()}


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    """Delete a task."""
    if task_id < 0 or task_id >= len(tasks):
        raise HTTPException(status_code=404, detail="Task not found")
    tasks.pop(task_id)
    return None
