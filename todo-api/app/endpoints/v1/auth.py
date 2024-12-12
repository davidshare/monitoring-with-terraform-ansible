from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from app.core.database import get_db
from app.auth.controller import AuthController
from app.auth.schemas import UserCreate, UserResponse, UserLogin
from app.auth.dependencies import get_current_user
from app.auth.models import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return AuthController.register_user(user, db)


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    return AuthController.login_user(user, db)


@router.get("/profile", response_model=UserResponse)
def get_user_profile(current_user: User = Depends(get_current_user)):
    """Retrieve the profile of the authenticated user."""
    return AuthController.get_user_profile(current_user)
