# Модуль, описывающий модели, с которыми работает менеджер задач


from dataclasses import dataclass
from datetime import date
from enum import StrEnum
from typing import Optional
        

class Priority(StrEnum):
    """Приоритет задачи"""
    
    high = "высокий"
    medium = "средний"
    low = "низкий"


class Status(StrEnum):
    """Статус задачи"""
    
    done = "выполнена"
    not_done = "не выполнена"


@dataclass
class Task:
    """Модель задачи"""
    
    title: str
    description: str
    category: str
    due_date: date
    priority: Priority
    id: Optional[int] = None
    status: Optional[Status] = None
    
    def to_json(self) -> dict:
        return {
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "due_date": str(self.due_date),
            "priority": self.priority,
            "id": self.id,
            "status": self.status
        }
    