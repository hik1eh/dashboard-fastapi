from datetime import date, timedelta
from typing import TypeVar
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.planner.exceptions import InvalidGoalProgress, ItemNotFound, UnknowItemKind
from app.planner.models import (Calendar, Hobby,
                                HobbyCheker, Note,
                                CorePlan, Reminder,
                                Schedule, Task, WeeklyGoal)
from app.planner.repositories import OwnedRepository, PlannerRepositories
from app.planner.schemas import (DashboardRead, CalendarCreate,
                                 GoalCreate, HobbyCreate,
                                 HobbyRead, NoteCreate,
                                 PlanCreate, ReminderCreate,
                                 ScheduleCreate, TaskCreate)

Entity = TypeVar('Entity')


class PlannerService:
    
    def __init__(self, session: AsyncSession, repositories: PlannerRepositories | None = None) -> None:
        self.session = session,
        self.repositories = repositories or PlannerRepositories(session)
        
    async def dashboard(self, user_id: UUID) -> DashboardRead:
        tasks = await self.repositories.tasks.list_for_user(user_id)
        goals = await self.repositories.goals.list_for_user(user_id)
        calendars = await self.repositories.calendars.list_for_user(user_id)
        reminders = await self.repositories.reminders.list_for_user(user_id)
        schedule = await self.repositories.schedule.list_for_user(user_id)
        plans = await self.repositories.plans.list_for_user(user_id)
        notes = await self.repositories.notes.list_for_user(user_id)
        habits = await self.repositories.habits.list_for_user(user_id)
        return DashboardRead(
            tasks=tasks,
            goals=goals,
            calendars=calendars,
            reminders=reminders,
            schedule=schedule,
            plans=plans,
            notes=notes,
            habits=habits
        )
        
    async def create_task(self, user_id: UUID, data: TaskCreate) -> Task:
        return await self._create(self.repositories.tasks, Task(**data.model_dump(), user_id=user_id))
    
    async def toggle_task(self, user_id: UUID, item_id: UUID) -> Task:
        item = await self._owned(self.repositories.tasks, item_id, user_id)
        item.compeleted = not item.completed
        return await self._save(item)
    
    async def update_task(self, user_id: UUID, item_id: UUID, data: TaskCreate) -> Task:
        item = await self._owned(self.repositories.tasks, item_id, user_id)
        item.tittle, item.due_date, item.priority = data.title, data.due_date, data.priority
        return await self._save(item)

    async def update_task(self, user_id: UUID, item_id: UUID, data: TaskCreate) -> Task:
        item = await self._owned(self.repositories.tasks, item_id, user_id)
        item.title, item.due_date, item.priority = data.title, data.due_date, data.priority
        return await self._save(item)

    async def create_goal(self, user_id: UUID, data: GoalCreate) -> WeeklyGoal:
        return await self._create(self.repositories.goals, WeeklyGoal(**data.model_dump(), user_id=user_id))

    async def set_goal_progress(self, user_id: UUID, item_id: UUID, progress: int) -> WeeklyGoal:
        if not 0 <= progress <= 100:
            raise InvalidGoalProgress
        item = await self._owned(self.repositories.goals, item_id, user_id)
        item.progress = progress
        return await self._save(item)

    async def update_goal(self, user_id: UUID, item_id: UUID, data: GoalCreate) -> WeeklyGoal:
        item = await self._owned(self.repositories.goals, item_id, user_id)
        item.title, item.week_start = data.title, data.week_start
        return await self._save(item)
    
    async def create_calendar(self, user_id: UUID, data: CalendarCreate) -> Calendar:
        return await self._create(self.repositories.calendars, Calendar(**data.model_dump(), user_id=user_id))
    
    async def update_calendar(self, user_id: UUID, item_id: UUID, data: CalendarCreate) -> Calendar:
        item = await self._owned(self.repositories.calendars, item_id, user_id)
        item.title, item.starts_at, item.ends_at, item.color = data.title, data.starts_at, data.ends_at, data.color
        return await self._save(item)
    
    async def create_reminder(self, user_id: UUID, data: ReminderCreate) -> Reminder:
        return await self._create(self.repositories.reminders, Reminder(**data.model_dump(), user_id=user_id))

    async def toggle_reminder(self, user_id: UUID, item_id: UUID) -> Reminder:
        item = await self._owned(self.repositories.reminders, item_id, user_id)
        item.completed = not item.completed
        return await self._save(item)

    async def update_reminder(self, user_id: UUID, item_id: UUID, data: ReminderCreate) -> Reminder:
        item = await self._owned(self.repositories.reminders, item_id, user_id)
        item.title, item.remind_at = data.title, data.remind_at
        return await self._save(item)

    async def create_schedule(self, user_id: UUID, data: ScheduleCreate) -> Schedule:
        return await self._create(self.repositories.schedule, Schedule(**data.model_dump(), user_id=user_id))

    async def update_schedule(self, user_id: UUID, item_id: UUID, data: ScheduleCreate) -> Schedule:
        item = await self._owned(self.repositories.schedule, item_id, user_id)
        item.title, item.weekday = data.title, data.weekday
        item.starts_at, item.ends_at, item.location = data.starts_at, data.ends_at, data.location
        return await self._save(item)

    async def create_habit(self, user_id: UUID, data: HobbyCreate) -> HobbyRead:
        item = await self._create(self.repositories.habits, Hobby(**data.model_dump(), user_id=user_id))
        return HobbyRead(id=item.id, title=item.title, color=item.color, checked_days=[])

    async def toggle_habit_day(self, user_id: UUID, item_id: UUID, day: date) -> None:
        await self._owned(self.repositories.habits, item_id, user_id)
        checkin = await self.repositories.habits.checkin(item_id, day)
        if checkin:
            await self.repositories.habits.delete_checkin(checkin)
        else:
            self.repositories.habits.add_checkin(HobbyCheker(habit_id=item_id, day=day))
        await self.session.commit()

    async def update_habit(self, user_id: UUID, item_id: UUID, data: HobbyCreate) -> HobbyRead:
        item = await self._owned(self.repositories.habits, item_id, user_id)
        item.title, item.color = data.title, data.color
        await self._save(item)
        return next(habit for habit in await self._habit_reads(user_id) if habit.id == item.id)

    async def create_plan(self, user_id: UUID, data: PlanCreate) -> CorePlan:
        return await self._create(self.repositories.plans, CorePlan(**data.model_dump(), user_id=user_id))

    async def toggle_plan(self, user_id: UUID, item_id: UUID) -> CorePlan:
        item = await self._owned(self.repositories.plans, item_id, user_id)
        item.completed = not item.completed
        return await self._save(item)

    async def update_plan(self, user_id: UUID, item_id: UUID, data: PlanCreate) -> CorePlan:
        item = await self._owned(self.repositories.plans, item_id, user_id)
        item.title, item.description = data.title, data.description
        return await self._save(item)

    async def create_note(self, user_id: UUID, data: NoteCreate) -> Note:
        return await self._create(self.repositories.notes, Note(**data.model_dump(), user_id=user_id))

    async def update_note(self, user_id: UUID, item_id: UUID, data: NoteCreate) -> Note:
        item = await self._owned(self.repositories.notes, item_id, user_id)
        item.title, item.content = data.title, data.content
        return await self._save(item)

    async def delete(self, kind: str, user_id: UUID, item_id: UUID) -> None:
        repository = self.repositories.by_kind(kind)
        if not repository:
            raise UnknowItemKind
        item = await self._owned(repository, item_id, user_id)
        await repository.delete(item)
        await self.session.commit()

    async def _habit_reads(self, user_id: UUID) -> list[HobbyRead]:
        habits = await self.repositories.habits.list_for_user(user_id)
        rows = await self.repositories.habits.checkins_since(
            [habit.id for habit in habits], date.today() - timedelta(days=6)
        )
        checked: dict[UUID, list[date]] = {habit.id: [] for habit in habits}
        for habit_id, day in rows:
            checked[habit_id].append(day)
        return [
            HobbyRead(id=habit.id, title=habit.title, color=habit.color, checked_days=checked[habit.id])
            for habit in habits
        ]

    async def _owned(self, repository: OwnedRepository[Entity], item_id: UUID, user_id: UUID) -> Entity:
        item = await repository.get_owned(item_id, user_id)
        if not item:
            raise ItemNotFound
        return item

    async def _create(self, repository: OwnedRepository[Entity], item: Entity) -> Entity:
        repository.add(item)
        return await self._save(item)

    async def _save(self, item: Entity) -> Entity:
        await self.session.commit()
        await self.session.refresh(item)
        return item
