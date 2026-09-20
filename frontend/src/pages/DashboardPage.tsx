import { ArrowUpRight, CalendarDays, CheckCircle2, Circle, Clock3, Flame, Target } from 'lucide-react'
import { Link } from 'react-router-dom'
import { Empty, Loading, Panel } from '../components/UI'
import { useData } from '../lib/DataContext'
import { formatDateTime, todayKey } from '../lib/dates'
import { useAuth } from '../lib/AuthContext'
import { format } from 'date-fns'
import { ru } from 'date-fns/locale'

export function DashboardPage() {
  const { data, loading } = useData()
  const { user } = useAuth()
  if (loading) return <Loading/>
  if (!data) return null
  const today = todayKey(); const todayTasks = data.tasks.filter((item) => item.due_date === today); const done = data.tasks.filter((item) => item.completed).length
  const reminders = [...data.reminders].filter((item) => !item.completed).sort((a,b) => a.remind_at.localeCompare(b.remind_at)).slice(0, 3)
  const events = [...data.events].filter((item) => item.starts_at >= new Date().toISOString()).slice(0, 3)
  const weekGoals = data.goals.slice(0, 3); const habitsDone = data.habits.filter((item) => item.checked_days.includes(today)).length
  const todaySchedule = data.schedule.filter(s => s.weekday === (new Date().getDay()+6)%7)
  return <div className="page dashboard-page">
    <header className="hero"><div><span className="eyebrow">{format(new Date(),'EEEE, d MMMM',{locale:ru})}</span><h1>Добрый день, {user?.name}</h1><p>Ваши задачи, встречи и привычки собраны в одном месте.</p><Link to="/tasks" className="primary">План на сегодня <ArrowUpRight size={18}/></Link></div><div className="today-badge"><span>сегодня</span><strong>{todayTasks.filter(t => t.completed).length}/{todayTasks.length}</strong><small>задач завершено</small></div></header>
    <div className="stats-row"><div><CheckCircle2/><span>Завершено<strong>{done}</strong></span></div><div><Circle/><span>В процессе<strong>{data.tasks.length - done}</strong></span></div><div><Flame/><span>Привычки<strong>{habitsDone}/{data.habits.length}</strong></span></div><div><Target/><span>Средний прогресс<strong>{weekGoals.length ? Math.round(weekGoals.reduce((s,g)=>s+g.progress,0)/weekGoals.length) : 0}%</strong></span></div></div>
    <div className="dashboard-grid">
      <Panel title="План на сегодня" subtitle="Фокус без спешки" action={<Link to="/tasks">Все задачи <ArrowUpRight size={15}/></Link>} className="span-2">
        <div className="list">{todayTasks.length ? todayTasks.slice(0,4).map(task => <div className={`list-row ${task.completed ? 'complete' : ''}`} key={task.id}>{task.completed ? <CheckCircle2/> : <Circle/>}<div><strong>{task.title}</strong><span className={`priority ${task.priority}`}>{task.priority === 'high' ? 'высокий' : task.priority === 'low' ? 'низкий' : 'средний'}</span></div></div>) : <Empty text="На сегодня задач нет"/>}</div>
      </Panel>
      <Panel title="Цели недели" action={<Link to="/tasks"><ArrowUpRight size={16}/></Link>}><div className="goal-list">{weekGoals.length ? weekGoals.map(goal => <div key={goal.id}><div><span>{goal.title}</span><b>{goal.progress}%</b></div><progress value={goal.progress} max="100"/></div>) : <Empty text="Добавьте первую цель"/>}</div></Panel>
      <Panel title="Ближайшие события" action={<Link to="/calendar"><CalendarDays size={17}/></Link>}><div className="mini-list">{events.length ? events.map(item => <div key={item.id}><i style={{background:item.color}}/><div><strong>{item.title}</strong><span>{formatDateTime(item.starts_at)}</span></div></div>) : <Empty text="Событий пока нет"/>}</div></Panel>
      <Panel title="Напоминания" action={<Link to="/reminders"><Clock3 size={17}/></Link>}><div className="mini-list">{reminders.length ? reminders.map(item => <div key={item.id}><i className="coral"/><div><strong>{item.title}</strong><span>{formatDateTime(item.remind_at)}</span></div></div>) : <Empty text="Всё спокойно"/>}</div></Panel>
      <Panel title="Сегодня в расписании" subtitle="Первая и вторая недели" action={<Link to="/schedule"><ArrowUpRight size={16}/></Link>} className="span-2"><div className="schedule-strip">{todaySchedule.length ? todaySchedule.map(item => <div key={item.id}><time>{item.starts_at.slice(0,5)} · неделя {item.week_number}</time><strong>{item.title}</strong><span>{item.location || 'Без аудитории'}</span></div>) : <Empty text="В расписании на сегодня свободно"/>}</div></Panel>
    </div>
  </div>
}
