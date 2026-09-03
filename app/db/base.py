from datetime import UTC, datetime

from sqlalchemy import Datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """ """

class TimeStampMixin:
    created_at : Mapped[datetime] = mapped_column(
        Datetime(timezone=True), default = lambda: datetime.now(UTC)
    )
    updated_at : Mapped[datetime] = mapped_column(
        Datetime(timezone=True), default = lambda: datetime.now(UTC),
        onupdate = lambda: datetime.now(UTC)
    )