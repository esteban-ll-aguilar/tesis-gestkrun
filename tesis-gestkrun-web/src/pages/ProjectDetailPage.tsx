import { useState } from 'react'
import { useParams } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { getProject, listAssignments, updateProject } from '../features/projects/projectService'
import TeamManagement from '../features/projects/TeamManagement'
import { useAuthStore } from '../stores/auth'
import BacklogPage from './BacklogPage'
import SprintListPage from './SprintListPage'
import ProjectBoardPage from './ProjectBoardPage'
import TasksPage from './TasksPage'
import ChatPage from './ChatPage'

type MainTab = 'info' | 'board' | 'backlog' | 'sprints' | 'tasks' | 'chat'

const TABS: { key: MainTab; label: string }[] = [
  { key: 'info', label: 'Información' },
  { key: 'board', label: 'Tablero' },
  { key: 'backlog', label: 'Backlog' },
  { key: 'sprints', label: 'Sprints' },
  { key: 'tasks', label: 'Tareas' },
  { key: 'chat', label: 'Chat' },
]

export default function ProjectDetailPage() {
  const { id } = useParams<{ id: string }>()
  const queryClient = useQueryClient()
  const hasRole = useAuthStore((s) => s.hasRole)
  const [tab, setTab] = useState<MainTab>('info')
  const [subTab, setSubTab] = useState<'info' | 'team'>('info')
  const [editing, setEditing] = useState(false)
  const [editNombre, setEditNombre] = useState('')
  const [editDesc, setEditDesc] = useState('')

  const { data: project, isLoading } = useQuery({
    queryKey: ['project', id],
    queryFn: () => getProject(id!),
    enabled: !!id,
  })

  const { data: assignments = [] } = useQuery({
    queryKey: ['assignments', id],
    queryFn: () => listAssignments(id!),
    enabled: !!id,
  })

  const updateMutation = useMutation({
    mutationFn: (data: { nombre?: string; descripcion?: string }) => updateProject(id!, data),
    onSuccess: () => { queryClient.invalidateQueries({ queryKey: ['project', id] }); setEditing(false) },
  })

  const startEditing = () => {
    setEditNombre(project?.nombre || '')
    setEditDesc(project?.descripcion || '')
    setEditing(true)
  }

  if (isLoading || !project) {
    return <div className="text-gray-500">Cargando proyecto...</div>
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-1">
        <h2 className="text-2xl font-bold">{project.nombre}</h2>
        {hasRole('PRODUCT_OWNER') && !editing && (
          <button onClick={startEditing} className="text-sm text-blue-600 hover:underline">Editar</button>
        )}
      </div>
      <p className="text-gray-500 text-sm mb-4">Estado: {project.estado}</p>

      <nav className="flex gap-1 mb-6 border-b overflow-x-auto">
        {TABS.map(t => (
          <button
            key={t.key}
            onClick={() => setTab(t.key)}
            className={`px-4 py-2 text-sm font-medium border-b-2 transition-colors whitespace-nowrap ${
              tab === t.key ? 'border-blue-600 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700'
            }`}
          >
            {t.label}
          </button>
        ))}
      </nav>

      {tab === 'info' && (
        <>
          <div className="flex gap-1 mb-6 border-b">
            {(['info', 'team'] as const).map(t => (
              <button key={t} onClick={() => setSubTab(t)}
                className={`px-3 py-1.5 text-xs font-medium border-b-2 transition-colors ${
                  subTab === t ? 'border-blue-600 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700'
                }`}
              >
                {t === 'info' ? 'Detalles' : 'Equipo'}
              </button>
            ))}
          </div>

          {subTab === 'info' && (
            <div className="space-y-3">
              {editing ? (
                <div className="border rounded p-4 bg-gray-50 space-y-3">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Nombre</label>
                    <input value={editNombre} onChange={e => setEditNombre(e.target.value)} className="w-full p-2 border rounded text-sm" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Descripción</label>
                    <textarea value={editDesc} onChange={e => setEditDesc(e.target.value)} className="w-full p-2 border rounded text-sm" rows={3} />
                  </div>
                  <div className="flex gap-2">
                    <button onClick={() => updateMutation.mutate({ nombre: editNombre, descripcion: editDesc })} disabled={!editNombre} className="bg-blue-600 text-white px-4 py-2 rounded text-sm hover:bg-blue-700 disabled:opacity-50">Guardar</button>
                    <button onClick={() => setEditing(false)} className="px-4 py-2 rounded text-sm border hover:bg-gray-100">Cancelar</button>
                  </div>
                </div>
              ) : (
                <>
                  <div>
                    <h3 className="font-medium text-gray-700">Descripción</h3>
                    <p className="text-gray-600">{project.descripcion || 'Sin descripción'}</p>
                  </div>
                  <div>
                    <h3 className="font-medium text-gray-700">Equipo ({assignments.length} miembros)</h3>
                    <ul className="text-gray-600 text-sm">
                      {assignments.map(a => <li key={a.id}>{a.nombre || a.user_id} — {a.rol}</li>)}
                    </ul>
                  </div>
                </>
              )}
            </div>
          )}
          {subTab === 'team' && <TeamManagement projectId={id!} assignments={assignments} />}
        </>
      )}

      {tab === 'board' && <ProjectBoardPage />}
      {tab === 'backlog' && <BacklogPage />}
      {tab === 'sprints' && <SprintListPage />}
      {tab === 'tasks' && <TasksPage />}
      {tab === 'chat' && <ChatPage />}
    </div>
  )
}
