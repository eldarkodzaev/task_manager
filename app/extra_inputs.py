# Модуль, описывающий функции для ввода данных о задаче
# со всеми возможными проверками


from typing import Optional
from datetime import datetime

import colorama
from models import Priority


def input_title(blank: bool = False) -> Optional[str]:
    """Функция для ввода заголовка задачи

    Args:
        blank (bool, optional): если True, то допускается ввод пустой строки. По умолчанию False.

    Returns:
        Optional[str]: заголовок задачи (title) или None
    """
    while True:
        title = input("Введите заголовок задачи: ")
        if title == "":
            if blank:
                return None
            else:
                print(colorama.Back.RED + "Заголовок не может быть пустым")
        else:
            return title
        

def input_category(blank: bool = False) -> Optional[str]:
    """Функция для ввода категории задачи

    Args:
        blank (bool, optional): если True, то допускается ввод пустой строки. По умолчанию False.

    Returns:
        Optional[str]: категорию задачи (category) или None
    """
    while True:
        category = input("Введите категорию задачи: ")
        if category == "":
            if blank:
                return None
            else:
                print(colorama.Back.RED + "Категория не может быть пустой")
        else:
            return category
        

def input_due_date(blank: bool = False) -> Optional[datetime.date]:
    """Функция для ввода срока выполнения задачи

    Args:
        blank (bool, optional): если True, то допускается ввод пустой строки. По умолчанию False.

    Returns:
        Optional[datetime.date]: объект даты (due_date) или None
    """
    while True:
        due_date = input("Введите срок выполнения в формате ГГГГ-ММ-ДД: ")
        try:
            if due_date == "" and blank:
                return None
            date = datetime.strptime(due_date, "%Y-%m-%d").date()
        except ValueError:
            print(colorama.Back.RED + "Неверный формат даты")
        else:
            if date < datetime.today().date():
                print(colorama.Back.RED + "Срок выполнения задачи не может быть в прошлом")
            else:
                return date
            
    
    
def input_priority(blank: bool = False) -> Optional[str]:
    """Функция для ввода приоритета задачи

    Args:
        blank (bool, optional): если True, то допускается ввод пустой строки. По умолчанию False.

    Returns:
        Optional[str]: строка: "1", "2" или "3"
    """
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
            print(colorama.Back.RED + "Неверный ввод")
            
def input_task_id() -> int:
    """Функция для ввода id задачи

    Returns:
        int: id задачи
    """
    while True:
        try:
            return int(input("Введите id задачи: "))
        except (ValueError, TypeError):
            print(colorama.Back.RED + "ID должно быть целым числом")
