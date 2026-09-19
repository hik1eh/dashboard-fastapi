import { AlertTriangle, LoaderCircle, Plus, X } from 'lucide-react'
import { useEffect, useState, type FormEvent, type ReactNode } from 'react'
import { useData } from '../lib/DataContext'

export function PageHeader({ eyebrow, title, description, action }: { eyebrow: string; title: string; description: string; action?: () => void }) {
  return <header className="page-header"><div><span className="eyebrow">{eyebrow}</span><h1>{title}</h1><p>{description}</p></div>{action && <button className="primary" onClick={action}><Plus size={18}/> Добавить</button>}</header>
}
export function Panel({ title, subtitle, action, children, className = '' }: { title?: string; subtitle?: string; action?: ReactNode; children: ReactNode; className?: string }) {
  return <section className={`panel ${className}`}><div className="panel-head"><div>{title && <h2>{title}</h2>}{subtitle && <p>{subtitle}</p>}</div>{action}</div>{children}</section>
}
export function Empty({ text }: { text: string }) { return <div className="empty"><span>✦</span><p>{text}</p></div> }
export function Loading() { return <div className="loading"><LoaderCircle className="spin"/><span>Собираем ваш день…</span></div> }
export function AppFeedback() { const { error, notice } = useData(); return <div className="toast-stack">{error && <div className="toast error"><AlertTriangle size={17}/>{error}</div>}{notice && <div className="toast success">✓ {notice}</div>}</div> }

export function Modal({ open, title, children, onClose }: { open: boolean; title: string; children: ReactNode; onClose: () => void }) {
  useEffect(() => { if (!open) return; const close = (event: KeyboardEvent) => event.key === 'Escape' && onClose(); window.addEventListener('keydown', close); return () => window.removeEventListener('keydown', close) }, [open, onClose])
  if (!open) return null
  return <div className="modal-backdrop" onMouseDown={(e) => e.target === e.currentTarget && onClose()}><div className="modal" role="dialog" aria-modal="true"><div className="modal-title"><h2>{title}</h2><button className="icon" onClick={onClose} aria-label="Закрыть"><X/></button></div>{children}</div></div>
}

export function FormModal({ open, title, onClose, onSubmit, children }: { open: boolean; title: string; onClose: () => void; onSubmit: () => Promise<boolean>; children: ReactNode }) {
  const [saving, setSaving] = useState(false)
  async function submit(event: FormEvent) { event.preventDefault(); setSaving(true); const ok = await onSubmit(); setSaving(false); if (ok) onClose() }
  return <Modal open={open} title={title} onClose={onClose}><form onSubmit={submit}>{children}<div className="modal-actions"><button type="button" className="ghost" onClick={onClose}>Отмена</button><button className="primary" disabled={saving}>{saving ? <LoaderCircle className="spin" size={18}/> : null}{saving ? 'Сохраняем' : 'Сохранить'}</button></div></form></Modal>
}

export function ConfirmModal({ open, name, onClose, onConfirm }: { open: boolean; name: string; onClose: () => void; onConfirm: () => Promise<boolean> }) {
  const [saving, setSaving] = useState(false)
  return <Modal open={open} title="Удалить запись?" onClose={onClose}><p className="confirm-text">«{name}» исчезнет без возможности восстановления.</p><div className="modal-actions"><button className="ghost" onClick={onClose}>Оставить</button><button className="danger" disabled={saving} onClick={async () => { setSaving(true); if (await onConfirm()) onClose(); setSaving(false) }}>Удалить</button></div></Modal>
}
