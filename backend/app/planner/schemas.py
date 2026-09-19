from uuid import UUID
from datetime import date, datetime, time

from pydantic import Field, BaseModel, ConfigDict, model_validator

class OrmSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
class TaskCreate(BaseModel):
    title : str = Field(min_length=1, max_length=200)
    due_date : date | None = None
    priority : str = Field(default='medium', pattern='^(low|medium|high)$')
    
    
class TaskRead(TaskCreate, OrmSchema):
    id : UUID 
    completed : bool
    
    
class CalendarCreate(BaseModel):
    title: str = Field(min_length=1, max_length=180)
    starts_at: datetime
    ends_at: datetime | None = None
    color: str = "#7dd3fc"
    
    @model_validator(mode='after')
    def end_after_start(self) -> 'CalendarCreate':
        if self.ends_at and self.ends_at < self.starts_at:
            raise ValueError('ends_at must not be before starts_at')
        return self
    
    
class CalendarRead(CalendarCreate, OrmSchema):
    id: UUID
  
  
class GoalCreate(BaseModel):
    title: str = Field(min_length=1, max_length=180)
    week_start: date


class GoalRead(GoalCreate, OrmSchema):
    id: UUID
    progress: int
    
      
class ReminderCreate(BaseModel):
    title: str = Field(min_length=1, max_length=180)
    remind_at: datetime


class ReminderRead(ReminderCreate, OrmSchema):
    id: UUID
    completed: bool


class ScheduleCreate(BaseModel):
    title: str = Field(min_length=1, max_length=180)
    weekday: int = Field(ge=0, le=6)
    starts_at: time
    ends_at: time
    location: str | None = Field(default=None, max_length=120)
    
    @model_validator(mode='after')
    def end_after_start(self) -> "ScheduleCreate":
        if self.ends_at <= self.starts_at:
            raise ValueError("ends_at must be after starts_at")
        return self

class ScheduleRead(ScheduleCreate, OrmSchema):
    id: UUID
    
class HobbyCreate(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    color: str = "#67e8f9"


class HobbyRead(HobbyCreate, OrmSchema):
    id: UUID
    checked_days: list[date] = Field(default_factory=list)


class PlanCreate(BaseModel):
    title: str = Field(min_length=1, max_length=180)
    description: str = Field(default="", max_length=4000)


class PlanRead(PlanCreate, OrmSchema):
    id: UUID
    completed: bool


class NoteCreate(BaseModel):
    title: str = Field(min_length=1, max_length=180)
    content: str = Field(default="", max_length=20000)


class NoteRead(NoteCreate, OrmSchema):
    id: UUID
    updated_at: datetime


class DashboardRead(BaseModel):
    tasks: list[TaskRead]
    goals: list[GoalRead]
    events: list[CalendarRead]
    reminders: list[ReminderRead]
    schedule: list[ScheduleRead]
    habits: list[HobbyRead]
    plans: list[PlanRead]
    notes: list[NoteRead]
