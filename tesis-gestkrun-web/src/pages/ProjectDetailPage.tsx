import { useState } from 'react'
import { useParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { getProject, listAssignments } from '../features/projects/projectService'
import TeamManagement from '../features/projects/TeamManagement'
import ModuleList from '../features/projects/ModuleList'

export default function ProjectDetailPage() {
  const { id } = useParams<{ id: string }>()
  const [tab, setTab] = useState<'info' | 'modules' | 'team'>('info')

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

  if (isLoading || !project) {
    return <div className="text-gray-500">Cargando proyecto...</div>
  }

  const tabs = [
    { key: 'info' as const, label: 'Información' },
    { key: 'modules' as const, label: 'Módulos' },
    { key: 'team' as const, label: 'Equipo' },
  ]

  return (
    <div>
      <h2 className="text-2xl font-bold mb-1">{project.nombre}</h2>
      <p className="text-gray-500 text-sm mb-4">Estado: {project.estado}</p>

      <div className="flex gap-1 mb-6 border-b">
        {tabs.map((t) => (
          <button
            key={t.key}
            onClick={() => setTab(t.key)}
            className={`px-4 py-2 text-sm font-medium border-b-2 transition-colors ${
              tab === t.key
                ? 'border-blue-600 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700'
            }`}
          >
            {t.label}
          </button>
        ))}
      </div>

      {tab === 'info' && (
        <div className="space-y-3">
          <div>
            <h3 className="font-medium text-gray-700">Descripción</h3>
            <p className="text-gray-600">{project.descripcion || 'Sin descripción'}</p>
          </div>
          <div>
            <h3 className="font-medium text-gray-700">Equipo ({assignments.length} miembros)</h3>
            <ul className="text-gray-600">
              {assignments.map((a) => (
                <li key={a.id}>{a.nombre || a.user_id} — {a.rol}</li>
              ))}
            </ul>
          </div>
        </div>
      )}

      {tab === 'modules' && <ModuleList projectId={id!} />}

      {tab === 'team' && <TeamManagement projectId={id!} assignments={assignments} />}
    </div>
  )
}
