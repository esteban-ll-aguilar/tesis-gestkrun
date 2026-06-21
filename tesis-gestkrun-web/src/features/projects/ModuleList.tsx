import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { projectService } from './projectService'
import http from '../../services/http'

interface ModuleDTO {
  id: string
  nombre: string
  descripcion?: string
  estado: string
}

interface ModuleDevDTO {
  id: string
  module_id: string
  user_id: string
}

async function listModules(projectId: string): Promise<ModuleDTO[]> {
  const { data } = await http.get(`/projects/${projectId}/modules`)
  return data
}

async function createModule(projectId: string, nombre: string, descripcion: string): Promise<ModuleDTO> {
  const { data } = await http.post(`/projects/${projectId}/modules`, { nombre, descripcion })
  return data
}

async function updateModule(projectId: string, moduleId: string, payload: { nombre?: string; descripcion?: string }): Promise<ModuleDTO> {
  const { data } = await http.patch(`/projects/${projectId}/modules/${moduleId}`, payload)
  return data
}

async function deleteModule(projectId: string, moduleId: string): Promise<void> {
  await http.delete(`/projects/${projectId}/modules/${moduleId}`)
}

async function listModuleDevs(projectId: string, moduleId: string): Promise<ModuleDevDTO[]> {
  const { data } = await http.get(`/projects/${projectId}/modules/${moduleId}/developers`)
  return data
}

async function addModuleDev(projectId: string, moduleId: string, userId: string): Promise<void> {
  await http.post(`/projects/${projectId}/modules/${moduleId}/developers`, { user_id: userId })
}

async function removeModuleDev(projectId: string, moduleId: string, userId: string): Promise<void> {
  await http.delete(`/projects/${projectId}/modules/${moduleId}/developers/${userId}`)
}

export default function ModuleList({ projectId }: { projectId: string }) {
  const queryClient = useQueryClient()
  const [nombre, setNombre] = useState('')
  const [descripcion, setDescripcion] = useState('')
  const [showForm, setShowForm] = useState(false)
  const [editingId, setEditingId] = useState<string | null>(null)
  const [editNombre, setEditNombre] = useState('')
  const [editDesc, setEditDesc] = useState('')
  const [showDevs, setShowDevs] = useState<Set<string>>(new Set())

  const { data: modules = [] } = useQuery({
    queryKey: ['modules', projectId],
    queryFn: () => listModules(projectId),
  })

  const { data: assignments = [] } = useQuery({
    queryKey: ['assignments', projectId],
    queryFn: () => projectService.listAssignments(projectId),
  })

  const createMutation = useMutation({
    mutationFn: () => createModule(projectId, nombre, descripcion),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['modules', projectId] })
      setNombre(''); setDescripcion(''); setShowForm(false)
    },
  })

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: string; data: { nombre?: string; descripcion?: string } }) => updateModule(projectId, id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['modules', projectId] })
      setEditingId(null)
    },
  })

  const deleteMutation = useMutation({
    mutationFn: (moduleId: string) => deleteModule(projectId, moduleId),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['modules', projectId] }),
  })

  const startEdit = (m: ModuleDTO) => {
    setEditingId(m.id)
    setEditNombre(m.nombre)
    setEditDesc(m.descripcion || '')
  }

  const toggleDevs = (moduleId: string) => {
    const next = new Set(showDevs)
    if (next.has(moduleId)) next.delete(moduleId)
    else next.add(moduleId)
    setShowDevs(next)
  }

  const developers = assignments.filter(a => a.rol === 'DEVELOPER')

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
          <input value={nombre} onChange={e => setNombre(e.target.value)} placeholder="Nombre del módulo" className="w-full border rounded px-3 py-1.5 text-sm" />
          <input value={descripcion} onChange={e => setDescripcion(e.target.value)} placeholder="Descripción (opcional)" className="w-full border rounded px-3 py-1.5 text-sm" />
          <button onClick={() => createMutation.mutate()} disabled={!nombre} className="bg-blue-600 text-white px-3 py-1.5 rounded text-sm hover:bg-blue-700 disabled:opacity-50">Crear</button>
        </div>
      )}

      {modules.length === 0 ? (
        <p className="text-gray-500 text-sm">Sin módulos</p>
      ) : (
        <ul className="space-y-2">
          {modules.map((m) => (
            <ModuleItem
              key={m.id}
              module={m}
              projectId={projectId}
              developers={developers}
              assignments={assignments}
              editingId={editingId}
              editNombre={editNombre}
              editDesc={editDesc}
              showDevs={showDevs.has(m.id)}
              onStartEdit={() => startEdit(m)}
              onEditNombre={setEditNombre}
              onEditDesc={setEditDesc}
              onSaveEdit={() => updateMutation.mutate({ id: m.id, data: { nombre: editNombre, descripcion: editDesc } })}
              onCancelEdit={() => setEditingId(null)}
              onDelete={() => deleteMutation.mutate(m.id)}
              onToggleDevs={() => toggleDevs(m.id)}
            />
          ))}
        </ul>
      )}
    </div>
  )
}

