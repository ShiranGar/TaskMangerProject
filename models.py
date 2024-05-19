from pydantic import BaseModel
from typing import Optional
import uuid

class Task(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: str # New field for priority
    label: str  # New field for label

class TaskManager(BaseModel):
    tasks: list[Task] = []

