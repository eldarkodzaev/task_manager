import colorama

from extra_inputs import input_due_date, input_priority, input_task_id
from managers import TaskManager
from models import Task, Status
from table import fill_table


def show_tasks(manager: TaskManager) -> None:
    """Выводит на экран таблицу всех задач

    Args:
        manager (TaskManager): объект менеджера задач
    """
    data = [
        [task['id'], task['status'], task['title'], task['description'],
        task['category'], task['due_date'], task['priority']]
        for task in manager.tasks
    ]
    table = fill_table(data)
    print(table)


def show_tasks_for_category(manager: TaskManager) -> None:
    """Выводит на экран таблицу всех задач определенной категории

    Args:
        manager (TaskManager): объект менеджера задач
    """
    category = input("Введите категорию: ").lower()
    data = [
        [task['id'], task['status'], task['title'], task['description'],
        task['category'], task['due_date'], task['priority']]
        for task in manager.tasks
        if task['category'].lower() == category
    ]
    table = fill_table(data)
    print(table)


def add_task(manager: TaskManager) -> None:
    """Добавление задачи в базу данных

    Args:
        manager (TaskManager): объект менеджера задач
    """
    print("Новая задача:")
    title = input("Заголовок: ")
    description = input("Описание: ")
    category = input("Категория: ")
    due_date = input_due_date()
    priority = input_priority()
    
    new_task = Task(title, description, category, due_date, priority)
    manager.add(new_task)
    print(colorama.Back.GREEN + "Задача добавлена")


def change_task(manager: TaskManager) -> None:
    """Редактирование задачи

    Args:
        manager (TaskManager): объект менеджера задач
    """
    task_id = input_task_id()
    if not manager.exists(task_id):
        print(colorama.Back.RED + f"Задачи с id '{task_id}' не существует")
        return
    
    print(colorama.Back.BLUE + "Введите новые данные (Enter, чтобы оставить поле без изменений):")
    title = input("Заголовок: ")
    description = input("Описание: ")
    category = input("Категория: ")
    due_date = input_due_date(blank=True)
    priority = input_priority(blank=True)
    
    new_data = {
        'title': title,
        'description': description,
        'category': category,
        'due_date': due_date,
        'priority': priority
    }

    manager.change(task_id, **new_data)
    print(colorama.Back.GREEN + "Задача изменена")
    

def mark_task_as_done(manager: TaskManager) -> None:
    """Отмечает задачу как выполненную

    Args:
        manager (TaskManager): объект менеджера задач
    """
    task_id = input_task_id()
    try:
        manager.change(task_id, status=Status.done)
        print(colorama.Back.GREEN + "Задача помечена как выполненная")
    except ValueError as e:
        print(colorama.Back.RED + str(e))


def delete_task_by_id(manager: TaskManager) -> None:
    """Удаляет задачу по ее ID

    Args:
        manager (TaskManager): объект менеджера задач
    """
    task_id = input_task_id()
    try:
        manager.delete_by_id(task_id)
        print(colorama.Back.GREEN + "Задача удалена.")
    except ValueError as e:
        print(colorama.Back.RED + str(e))
        

def delete_task_by_category(manager: TaskManager) -> None:
    """Удаляет задачи по категории

    Args:
        manager (TaskManager): объект менеджера задач
    """
    category = input("Введите категорию задач, которые хотите удалить: ")
    number_of_deleted_tasks = manager.delete_by_category(category)
    print(colorama.Back.GREEN + f"Количество удаленных задач: {number_of_deleted_tasks}")


def search_task(manager: TaskManager) -> None:
    """Поиск задач

    Args:
        manager (TaskManager): объект менеджера задач
    """
    query = input("Введите запрос: ")
    data = [
        [task['id'], task['status'], task['title'], task['description'],
        task['category'], task['due_date'], task['priority']]
        for task in manager.search(query)
    ]
    table = fill_table(data)
    print(table)
