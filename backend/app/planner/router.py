from collections.abc import Awaitable
from datetime import date
from typing import Annotated, TypeVar
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.auth.dependencies import CurrentUser, DbSession
from app.planner.exceptions import InvalidGoalProgress, ItemNotFound, UnknowItemKind
from app.planner.schemas import (
    CalendarCreate, CalendarRead, 
    NoteCreate, NoteRead, 
    PlanCreate, PlanRead, 
    ReminderCreate, ReminderRead, 
    ScheduleCreate, ScheduleRead, 
    TaskCreate, TaskRead,
    GoalCreate, GoalRead,
    HobbyCreate, HobbyRead, 
    DashboardRead)
from app.planner.models import Calendar, Note, CorePlan, Reminder, Schedule, Task, WeeklyGoal
from app.planner.services import PlannerService

router = APIRouter(prefix='/planner', tags=['planner'])
Result = TypeVar('Result')

def get_planner_service(db: DbSession) -> PlannerService:
    return PlannerService(db)

PlannerServiceDep = Annotated[PlannerService, Depends(get_planner_service)]

async def execute(use_case: Awaitable[Result]) -> Result:
    
    try:
        return await use_case
    except ItemNotFound as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'Item not found') from exc
    except UnknowItemKind as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Unknown item type") from exc
    except InvalidGoalProgress as exc:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "Progress must be between 0 and 100") from exc

@router.delete("/{kind}/{item_id}", status_code=204)
async def delete_item(kind: str, item_id: UUID, user: CurrentUser, service: PlannerServiceDep) -> Response:
    await execute(service.delete(kind, user.id, item_id))
    return Response(status_code=204)

@router.get('/dashboard', response_model=DashboardRead)
async def dashboard(user: CurrentUser, service: PlannerServiceDep) -> DashboardRead:
    return await service.dashboard(user.id)

@router.post('/tasks', response_model=TaskRead, status_code=201)
async def create_task(data: TaskCreate, user: CurrentUser, service: PlannerServiceDep) -> Task:
    return await service.create_task(user.id, data)

@router.patch('/tasks/{item_id}/toggle', response_model=TaskRead)
async def toggle_task(item_id: UUID, user: CurrentUser, service: PlannerServiceDep) -> Task:
    return await execute(service.toggle_task(user.id, item_id))

@router.put("/tasks/{item_id}", response_model=TaskRead)
async def update_task(item_id: UUID, data: TaskCreate, user: CurrentUser, service: PlannerServiceDep) -> Task:
    return await execute(service.update_task(user.id, item_id, data))

@router.post("/goals", response_model=GoalRead, status_code=201)
async def create_goal(data: GoalCreate, user: CurrentUser, service: PlannerServiceDep) -> WeeklyGoal:
    return await service.create_goal(user.id, data)

@router.patch("/goals/{item_id}/progress/{progress}", response_model=GoalRead)
async def set_goal_progress(item_id: UUID, progress: int, user: CurrentUser, service: PlannerServiceDep) -> WeeklyGoal:
    return await execute(service.set_goal_progress(user.id, item_id, progress))

@router.put("/goals/{item_id}", response_model=GoalRead)
async def update_goal(item_id: UUID, data: GoalCreate, user: CurrentUser, service: PlannerServiceDep) -> WeeklyGoal:
    return await execute(service.update_goal(user.id, item_id, data))

@router.post("/events", response_model=CalendarRead, status_code=201)
async def create_event(data: CalendarCreate, user: CurrentUser, service: PlannerServiceDep) -> Calendar:
    return await service.create_calendar(user.id, data)

@router.put("/events/{item_id}", response_model=CalendarRead)
async def update_event(item_id: UUID, data: CalendarCreate, user: CurrentUser, service: PlannerServiceDep) -> Calendar:
    return await execute(service.update_calendar(user.id, item_id, data))

@router.post("/reminders", response_model=ReminderRead, status_code=201)
async def create_reminder(data: ReminderCreate, user: CurrentUser, service: PlannerServiceDep) -> Reminder:
    return await service.create_reminder(user.id, data)

@router.patch("/reminders/{item_id}/toggle", response_model=ReminderRead)
async def toggle_reminder(item_id: UUID, user: CurrentUser, service: PlannerServiceDep) -> Reminder:
    return await execute(service.toggle_reminder(user.id, item_id))

@router.put("/reminders/{item_id}", response_model=ReminderRead)
async def update_reminder(item_id: UUID, data: ReminderCreate, user: CurrentUser, service: PlannerServiceDep) -> Reminder:
    return await execute(service.update_reminder(user.id, item_id, data))

@router.post("/schedule", response_model=ScheduleRead, status_code=201)
async def create_schedule(data: ScheduleCreate, user: CurrentUser, service: PlannerServiceDep) -> Schedule:
    return await service.create_schedule(user.id, data)

@router.put("/schedule/{item_id}", response_model=ScheduleRead)
async def update_schedule(item_id: UUID, data: ScheduleCreate, user: CurrentUser, service: PlannerServiceDep) -> Schedule:
    return await execute(service.update_schedule(user.id, item_id, data))

@router.post("/habits", response_model=HobbyRead, status_code=201)
async def create_habit(data: HobbyCreate, user: CurrentUser, service: PlannerServiceDep) -> HobbyRead:
    return await service.create_habit(user.id, data)

@router.put("/habits/{item_id}/checkins/{day}", status_code=204)
async def toggle_habit_day(item_id: UUID, day: date, user: CurrentUser, service: PlannerServiceDep) -> Response:
    await execute(service.toggle_habit_day(user.id, item_id, day))
    return Response(status_code=204)

@router.put("/habits/{item_id}", response_model=HobbyRead)
async def update_habit(item_id: UUID, data: HobbyCreate, user: CurrentUser, service: PlannerServiceDep) -> HobbyRead:
    return await execute(service.update_habit(user.id, item_id, data))

@router.post("/plans", response_model=PlanRead, status_code=201)
async def create_plan(data: PlanCreate, user: CurrentUser, service: PlannerServiceDep) -> CorePlan:
    return await service.create_plan(user.id, data)

@router.patch("/plans/{item_id}/toggle", response_model=PlanRead)
async def toggle_plan(item_id: UUID, user: CurrentUser, service: PlannerServiceDep) -> CorePlan:
    return await execute(service.toggle_plan(user.id, item_id))

@router.put("/plans/{item_id}", response_model=PlanRead)
async def update_plan(item_id: UUID, data: PlanCreate, user: CurrentUser, service: PlannerServiceDep) -> CorePlan:
    return await execute(service.update_plan(user.id, item_id, data))

@router.post("/notes", response_model=NoteRead, status_code=201)
async def create_note(data: NoteCreate, user: CurrentUser, service: PlannerServiceDep) -> Note:
    return await service.create_note(user.id, data)

@router.put("/notes/{item_id}", response_model=NoteRead)
async def update_note(item_id: UUID, data: NoteCreate, user: CurrentUser, service: PlannerServiceDep) -> Note:
    return await execute(service.update_note(user.id, item_id, data))
