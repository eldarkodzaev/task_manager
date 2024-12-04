import pytest
import json
from datetime import date
from managers import TaskManager
from models import Task, Priority, Status


@pytest.fixture
def reset_test_data():
    """Фикстура восстанавливает базу данных перед запуском теста"""
    
    with open("test_data.json", "r", encoding="utf-8") as test_data:
        data = json.load(test_data)
        
    with open("test_tasks.json", "w", encoding="utf-8") as test_tasks:
        json.dump(data, test_tasks, ensure_ascii=False, indent=4)


@pytest.mark.usefixtures("reset_test_data")
class TestTaskManager:

    def test_get_new_id(self):
        """Проверяет функцию генерации нового id"""
        
        manager = TaskManager(file="test_tasks.json")
        assert 4 == manager.get_new_id()
        
        manager = TaskManager(file="test_tasks_EMPTY.json")
        assert 1 == manager.get_new_id()
        

    def test_add(self):
        """Проверяет добавление новой задачи"""
        
        manager = TaskManager(file="test_tasks.json")
        task = Task(
            title="new title",
            description="new description",
            category="new category",
            due_date=date(2124, 1, 1),
            priority=Priority.high,
            id=4,
            status=Status.not_done
        )
        manager.add_task(task)
        
        with open("test_data.json", "r", encoding="utf-8") as json_file:
            expected_json = json.load(json_file)
        
        expected_json = [
            {"id": 1, "status": "выполнена", "title": "Task 1", "description": "Description for Task 1", "category": "Work", "due_date": "2023-11-01", "priority": "высокий"},
            {"id": 2, "status": "не выполнена", "title": "Task 2", "description": "Description for Task 2", "category": "Personal", "due_date": "2023-11-05", "priority": "средний"},
            {"id": 3, "status": "выполнена", "title": "Task 3", "description": "Description for Task 3", "category": "Work", "due_date": "2023-11-08", "priority": "низкий"},
            {"id": 4, "status": "не выполнена", "title": "new title", "description": "new description", "category": "new category", "due_date": "2124-01-01", "priority": "высокий"}
        ]
        
        with open("test_tasks.json", "r", encoding="utf-8") as json_file:
            tasks = json.load(json_file)
        
        assert expected_json == tasks
        

    def test_change_if_task_not_exists(self):
        """Случай, когда пользователь пытается редактировать задачу,
        которой нет в базе данных"""
        
        manager = TaskManager(file="test_tasks.json")
        with pytest.raises(ValueError):
            manager.change_task(task_id=123)  # нет задачи с id 123
            

    def test_change_task_fully(self):
        """Случай, когда редактирутся все поля задачи"""
        
        manager = TaskManager(file="test_tasks.json")
        manager.change_task(
            task_id=1, 
            title="New title", 
            description="New description", 
            category="New category",
            due_date=date(2124, 11, 11),
            priority=Priority.low
        )
        
        expected_json = [
            {"id": 1, "status": "выполнена", "title": "New title", "description": "New description", "category": "New category", "due_date": "2124-11-11", "priority": "низкий"},
            {"id": 2, "status": "не выполнена", "title": "Task 2", "description": "Description for Task 2", "category": "Personal", "due_date": "2023-11-05", "priority": "средний"},
            {"id": 3, "status": "выполнена", "title": "Task 3", "description": "Description for Task 3", "category": "Work", "due_date": "2023-11-08", "priority": "низкий"}
        ]
        with open("test_tasks.json", "r", encoding="utf-8") as json_file:
            tasks = json.load(json_file)
            
        assert expected_json == tasks
        
        
    def test_change_task_partial(self):
        """Случай, когда редактируются не все поля задачи"""
        
        manager = TaskManager(file="test_tasks.json")
        manager.change_task(
            task_id=1,
            title="New title",
            category="",  # Пустые строки означают, что это поле не будет изменено.
            due_date=""   # Если поле вообще не указано, оно также не будет изменено.
        )
        
        expected_json = [
            {"id": 1, "status": "выполнена", "title": "New title", "description": "Description for Task 1", "category": "Work", "due_date": "2023-11-01", "priority": "высокий"},
            {"id": 2, "status": "не выполнена", "title": "Task 2", "description": "Description for Task 2", "category": "Personal", "due_date": "2023-11-05", "priority": "средний"},
            {"id": 3, "status": "выполнена", "title": "Task 3", "description": "Description for Task 3", "category": "Work", "due_date": "2023-11-08", "priority": "низкий"}
        ]
        with open("test_tasks.json", "r", encoding="utf-8") as json_file:
            tasks = json.load(json_file)
            
        assert expected_json == tasks
        
        
    def test_mark_as_done(self):
        """Изменение статуса задачи на 'выполнена'"""
        manager = TaskManager(file="test_tasks.json")
        manager.change_task(
            task_id=2,
            status=Status.done
        )
        
        expected_json = [
            {"id": 1, "status": "выполнена", "title": "Task 1", "description": "Description for Task 1", "category": "Work", "due_date": "2023-11-01", "priority": "высокий"},
            {"id": 2, "status": "выполнена", "title": "Task 2", "description": "Description for Task 2", "category": "Personal", "due_date": "2023-11-05", "priority": "средний"},
            {"id": 3, "status": "выполнена", "title": "Task 3", "description": "Description for Task 3", "category": "Work", "due_date": "2023-11-08", "priority": "низкий"}
        ]
        with open("test_tasks.json", "r", encoding="utf-8") as json_file:
            tasks = json.load(json_file)
            
        assert expected_json == tasks
        

    def test_delete_by_id(self):
        """Удаление задачи по id"""
        manager = TaskManager(file="test_tasks.json")
        manager.delete_task_by_id(task_id=1)
        expected_json = [
            {"id": 2, "status": "не выполнена", "title": "Task 2", "description": "Description for Task 2", "category": "Personal", "due_date": "2023-11-05", "priority": "средний"},
            {"id": 3, "status": "выполнена", "title": "Task 3", "description": "Description for Task 3", "category": "Work", "due_date": "2023-11-08", "priority": "низкий"}
        ]
        with open("test_tasks.json", "r", encoding="utf-8") as json_file:
            tasks = json.load(json_file)
            
        assert expected_json == tasks


    def test_delete_by_category(self):
        """Удаление задач по категории"""
        manager = TaskManager(file="test_tasks.json")
        number_of_deleted_tasks = manager.delete_task_by_category(category="Work")
        expected_json = [
            {"id": 2, "status": "не выполнена", "title": "Task 2", "description": "Description for Task 2", "category": "Personal", "due_date": "2023-11-05", "priority": "средний"}
        ]
        with open("test_tasks.json", "r", encoding="utf-8") as json_file:
            tasks = json.load(json_file)
            
        assert expected_json == tasks
        assert 2 == number_of_deleted_tasks
