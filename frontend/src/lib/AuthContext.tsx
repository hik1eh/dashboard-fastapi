/* eslint-disable react-refresh/only-export-components */
import { createContext, useContext, useEffect, useState, type ReactNode } from 'react'
import { api, tokenStore } from './api'
import type { User } from '../types'

type Credentials = { email: string; password: string }
type AuthState = { user: User | null; loading: boolean; login: (data: Credentials) => Promise<void>; register: (data: Credentials & { name: string }) => Promise<void>; logout: () => void }
const AuthContext = createContext<AuthState | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(() => Boolean(tokenStore.get()))
  useEffect(() => {
    let active = true
    const unauthorized = () => { tokenStore.clear(); setUser(null) }
    window.addEventListener('auth:unauthorized', unauthorized)
    if (tokenStore.get()) api.me().then((profile) => { if (active) setUser(profile) }).catch(() => tokenStore.clear()).finally(() => { if (active) setLoading(false) })
    return () => { active = false; window.removeEventListener('auth:unauthorized', unauthorized) }
  }, [])
  const accept = (response: { access_token: string; user: User }) => { tokenStore.set(response.access_token); setUser(response.user) }
  const login = async (data: Credentials) => accept(await api.login(data))
  const register = async (data: Credentials & { name: string }) => accept(await api.register(data))
  const logout = () => { void api.logout().catch(() => undefined); tokenStore.clear(); setUser(null) }
  return <AuthContext.Provider value={{ user, loading, login, register, logout }}>{children}</AuthContext.Provider>
}

export function useAuth() { const value = useContext(AuthContext); if (!value) throw new Error('AuthProvider is missing'); return value }
