from __future__ import annotations

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimeStampMixin

class User(TimeStampMixin, Base):
    __tablename__ = "users"
    
    id : Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    email : Mapped[str] = mapped_column(String(60), unique=True, index=True)
    name : Mapped[str] = mapped_column(String(60))
    password_hash : Mapped[str] = mapped_column(String(255))
    is_active : Mapped[bool] = mapped_column(Boolean, default=True)