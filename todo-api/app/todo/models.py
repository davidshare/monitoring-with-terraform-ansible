from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum
from datetime import datetime


class PriorityEnum(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class StatusEnum(enum.Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class TodoItem(Base):
    __tablename__ = "todo_items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    start_date = Column(DateTime, nullable=True, default=None)
    due_date = Column(DateTime, nullable=True, default=None)
    priority = Column(Enum(PriorityEnum, native_enum=False),
                      default=PriorityEnum.MEDIUM, nullable=False)
    status = Column(Enum(StatusEnum, native_enum=True),
                    default=StatusEnum.PENDING, nullable=False)
    tags = Column(String, nullable=True)  # Comma-separated values for tags
    category = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)

    # Foreign key to associate with the User model
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationship with the User model
    user = relationship("User", back_populates="todos")
