from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from .schemas import UserCreate, UserResponse, UserLogin
from .service import AuthService
from .models import User


class AuthController:
    @staticmethod
    def register_user(user: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
        """Handle user registration."""
        try:
            new_user = AuthService.register_user(db, user)
            return UserResponse(
                id=new_user.id, username=new_user.username, email=new_user.email
            )
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail="An error occurred during registration"
            )

    @staticmethod
    def login_user(user: UserLogin, db: Session = Depends(get_db)) -> dict:
        """Handle user login and return JWT token."""
        try:
            access_token = AuthService.authenticate_user(
                db, user.email, user.password
            )
            return {"access_token": access_token, "token_type": "bearer"}
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail="An error occurred during login", error=e
            )

    @staticmethod
    def get_user_profile(current_user: User, db: Session = Depends(get_db)) -> UserResponse:
        """Retrieve user profile."""
        try:
            if not current_user:
                raise HTTPException(
                    status_code=401, detail="Not authenticated"
                )
            return UserResponse(
                id=current_user.id, username=current_user.username, email=current_user.email
            )
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)
        except Exception:
            raise HTTPException(
                status_code=500, detail="An error occurred while fetching profile"
            )
