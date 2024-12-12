from typing import Optional, List
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, validator


class PriorityEnum(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class StatusEnum(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class TodoBase(BaseModel):
    title: str = Field(..., example="Finish the report")
    description: str = Field(...,
                             example="Complete the quarterly financial report")
    start_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    priority: PriorityEnum = PriorityEnum.MEDIUM
    status: StatusEnum = StatusEnum.PENDING
    tags: Optional[List[str]] = []
    category: str = Field(..., example="Work")

    @validator("status", pre=True, always=True)
    def status_to_upper(cls, v):
        if isinstance(v, str):
            return v.upper()
        return v

    class Config:
        use_enum_values = True


class TodoCreate(TodoBase):
    pass

    class Config:
        use_enum_values = True


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    priority: Optional[PriorityEnum] = None
    status: Optional[StatusEnum] = None
    tags: Optional[List[str]] = None
    category: Optional[str] = None


class TodoResponse(TodoBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
