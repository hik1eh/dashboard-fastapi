import { Navigate, Route, Routes } from 'react-router-dom'
import { AppLayout } from './layout/AppLayout'
import { CalendarPage } from './pages/CalendarPage'
import { DashboardPage } from './pages/DashboardPage'
import { HabitsPage, NotesPage, PlansPage, RemindersPage, SchedulePage, SettingsPage } from './pages/CollectionPages'
import { TasksGoalsPage } from './pages/TasksGoalsPage'
import { AuthPage } from './pages/AuthPage'
import { useAuth } from './lib/AuthContext'
import { DataProvider } from './lib/DataContext'

function ProtectedLayout(){const{user,loading}=useAuth();if(loading)return <div className="loading">Загрузка…</div>;if(!user)return <Navigate to="/auth" replace/>;return <DataProvider><AppLayout/></DataProvider>}

export default function App(){return <Routes><Route path="auth" element={<AuthPage/>}/><Route element={<ProtectedLayout/>}><Route index element={<DashboardPage/>}/><Route path="tasks" element={<TasksGoalsPage/>}/><Route path="calendar" element={<CalendarPage/>}/><Route path="reminders" element={<RemindersPage/>}/><Route path="schedule" element={<SchedulePage/>}/><Route path="habits" element={<HabitsPage/>}/><Route path="plans" element={<PlansPage/>}/><Route path="notes" element={<NotesPage/>}/><Route path="settings" element={<SettingsPage/>}/><Route path="*" element={<Navigate to="/" replace/>}/></Route></Routes>}
