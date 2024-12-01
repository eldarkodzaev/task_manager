from typing import Optional
from datetime import datetime

import colorama
from models import Priority


def input_due_date(blank: bool = False) -> Optional[datetime.date]:
    while True:
        due_date = input("Введите срок выполнения в формате ГГГГ-ММ-ДД: ")
        try:
            if due_date == "" and blank:
                return None
            date = datetime.strptime(due_date, "%Y-%m-%d").date()
        except ValueError:
            print(colorama.Fore.RED + "Неверный формат даты")
        else:
            if date < datetime.today().date():
                print(colorama.Fore.RED + "Срок выполнения задачи не может быть в прошлом")
            else:
                return date
            
    
    
def input_priority(blank: bool = False) -> str | None:
    priorities = {
        "1": Priority.high,
        "2": Priority.medium,
        "3": Priority.low
    }
    
    while True:
        print("Введите приоритет:")
        print("1 - высокий, 2 - средний, 3 - низкий:", end=" ")
        
        priority = input()
        if priority == "" and blank:
            return None
        if priority in priorities.keys():
            return priorities[priority]
        else:
            print(colorama.Fore.RED + "Неверный ввод")
            
def input_task_id() -> int:
    while True:
        try:
            return int(input("Введите id задачи: "))
        except (ValueError, TypeError):
            print(colorama.Fore.RED + "ID должно быть целым числом")
