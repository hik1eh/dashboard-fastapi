import { format, parseISO, startOfWeek, subDays } from 'date-fns'
import { ru } from 'date-fns/locale'

export const todayKey = () => format(new Date(), 'yyyy-MM-dd')
export const toDateKey = (value: Date | string) => format(typeof value === 'string' ? parseISO(value) : value, 'yyyy-MM-dd')
export const formatDate = (value: string) => format(parseISO(value), 'd MMMM', { locale: ru })
export const formatDateTime = (value: string) => format(parseISO(value), 'd MMM, HH:mm', { locale: ru })
export const weekStartKey = () => format(startOfWeek(new Date(), { weekStartsOn: 1 }), 'yyyy-MM-dd')
export const lastSevenDays = () => Array.from({ length: 7 }, (_, i) => subDays(new Date(), 6 - i))
export const localDateTimeValue = (iso?: string | null) => iso ? format(parseISO(iso), "yyyy-MM-dd'T'HH:mm") : `${todayKey()}T09:00`
export const toIso = (local: string) => new Date(local).toISOString()
