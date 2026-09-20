export type Priority = 'low' | 'medium' | 'high'
export interface User { id: string; email: string; name: string }
export interface AuthResponse { user: User; message: string; access_token: string; token_type: string }
export interface Task { id: string; title: string; due_date: string | null; priority: Priority; completed: boolean }
export interface Goal { id: string; title: string; week_start: string; progress: number }
export interface CalendarEvent { id: string; title: string; starts_at: string; ends_at: string | null; color: string }
export interface Reminder { id: string; title: string; remind_at: string; completed: boolean }
export interface Schedule { id: string; title: string; week_number: 1 | 2; weekday: number; starts_at: string; ends_at: string; location: string | null }
export interface Habit { id: string; title: string; color: string; checked_days: string[] }
export interface Plan { id: string; title: string; description: string; completed: boolean }
export interface Note { id: string; title: string; content: string; updated_at: string }
export interface Dashboard { tasks: Task[]; goals: Goal[]; events: CalendarEvent[]; reminders: Reminder[]; schedule: Schedule[]; habits: Habit[]; plans: Plan[]; notes: Note[] }
export type EntityKind = 'tasks' | 'goals' | 'calendars' | 'reminders' | 'schedule' | 'habits' | 'plans' | 'notes'
export type TaskInput = Omit<Task, 'id' | 'completed'>
export type GoalInput = Omit<Goal, 'id' | 'progress'>
export type EventInput = Omit<CalendarEvent, 'id'>
export type ReminderInput = Omit<Reminder, 'id' | 'completed'>
export type ScheduleInput = Omit<Schedule, 'id'>
export type HabitInput = Omit<Habit, 'id' | 'checked_days'>
export type PlanInput = Omit<Plan, 'id' | 'completed'>
export type NoteInput = Pick<Note, 'title' | 'content'>