function ModuleItem({ module: m, projectId, developers, assignments, editingId, editNombre, editDesc, showDevs, onStartEdit, onEditNombre, onEditDesc, onSaveEdit, onCancelEdit, onDelete, onToggleDevs }: {
  module: ModuleDTO; projectId: string; developers: { user_id: string; nombre?: string; email?: string }[];
  assignments: { user_id: string; nombre?: string; email?: string; rol: string }[];
  editingId: string | null; editNombre: string; editDesc: string; showDevs: boolean;
  onStartEdit: () => void; onEditNombre: (v: string) => void; onEditDesc: (v: string) => void;
  onSaveEdit: () => void; onCancelEdit: () => void; onDelete: () => void; onToggleDevs: () => void;
}) {
  const queryClient = useQueryClient()

  const { data: devs = [] } = useQuery({
    queryKey: ['module-devs', m.id],
    queryFn: () => listModuleDevs(projectId, m.id),
    enabled: showDevs,
  })

  const addDevMutation = useMutation({
    mutationFn: (userId: string) => addModuleDev(projectId, m.id, userId),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['module-devs', m.id] }),
  })

  const removeDevMutation = useMutation({
    mutationFn: (userId: string) => removeModuleDev(projectId, m.id, userId),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['module-devs', m.id] }),
  })

  const assignedDevIds = new Set(devs.map(d => d.user_id))
  const availableDevs = developers.filter(d => !assignedDevIds.has(d.user_id))

  return (
    <li className="border rounded">
      <div className="flex items-center justify-between p-2">
        {editingId === m.id ? (
          <div className="flex-1 space-y-2">
            <input value={editNombre} onChange={e => onEditNombre(e.target.value)} className="w-full p-1.5 border rounded text-sm" />
            <input value={editDesc} onChange={e => onEditDesc(e.target.value)} className="w-full p-1.5 border rounded text-sm" placeholder="Descripción" />
            <div className="flex gap-2">
              <button onClick={onSaveEdit} disabled={!editNombre} className="text-xs text-blue-600 hover:underline">Guardar</button>
              <button onClick={onCancelEdit} className="text-xs text-gray-500 hover:underline">Cancelar</button>
            </div>
          </div>
        ) : (
          <>
            <div className="flex-1">
              <div className="flex items-center gap-2">
                <button onClick={onToggleDevs} className="text-xs text-gray-400 hover:text-gray-600">
                  {showDevs ? '▾' : '▸'}
                </button>
                <span className="font-medium text-sm cursor-pointer" onClick={onToggleDevs}>{m.nombre}</span>
                <span className="text-xs text-gray-500">{m.estado}</span>
              </div>
              {m.descripcion && <p className="text-xs text-gray-400 ml-5">{m.descripcion}</p>}
            </div>
            <div className="flex gap-2">
              <button onClick={onStartEdit} className="text-blue-600 text-xs hover:underline">Editar</button>
              <button onClick={onDelete} className="text-red-600 text-xs hover:underline">Eliminar</button>
            </div>
          </>
        )}
      </div>
      {showDevs && (
        <div className="px-4 pb-2 border-t bg-gray-50">
          <p className="text-xs text-gray-500 font-medium mt-2 mb-1">Desarrolladores asignados:</p>
          {devs.length === 0 && <p className="text-xs text-gray-400 mb-1">Ninguno</p>}
          {devs.map(d => {
            const user = assignments.find(a => a.user_id === d.user_id)
            return (
              <div key={d.user_id} className="flex items-center justify-between text-xs text-gray-600 py-0.5">
                <span>{user?.nombre || d.user_id.slice(0, 8)}</span>
                <button onClick={() => removeDevMutation.mutate(d.user_id)} className="text-red-500 hover:underline">Quitar</button>
              </div>
            )
          })}
          {availableDevs.length > 0 && (
            <div className="flex gap-1 mt-1">
              <select
                onChange={e => { if (e.target.value) addDevMutation.mutate(e.target.value) }}
                className="flex-1 p-1 border rounded text-xs"
                defaultValue=""
              >
                <option value="" disabled>Añadir developer...</option>
                {availableDevs.map(d => (
                  <option key={d.user_id} value={d.user_id}>{d.nombre || d.email}</option>
                ))}
              </select>
            </div>
          )}
        </div>
      )}
    </li>
  )
}
