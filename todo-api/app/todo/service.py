from sqlalchemy.orm import Session
from .models import TodoItem
from .schemas import TodoCreate, TodoUpdate
from .models import PriorityEnum  # Import your enum if necessary


class TodoService:
    @staticmethod
    def create(db: Session, todo: TodoCreate, user_id: int) -> TodoItem:
        """Create a new todo for the given user."""
        # Ensure that the 'priority' field is correctly passed as an Enum
        priority = PriorityEnum(todo.priority) if isinstance(
            todo.priority, str) else todo.priority

        # Handle empty tag list
        tags_string = ', '.join(todo.tags) if todo.tags else ''

        new_todo = TodoItem(
            title=todo.title,
            description=todo.description,
            start_date=todo.start_date,
            due_date=todo.due_date,
            priority=priority,  # Use the correct enum here
            status=todo.status,
            tags=tags_string,
            category=todo.category,
            user_id=user_id
        )

        db.add(new_todo)
        db.commit()
        db.refresh(new_todo)
        new_todo.tags = new_todo.tags.split(', ') if new_todo.tags else []
        return new_todo

    @staticmethod
    def get_all_todos(db: Session, user_id: int) -> list[TodoItem]:
        """Retrieve all todos for the given user."""
        todos = db.query(TodoItem).filter(
            TodoItem.user_id == user_id
        ).all()

        for todo in todos:
            todo.tags = todo.tags.split(', ') if todo.tags else []

        return todos

    @staticmethod
    def get_todo_by_id(db: Session, todo_id: int, user_id: int) -> TodoItem:
        """Retrieve a todo by ID for the given user."""
        return db.query(TodoItem).filter(
            TodoItem.id == todo_id, TodoItem.user_id == user_id
        ).first()

    @staticmethod
    def update(db: Session, todo_id: int, todo: TodoUpdate, user_id: int) -> TodoItem:
        """Update a todo for the given user."""
        existing_todo = db.query(TodoItem).filter(
            TodoItem.id == todo_id, TodoItem.user_id == user_id
        ).first()
        if not existing_todo:
            return None

        # Ensure that 'priority' is updated as an Enum, if provided
        if todo.priority:
            priority = PriorityEnum(todo.priority) if isinstance(
                todo.priority, str) else todo.priority
            setattr(existing_todo, 'priority', priority)

        # Update other fields
        for key, value in todo.dict(exclude_unset=True).items():
            if key != 'priority':  # Avoid re-setting priority twice
                setattr(existing_todo, key, value)

        db.commit()
        db.refresh(existing_todo)
        return existing_todo

    @staticmethod
    def delete(db: Session, todo_id: int, user_id: int) -> bool:
        """Delete a todo for the given user."""
        existing_todo = db.query(TodoItem).filter(
            TodoItem.id == todo_id, TodoItem.user_id == user_id
        ).first()
        if not existing_todo:
            return False
        db.delete(existing_todo)
        db.commit()
        return True
