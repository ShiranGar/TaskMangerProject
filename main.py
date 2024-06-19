from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List,Literal
import uuid
from models import Task, TaskManager  # Import the Task and TaskManager models
from firebase_config import db  # Import Firebase configuration

app = FastAPI()

templates = Jinja2Templates(directory="templates")

task_manager = TaskManager()

@app.post("/tasks/", response_model=Task)
async def create_task(task: Task):
    task.id = str(uuid.uuid4())
    task_manager.tasks.append(task)
    db.collection("tasks").document(task.id).set(task.dict())
    return task

@app.get("/tasks/", response_model=List[Task])
async def read_tasks():
    tasks = [task.to_dict() for task in db.collection("tasks").stream()]
    return tasks

@app.get("/tasks/{task_id}", response_model=Task)
async def read_task(task_id: str):
    task_ref = db.collection("tasks").document(task_id)
    task = task_ref.get()
    if task.exists:
        return task.to_dict()
    else:
        raise HTTPException(status_code=404, detail="Task not found")

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: str, task: Task):
    task_ref = db.collection("tasks").document(task_id)
    task_ref.update(task.dict(exclude_unset=True))
    updated_task = task_ref.get()
    return updated_task.to_dict()

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    task_ref = db.collection("tasks").document(task_id)
    task_ref.delete()
    return {"message": "Task deleted successfully"}

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    tasks = [task.to_dict() for task in db.collection("tasks").stream()]
    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks})

@app.get("/tasks/priority/{priority}", response_model=List[Task])
async def read_tasks_by_priority(priority: Literal["low", "medium", "high"]):
    tasks = [task.to_dict() for task in db.collection("tasks").where("priority", "==", priority).stream()]
    return tasks

# Run the app with: uvicorn main:app --reload
