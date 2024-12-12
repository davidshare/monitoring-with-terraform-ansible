from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from .models import TodoItem
from .schemas import TodoCreate, TodoUpdate
from .service import TodoService
from app.auth.models import User  # Import the User model


class TodoController:

    @staticmethod
    def create(db: Session, todo: TodoCreate, current_user: User) -> TodoItem:
        """Create a new todo for the current user."""
        try:
            new_todo = TodoService.create(
                db=db, todo=todo, user_id=current_user.id
            )
            return new_todo
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_all_todos(db: Session, current_user: User) -> list[TodoItem]:
        """Retrieve a todo for the current user."""
        try:
            todos = TodoService.get_all_todos(
                db=db, user_id=current_user.id
            )
            if not todos:
                return {
                    "message": "No todos have been created",
                    "data": []
                }

            return todos
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get(db: Session, todo_id: int, current_user: User) -> TodoItem:
        """Retrieve a todo for the current user."""
        try:
            todo = TodoService.get_todo_by_id(
                db=db, todo_id=todo_id, user_id=current_user.id
            )
            if not todo:
                raise HTTPException(status_code=404, detail="Todo not found")
            return todo
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def update(db: Session, todo_id: int, todo: TodoUpdate, current_user: User) -> TodoItem:
        """Update a todo for the current user."""
        try:
            updated_todo = TodoService.update(
                db=db, todo_id=todo_id, todo=todo, user_id=current_user.id
            )
            if not updated_todo:
                raise HTTPException(status_code=404, detail="Todo not found")
            return updated_todo
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def delete(db: Session, todo_id: int, current_user: User) -> bool:
        """Delete a todo for the current user."""
        try:
            result = TodoService.delete(
                db=db, todo_id=todo_id, user_id=current_user.id
            )
            if not result:
                raise HTTPException(status_code=404, detail="Todo not found")
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
