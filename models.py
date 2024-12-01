from dataclasses import dataclass
from datetime import date
from enum import StrEnum
        

class Priority(StrEnum):
    high = "высокий"
    medium = "средний"
    low = "низкий"


class Status(StrEnum):
    done = "выполнена"
    not_done = "не выполнена"


@dataclass
class Task:
    title: str
    description: str
    category: str
    due_date: date
    priority: Priority
    id: int | None = None
    status: Status | None = None
    
    def to_json(self):
        return {
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "due_date": str(self.due_date),
            "priority": self.priority,
            "id": self.id,
            "status": self.status
        }
    