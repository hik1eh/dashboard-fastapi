from datetime import date, datetime, time
from uuid import UUID, uuid4

from sqlaclhemy import Boolean, Date, DateTime, ForeignKey, Integer, String, Text, Time, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimeStampMixin

class OwnedMixin:
    user_id : Mapped[UUID] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), index=True)
    
    
class Task(OwnedMixin, TimeStampMixin, Base):
    __tablename__ = 'tasks'
    id : Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    title : Mapped[str] = mapped_column(String(180))
    due_date : Mapped[date | None] = mapped_column(Date)
    priority : Mapped[str] = mapped_column(String(20), default='medium')
    completed : Mapped[bool] = mapped_column(Boolean, default=False)


class Calendar(OwnedMixin, TimeStampMixin, Base):
    __tablename__ = 'calendars'
    id : Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    title : Mapped[str] = mapped_column(String(180))
    starts_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    ends_at : Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    color : Mapped[str] = mapped_column(String(16), default='#7dd3fc')


class WeeklyGoal(OwnedMixin, TimeStampMixin, Base):
    __tablename__ = 'weeklygoals'
    id : Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    title : Mapped[str] = mapped_column(String(180))
    week_start : Mapped[datetime] = mapped_column(Date)
    progress : Mapped[int] = mapped_column(Integer, default=0)


class Schedule(OwnedMixin, TimeStampMixin, Base): 
    __tablename__ = 'schedules'
    id : Mapped[UUID] = mapped_column(primary_key=True,  default=uuid4)
    title : Mapped[str] = mapped_column(String(180))
    weekday : Mapped[int] = mapped_column(Integer)
    starts_at : Mapped[time] = mapped_column(Time)
    ends_at : Mapped[time] = mapped_column(Time)
    location : Mapped[str | None] = mapped_column(String(16))
    
    
class Reminder(OwnedMixin, TimeStampMixin, Base):
    __tablename__ = 'reminders'
    id : Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    title : Mapped[str] = mapped_column(String(180))
    remind_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    completed : Mapped[bool] = mapped_column(Boolean, default=True)

class Hobby(OwnedMixin, TimeStampMixin, Base):
    __tablename__ = 'hobbyes'
    id : Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    title : Mapped[str] = mapped_column(String(180))
    color: Mapped[str] = mapped_column(String(16), default="#67e8f9")
    
    
class HobbyCheker(OwnedMixin, TimeStampMixin, Base):
    __tablename__ = 'hobbychekers'
    __table_args__ = (UniqueConstraint("habit_id", "day", name="uq_habit_day"),)
    id : Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    habit_id: Mapped[UUID] = mapped_column(ForeignKey("hobbyes.id", ondelete="CASCADE"), index=True)
    day: Mapped[date] = mapped_column(Date)
    
    
class CorePlan(OwnedMixin, TimeStampMixin, Base):
    __tablename__ = 'coreplans'
    id : Mapped[str] = mapped_column(primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(String(180))
    description: Mapped[str] = mapped_column(Text, default="")
    completed: Mapped[bool] = mapped_column(Boolean, default=False)

class Note(OwnedMixin, TimeStampMixin, Base):
    __tablename__ = "notes"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(String(180))
    content: Mapped[str] = mapped_column(Text, default="")