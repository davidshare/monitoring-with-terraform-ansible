import pytest
from datetime import datetime, timedelta
from app.crud import task as task_crud
from app.schemas.task import TaskCreate, TaskUpdate
from app.models.task import TaskStatus, TaskPriority


def test_create_task(db):
    task = TaskCreate(
        title="Test Task",
        description="This is a test task",
        status=TaskStatus.pending,
        priority=TaskPriority.medium,
        category="Test",
        due_date=datetime.utcnow() + timedelta(days=1)
    )
    db_task = task_crud.create_task(db, task)
    assert db_task.title == "Test Task"
    assert db_task.description == "This is a test task"
    assert db_task.status == TaskStatus.pending
    assert db_task.priority == TaskPriority.medium
    assert db_task.category == "Test"
    assert db_task.due_date is not None


def test_get_task(db):
    task = TaskCreate(title="Get Task Test")
    db_task = task_crud.create_task(db, task)
    retrieved_task = task_crud.get_task(db, db_task.id)
    assert retrieved_task.id == db_task.id
    assert retrieved_task.title == "Get Task Test"


def test_get_tasks(db):
    task1 = TaskCreate(title="Task 1")
    task2 = TaskCreate(title="Task 2")
    task_crud.create_task(db, task1)
    task_crud.create_task(db, task2)
    tasks = task_crud.get_tasks(db)
    assert len(tasks) == 2
    assert tasks[0].title == "Task 1"
    assert tasks[1].title == "Task 2"


def test_update_task(db):
    task = TaskCreate(title="Update Task Test")
    db_task = task_crud.create_task(db, task)
    update_data = TaskUpdate(title="Updated Task", status=TaskStatus.completed)
    updated_task = task_crud.update_task(db, db_task.id, update_data)
    assert updated_task.title == "Updated Task"
    assert updated_task.status == TaskStatus.completed


def test_delete_task(db):
    task = TaskCreate(title="Delete Task Test")
    db_task = task_crud.create_task(db, task)
    deleted_task = task_crud.delete_task(db, db_task.id)
    assert deleted_task.id == db_task.id
    assert task_crud.get_task(db, db_task.id) is None
