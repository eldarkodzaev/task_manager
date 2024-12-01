from actions import (
    show_tasks, show_tasks_for_category,
    add_task, change_task, mark_task_as_done,
    delete_task_by_id, delete_task_by_category, search_task
)


def print_menu():
    print("\nВыберите действие:")
    print("1) Посмотреть все задачи")
    print("2) Посмотреть задачи определенной категории")
    print("3) Добавить новую задачу")
    print("4) Редактировать задачу")
    print("5) Отметить задачу как выполненную")
    print("6) Удалить задачу по ID")
    print("7) Удалить задачи по категории")
    print("8) Поиск задач")
    print("0) Выход\n")
    
    
menu = {
    "1": show_tasks,
    "2": show_tasks_for_category,
    "3": add_task,
    "4": change_task,
    "5": mark_task_as_done,
    "6": delete_task_by_id,
    "7": delete_task_by_category,
    "8": search_task
}