from sqlalchemy.orm import Session
from .models import User
from .schemas import UserCreate
from fastapi import HTTPException
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
import os

# Initialize bcrypt context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300


class AuthService:
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash the password using bcrypt with automatic salting."""
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify the provided password against the hashed password."""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
        """Generate a JWT token."""
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def register_user(db: Session, user: UserCreate) -> User:
        """Register a new user."""
        if db.query(User).filter((User.email == user.email) | (User.username == user.username)).first():
            raise HTTPException(
                status_code=400, detail="Username or email already exists")

        hashed_password = AuthService.hash_password(user.password)
        new_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> str:
        """Authenticate a user and return a JWT token."""
        user = db.query(User).filter(User.email == email).first()
        if not user or not AuthService.verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        access_token = AuthService.create_access_token({"sub": user.email})
        return access_token

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User:
        """Retrieve user details by email."""
        return db.query(User).filter(User.email == email).first()
