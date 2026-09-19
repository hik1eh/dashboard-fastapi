import { Bell, CalendarDays, CheckSquare2, ClipboardList, Home, LogOut, Menu, NotebookPen, Repeat2, Settings, Snowflake, Target, X } from 'lucide-react'
import { useState } from 'react'
import { NavLink, Outlet } from 'react-router-dom'
import { AppFeedback } from '../components/UI'
import { useAuth } from '../lib/AuthContext'
import catDogMark from '../assets/cat-dog-mark.png'

const nav = [
  ['/', Home, 'Главная'], ['/tasks', CheckSquare2, 'Задачи и цели'], ['/calendar', CalendarDays, 'Календарь'],
  ['/reminders', Bell, 'Напоминания'], ['/schedule', ClipboardList, 'Расписание'], ['/habits', Repeat2, 'Привычки'],
  ['/plans', Target, 'Планы'], ['/notes', NotebookPen, 'Заметки'], ['/settings', Settings, 'Настройки'],
] as const

export function AppLayout() {
  const [open, setOpen] = useState(false)
  const { user, logout } = useAuth()
  return <div className="app-shell">
    <button className="mobile-menu" onClick={() => setOpen(true)} aria-label="Открыть меню"><Menu/></button>
    {open && <button className="sidebar-scrim" onClick={() => setOpen(false)} aria-label="Закрыть меню"/>}
    <aside className={`sidebar ${open ? 'open' : ''}`}>
      <div className="brand"><div className="brand-mark"><Snowflake/></div><div><strong>MoonFlow</strong><span>for любимка</span></div><button className="sidebar-close" onClick={() => setOpen(false)}><X/></button></div>
      <nav>{nav.map(([path, Icon, label]) => <NavLink key={path} to={path} end={path === '/'} onClick={() => setOpen(false)}><Icon size={19}/><span>{label}</span></NavLink>)}</nav>
      <div className="sidebar-mascot"><img src={catDogMark} alt="Кот и собака"/></div>
      <div className="user-card"><div className="avatar">{user?.name.charAt(0).toUpperCase()}</div><div><strong>{user?.name}</strong><span>{user?.email}</span></div><button className="icon" onClick={logout} title="Выйти" aria-label="Выйти"><LogOut size={18}/></button></div>
    </aside>
    <main><Outlet/></main><AppFeedback/>
  </div>
}
