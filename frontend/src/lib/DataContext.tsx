/* eslint-disable react-refresh/only-export-components */
import { createContext, useCallback, useContext, useEffect, useState, type ReactNode } from 'react'
import { api } from './api'
import type { Dashboard } from '../types'

type DataState = { data: Dashboard | null; loading: boolean; error: string; refresh: () => Promise<void>; mutate: (action: () => Promise<unknown>, success?: string) => Promise<boolean>; notice: string }
const Context = createContext<DataState | null>(null)

export function DataProvider({ children }: { children: ReactNode }) {
  const [data, setData] = useState<Dashboard | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [notice, setNotice] = useState('')
  const refresh = useCallback(async () => { try { setError(''); setData(await api.dashboard()) } catch (err) { setError(err instanceof Error ? err.message : 'Нет связи с сервером') } finally { setLoading(false) } }, [])
  useEffect(() => {
    let active = true
    api.dashboard().then((result) => { if (active) setData(result) }).catch((err: unknown) => { if (active) setError(err instanceof Error ? err.message : 'Нет связи с сервером') }).finally(() => { if (active) setLoading(false) })
    return () => { active = false }
  }, [])
  const mutate = async (action: () => Promise<unknown>, success = 'Изменения сохранены') => {
    try { setError(''); await action(); await refresh(); setNotice(success); window.setTimeout(() => setNotice(''), 2800); return true }
    catch (err) { setError(err instanceof Error ? err.message : 'Не удалось сохранить'); return false }
  }
  return <Context.Provider value={{ data, loading, error, refresh, mutate, notice }}>{children}</Context.Provider>
}
export function useData() { const value = useContext(Context); if (!value) throw new Error('DataProvider is missing'); return value }
