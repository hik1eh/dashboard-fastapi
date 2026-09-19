from datetime import date
from typing import Generic, TypeVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.planner.models import (
    Calendar,
    Hobby,
    HobbyCheker,
    Note,
    CorePlan,
    Reminder,
    Schedule,
    Task,
    WeeklyGoal,
)

OwnedModel = TypeVar(
    "OwnedModel", Task, WeeklyGoal, Calendar, Reminder, Schedule, Hobby, CorePlan, Note
)

class OwnedRepository(Generic[OwnedModel]):
    
    model : type[OwnedModel]
    order_by : tuple[object, ...]
    
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        
    async def list_for_user(self, user_id: UUID) -> list[OwnedModel]:
        result = await self.session.scalars(
            select(self.model)
            .where(self.model.user_id == user_id)
            .order_by(*self.order_by)
        )
        return list(result.all())
    
    async def get_owned(self, item_id: UUID, user_id: UUID) -> OwnedModel | None:
        return await self.session.scalar(
            select(self.model).where(self.model.id == item_id,
                                     self.model.user_id == user_id)
        )
        
    def add (self, item: OwnedModel) -> None:
        self.session.add(item)
        
    async def delete(self, item: OwnedModel) -> None:
        await self.session.delete(item)

class TaskRepository(OwnedRepository[Task]):
    model = Task
    order_by = (Task.created_at.desc(),)


class GoalRepository(OwnedRepository[WeeklyGoal]):
    model = WeeklyGoal
    order_by = (WeeklyGoal.week_start.desc(),)


class CalendarRepository(OwnedRepository[Calendar]):
    model = Calendar
    order_by = (Calendar.starts_at,)


class ReminderRepository(OwnedRepository[Reminder]):
    model = Reminder
    order_by = (Reminder.remind_at,)


class ScheduleRepository(OwnedRepository[Schedule]):
    model = Schedule
    order_by = (Schedule.weekday, Schedule.starts_at)


class PlanRepository(OwnedRepository[CorePlan]):
    model = CorePlan
    order_by = (CorePlan.created_at.desc(),)


class NoteRepository(OwnedRepository[Note]):
    model = Note
    order_by = (Note.updated_at.desc(),)
    
class HobbyRepository(OwnedRepository[Hobby]):
    model = Hobby
    order_by = (Hobby.created_at,)

    async def checkin(self, habit_id: UUID, day: date) -> HobbyCheker | None:
        return await self.session.scalar(
            select(HobbyCheker).where(
                HobbyCheker.habit_id == habit_id,
                HobbyCheker.day == day,
            )
        )

    async def checkins_since(
        self, habit_ids: list[UUID], start: date
    ) -> list[tuple[UUID, date]]:
        if not habit_ids:
            return []
        rows = await self.session.execute(
            select(HobbyCheker.habit_id, HobbyCheker.day).where(
                HobbyCheker.habit_id.in_(habit_ids),
                HobbyCheker.day >= start,
            )
        )
        return list(rows.tuples().all())

    def add_checkin(self, checkin: HobbyCheker) -> None:
        self.session.add(checkin)

    async def delete_checkin(self, checkin: HobbyCheker) -> None:
        await self.session.delete(checkin)
        

class PlannerRepositories:
    
    def __init__(self, session: AsyncSession) -> None:
        self.tasks = TaskRepository(session)
        self.goals = GoalRepository(session)
        self.calendars = CalendarRepository(session)
        self.reminders = ReminderRepository(session)
        self.schedule = ScheduleRepository(session)
        self.habits = HobbyRepository(session)
        self.plans = PlanRepository(session)
        self.notes = NoteRepository(session)

    def by_kind(self, kind: str) -> OwnedRepository | None:
        return {
            "tasks": self.tasks,
            "goals": self.goals,
            "calendars": self.calendars,
            "reminders": self.reminders,
            "schedule": self.schedule,
            "habits": self.habits,
            "plans": self.plans,
            "notes": self.notes,
        }.get(kind)