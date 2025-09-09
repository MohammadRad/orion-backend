"""SQLAlchemy models for the Orion backend.

The database schema consists of three tables:

* **users** – stores registered users with hashed passwords.
* **projects** – projects owned by users.  Each project has a name and an
  optional description.
* **tasks** – tasks belong to projects and have a title and status.  The
  status field uses a simple enumeration to indicate whether the task is
  pending, in progress or completed.

SQLAlchemy 2.0 style typing is used to make the code concise and type
checked.  Relationships are configured so that tasks can refer to their
associated project, and projects reference their owner.
"""

from enum import Enum
from typing import Optional
from sqlalchemy import Enum as SQLEnum, ForeignKey, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all models, from which SQLAlchemy inherits metadata."""
    pass


class TaskStatus(str, Enum):
    """Enumeration of allowed task status values."""

    TODO = "todo"
    DOING = "doing"
    DONE = "done"


class User(Base):
    """A registered user of the system."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))

    projects: Mapped[list["Project"]] = relationship(
        back_populates="owner", cascade="all, delete-orphan"
    )


class Project(Base):
    """A project belonging to a user."""

    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)

    owner: Mapped[User] = relationship(back_populates="projects")
    tasks: Mapped[list["Task"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )


class Task(Base):
    """A task belonging to a project."""

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    status: Mapped[TaskStatus] = mapped_column(SQLEnum(TaskStatus), default=TaskStatus.TODO)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)

    project: Mapped[Project] = relationship(back_populates="tasks")
