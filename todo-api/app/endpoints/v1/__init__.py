from fastapi import APIRouter
from .auth import router as auth_router
from .todo import router as todo_router

v1_router = APIRouter()

v1_router.include_router(auth_router)
v1_router.include_router(todo_router)
