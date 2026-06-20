import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import http from '../../services/http'

interface ModuleDTO {
  id: string
  nombre: string
  descripcion?: string
  estado: string
}

async function listModules(projectId: string): Promise<ModuleDTO[]> {
  const { data } = await http.get(`/projects/${projectId}/modules`)
  return data
}

async function createModule(projectId: string, nombre: string, descripcion: string): Promise<ModuleDTO> {
  const { data } = await http.post(`/projects/${projectId}/modules`, { nombre, descripcion })
  return data
}

async function deleteModule(projectId: string, moduleId: string): Promise<void> {
  await http.delete(`/projects/${projectId}/modules/${moduleId}`)
}

export default function ModuleList({ projectId }: { projectId: string }) {
  const queryClient = useQueryClient()
  const [nombre, setNombre] = useState('')
  const [descripcion, setDescripcion] = useState('')
  const [showForm, setShowForm] = useState(false)

  const { data: modules = [] } = useQuery({
    queryKey: ['modules', projectId],
    queryFn: () => listModules(projectId),
  })

  const createMutation = useMutation({
    mutationFn: () => createModule(projectId, nombre, descripcion),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['modules', projectId] })
      setNombre(''); setDescripcion(''); setShowForm(false)
    },
  })

  const deleteMutation = useMutation({
    mutationFn: (moduleId: string) => deleteModule(projectId, moduleId),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['modules', projectId] }),
  })

  return (
    <div>
      <div className="flex items-center justify-between mb-3">
        <h3 className="font-medium">Módulos</h3>
        <button
          onClick={() => setShowForm(!showForm)}
          className="text-sm text-blue-600 hover:underline"
        >
          {showForm ? 'Cancelar' : 'Añadir módulo'}
        </button>
      </div>

      {showForm && (
        <div className="mb-4 p-3 border rounded bg-gray-50 space-y-2">
          <input
            value={nombre} onChange={e => setNombre(e.target.value)}
            placeholder="Nombre del módulo"
            className="w-full border rounded px-3 py-1.5 text-sm"
          />
          <input
            value={descripcion} onChange={e => setDescripcion(e.target.value)}
            placeholder="Descripción (opcional)"
            className="w-full border rounded px-3 py-1.5 text-sm"
          />
          <button
            onClick={() => createMutation.mutate()}
            disabled={!nombre}
            className="bg-blue-600 text-white px-3 py-1.5 rounded text-sm hover:bg-blue-700 disabled:opacity-50"
          >
            Crear
          </button>
        </div>
      )}

      {modules.length === 0 ? (
        <p className="text-gray-500 text-sm">Sin módulos</p>
      ) : (
        <ul className="space-y-2">
          {modules.map((m) => (
            <li key={m.id} className="flex items-center justify-between p-2 border rounded">
              <div>
                <span className="font-medium text-sm">{m.nombre}</span>
                <span className="text-xs text-gray-500 ml-2">{m.estado}</span>
              </div>
              <button
                onClick={() => deleteMutation.mutate(m.id)}
                className="text-red-600 text-xs hover:underline"
              >
                Eliminar
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
