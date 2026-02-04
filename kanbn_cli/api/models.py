"""Pydantic models for Kan.bn API entities."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class Workspace(BaseModel):
    """Workspace model."""

    id: Optional[str] = None
    public_id: Optional[str] = None
    name: str
    slug: Optional[str] = None
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class Board(BaseModel):
    """Board model."""

    id: Optional[str] = None
    public_id: Optional[str] = None
    workspace_id: Optional[str] = None
    name: str
    slug: Optional[str] = None
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class List(BaseModel):
    """List model."""

    id: Optional[str] = None
    public_id: Optional[str] = None
    board_id: Optional[str] = None
    name: str
    position: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class Label(BaseModel):
    """Label model."""

    id: Optional[str] = None
    public_id: Optional[str] = None
    board_id: Optional[str] = None
    name: str
    color: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ChecklistItem(BaseModel):
    """Checklist item model."""

    id: Optional[str] = None
    public_id: Optional[str] = None
    title: str
    completed: bool = False
    position: Optional[int] = None


class Checklist(BaseModel):
    """Checklist model."""

    id: Optional[str] = None
    public_id: Optional[str] = None
    title: str
    items: List[ChecklistItem] = Field(default_factory=list)


class Comment(BaseModel):
    """Comment model."""

    id: Optional[str] = None
    public_id: Optional[str] = None
    card_id: Optional[str] = None
    user_id: Optional[str] = None
    content: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class Card(BaseModel):
    """Card model."""

    id: Optional[str] = None
    public_id: Optional[str] = None
    list_id: Optional[str] = None
    title: str
    description: Optional[str] = None
    position: Optional[int] = None
    due_date: Optional[datetime] = None
    labels: List[Label] = Field(default_factory=list)
    checklists: List[Checklist] = Field(default_factory=list)
    comments: List[Comment] = Field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class User(BaseModel):
    """User model."""

    id: Optional[str] = None
    public_id: Optional[str] = None
    email: str
    name: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
