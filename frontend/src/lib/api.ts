import type { AuthResponse, Dashboard, EntityKind, User } from '../types'

const API_URL = (import.meta.env.VITE_API_URL || '/api').replace(/\/$/, '')
const TOKEN_KEY = 'planner_access_token'

export const tokenStore = {
  get: () => localStorage.getItem(TOKEN_KEY),
  set: (token: string) => localStorage.setItem(TOKEN_KEY, token),
  clear: () => localStorage.removeItem(TOKEN_KEY),
}

export class ApiError extends Error {
  constructor(message: string, public status: number) { super(message) }
}

function errorMessage(status: number, payload: unknown): string {
  if (payload && typeof payload === 'object' && 'detail' in payload) {
    const detail = (payload as { detail: unknown }).detail
    if (typeof detail === 'string') return detail
    if (Array.isArray(detail)) return detail.map((item) => typeof item === 'object' && item && 'msg' in item ? String(item.msg) : 'Некорректное значение').join('. ')
  }
  return ({ 400: 'Проверьте введённые данные', 404: 'Запись не найдена', 409: 'Такая запись уже существует', 422: 'Данные не прошли проверку', 500: 'Сервис временно недоступен' } as Record<number, string>)[status] || 'Не удалось выполнить запрос'
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const token = tokenStore.get()
  const response = await fetch(`${API_URL}${path}`, { ...init, headers: { 'Content-Type': 'application/json', ...(token ? { Authorization: `Bearer ${token}` } : {}), ...init?.headers } })
  if (!response.ok) {
    const payload = await response.json().catch(() => null)
    if (response.status === 401 && path !== '/auth/login') window.dispatchEvent(new Event('auth:unauthorized'))
    throw new ApiError(errorMessage(response.status, payload), response.status)
  }
  if (response.status === 204) return undefined as T
  return response.json() as Promise<T>
}

export const api = {
  register: (data: { name: string; email: string; password: string }) => request<AuthResponse>('/auth/register', { method: 'POST', body: JSON.stringify(data) }),
  login: (data: { email: string; password: string }) => request<AuthResponse>('/auth/login', { method: 'POST', body: JSON.stringify(data) }),
  me: () => request<User>('/auth/me'),
  logout: () => request<void>('/auth/logout', { method: 'POST' }),
  dashboard: () => request<Dashboard>('/planner/dashboard'),
  create: <T>(path: string, data: unknown) => request<T>(`/planner/${path}`, { method: 'POST', body: JSON.stringify(data) }),
  update: <T>(path: string, id: string, data: unknown) => request<T>(`/planner/${path}/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  remove: (kind: EntityKind, id: string) => request<void>(`/planner/${kind}/${id}`, { method: 'DELETE' }),
  toggle: <T>(path: string, id: string) => request<T>(`/planner/${path}/${id}/toggle`, { method: 'PATCH' }),
  progress: (id: string, value: number) => request(`/planner/goals/${id}/progress/${value}`, { method: 'PATCH' }),
  checkin: (id: string, day: string) => request<void>(`/planner/habits/${id}/checkins/${day}`, { method: 'PUT' }),
}
