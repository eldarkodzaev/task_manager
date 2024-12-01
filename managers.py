import os
import json
from datetime import datetime

import colorama
from models import Task, Status


class TaskManager:

    def __init__(self, file: str) -> None:
        """
        Args:
            file (str): путь к файлу базы данных
        """
        self.file = file
        if not os.path.isfile(file):
            with open(self.file, "w", encoding="utf-8"):
                print(colorama.Back.YELLOW + f"База данных '{file}' не найдена")
                print(colorama.Back.GREEN + f"Создана новая база данных '{file}'")
        else:
            print(colorama.Back.GREEN + f"Подключено к базе данных '{file}'")

    @property
    def tasks(self) -> list[dict]:
        """Возвращает список задач

        Returns:
            list[dict]: список задач
        """
        with open(self.file, "r", encoding="utf-8") as json_file:
            try:
                return json.load(json_file)
            except json.JSONDecodeError:
                return []

    def get_new_id(self) -> int:
        """Возвращает уникальный id для новой задачи

        Returns:
            int: id
        """
        ids = [task['id'] for task in self.tasks]
        return max(ids, default=0) + 1

    def get_task_from_id(self, task_id: int) -> Task:
        """Возвращает объект Task по ее id

        Args:
            task_id (int): id задачи

        Raises:
            ValueError: если задача не найдена

        Returns:
            Task: объект задачи
        """
        for task in self.tasks:
            if task['id'] == task_id:
                return Task(
                    title=task['title'],
                    description=task['description'],
                    category=task['category'],
                    due_date=datetime.strptime(task['due_date'], "%Y-%m-%d").date(),
                    priority=task['priority'],
                    id=task['id'],
                    status=task['status']
                )
        raise ValueError(f"Задачи с id '{task_id}' не существует")

    def exists(self, task_id: int) -> bool:
        """Определяет, существует ли задача с указанным id

        Args:
            task_id (int): id задачи

        Returns:
            bool: True/False
        """
        return any([task['id'] == task_id for task in self.tasks])

    def add(self, task: Task) -> None:
        """Добавляет задачу в базу данных

        Args:
            task (Task): объект задачи
        """
        tasks = self.tasks
        task_json = task.to_json()
        extra = {
            "id": self.get_new_id(),
            "status": str(Status.not_done)
        }
        tasks.append(task_json | extra)
        self.__rewrite_tasks(new_data=tasks)

    def change(self, task_id: int, **kwargs) -> None:
        """Редактирует задачу

        Args:
            task_id (int): id задачи
        """
        
        task: Task = self.get_task_from_id(task_id)
        
        if (title := kwargs.get('title')):
            task.title = title
            
        if (description := kwargs.get('description')):
            task.description = description
        
        if (category := kwargs.get('category')):
            task.category = category
        
        if (due_date := kwargs.get('due_date')):
            task.due_date = due_date
            
        if (priority := kwargs.get('priority')):
            task.priority = priority
            
        if (status := kwargs.get('status')):
            task.status = status

        tasks = []
        for item in self.tasks:
            if item['id'] == task_id:
                tasks.append(task.to_json())
            else:
                tasks.append(item)

        self.__rewrite_tasks(new_data=tasks)

    def delete_by_id(self, task_id: int) -> None:
        """Удаляет задачу по ее id

        Args:
            task_id (int): id задачи

        Raises:
            ValueError: если task_id не существует
        """
        if not self.exists(task_id):
            raise ValueError(f"Задачи с id '{task_id}' не существует")

        tasks = []
        for task in self.tasks:
            if task['id'] != task_id:
                tasks.append(task)
        self.__rewrite_tasks(new_data=tasks)

    def delete_by_category(self, category: str) -> int:
        """Удаляет задачи заданной категории

        Args:
            category (str): категория задач

        Returns:
            int: количество удаленных задач
        """
        number_of_deleted_tasks = 0
        tasks = []
        for task in self.tasks:
            if task['category'] != category:
                tasks.append(task)
            else:
                number_of_deleted_tasks += 1
        self.__rewrite_tasks(new_data=tasks)
        return number_of_deleted_tasks

    def search(self, query: str) -> list[dict]:
        """Поиск по ключевым словам, категории или статусу выполнения

        Returns:
            list[dict]: список задач
        """
        query = query.lower()
        tasks = []
        for task in self.tasks:
            if (query in task['title'].lower().split() 
                or query == task['category'].lower()
                or query == task['status']):
                    tasks.append(task)
        return tasks

    def __rewrite_tasks(self, new_data: list[dict]) -> None:
        """Перезаписывает файл базы данных с новыми данными

        Args:
            new_data (list[dict]): новые данные
        """
        with open(self.file, "w", encoding="utf-8") as json_file:
            json.dump(new_data, json_file, ensure_ascii=False, indent=4)
