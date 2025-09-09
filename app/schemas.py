"""Pydantic schema definitions for request and response bodies.

The schemas mirror the database models but include only the fields that
should be exposed via the API.  They also perform basic validation
automatically.  For example, email addresses must be valid per RFC 5322 and
task status values must match the defined enumeration.
"""

from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from .models import TaskStatus


class UserCreate(BaseModel):
    """Schema for user registration."""

    email: EmailStr
    password: str = Field(min_length=6, description="Password must be at least 6 characters long")


class Token(BaseModel):
    """Schema returned after successful authentication."""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Data extracted from a validated JWT."""

    sub: str


class UserOut(BaseModel):
    """Public representation of a user."""

    id: int
    email: EmailStr

    class Config:
        from_attributes = True


class ProjectCreate(BaseModel):
    """Schema for creating projects."""

    name: str = Field(min_length=1, max_length=200)
    description: Optional[str] = None


class ProjectOut(BaseModel):
    """Representation of a project returned from the API."""

    id: int
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


class TaskCreate(BaseModel):
    """Schema for creating tasks."""

    title: str = Field(min_length=1, max_length=200)
    status: TaskStatus = TaskStatus.TODO


class TaskOut(BaseModel):
    """Representation of a task returned from the API."""

    id: int
    title: str
    status: TaskStatus

    class Config:
        from_attributes = True
