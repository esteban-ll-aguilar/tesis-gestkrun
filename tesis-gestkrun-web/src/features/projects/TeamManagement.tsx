import { useState } from 'react'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { assignTeam, type AssignmentDTO } from './projectService'

interface Props {
  projectId: string
  assignments: AssignmentDTO[]
}

export default function TeamManagement({ projectId, assignments }: Props) {
  const queryClient = useQueryClient()
  const [userId, setUserId] = useState('')
  const [rol, setRol] = useState<'SCRUM_MASTER' | 'DEVELOPER'>('DEVELOPER')

  const mutation = useMutation({
    mutationFn: () => assignTeam(projectId, userId, rol),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['assignments', projectId] })
      setUserId('')
    },
  })

  return (
    <div>
      <h3 className="font-medium mb-3">Miembros del equipo</h3>

      <div className="mb-4 p-3 border rounded bg-gray-50 space-y-2">
        <input
          value={userId} onChange={e => setUserId(e.target.value)}
          placeholder="ID del usuario"
          className="w-full border rounded px-3 py-1.5 text-sm"
        />
        <select
          value={rol} onChange={e => setRol(e.target.value as 'SCRUM_MASTER' | 'DEVELOPER')}
          className="w-full border rounded px-3 py-1.5 text-sm"
        >
          <option value="DEVELOPER">Developer</option>
          <option value="SCRUM_MASTER">Scrum Master</option>
        </select>
        <button
          onClick={() => mutation.mutate()}
          disabled={!userId}
          className="bg-blue-600 text-white px-3 py-1.5 rounded text-sm hover:bg-blue-700 disabled:opacity-50"
        >
          Asignar
        </button>
      </div>

      {assignments.length === 0 ? (
        <p className="text-gray-500 text-sm">Sin miembros asignados</p>
      ) : (
        <ul className="space-y-2">
          {assignments.map((a) => (
            <li key={a.id} className="flex items-center justify-between p-2 border rounded">
              <div>
                <span className="text-sm">{a.nombre || a.user_id}</span>
                <span className={`ml-2 text-xs px-2 py-0.5 rounded ${
                  a.rol === 'SCRUM_MASTER' ? 'bg-purple-100 text-purple-700' : 'bg-blue-100 text-blue-700'
                }`}>
                  {a.rol}
                </span>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
