from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.todo.schemas import TodoCreate, TodoUpdate, TodoResponse
from app.todo.controller import TodoController
from app.auth.dependencies import get_current_user
from app.auth.models import User

router = APIRouter(prefix="/todos", tags=["Todos"])


@router.post("/", response_model=TodoResponse)
def create(
    todo: TodoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return TodoController.create(db=db, todo=todo, current_user=current_user)


@router.get("/", response_model=list[TodoResponse])
def get_all_todos(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    print(current_user)
    return TodoController.get_all_todos(db=db, current_user=current_user)


@router.get("/{todo_id}", response_model=TodoResponse)
def read(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return TodoController.get(db=db, todo_id=todo_id, current_user=current_user)


@router.put("/{todo_id}", response_model=TodoResponse)
def update(
    todo_id: int,
    todo: TodoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return TodoController.update(db=db, todo_id=todo_id, todo=todo, current_user=current_user)


@router.delete("/{todo_id}")
def delete(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return TodoController.delete(db=db, todo_id=todo_id, current_user=current_user)
