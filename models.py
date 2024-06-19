from pydantic import BaseModel
from typing import Optional,Literal
import uuid

class Task(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: Literal["low", "medium", "high"]
    label: str  # New field for label

class TaskManager(BaseModel):
    tasks: list[Task] = []

