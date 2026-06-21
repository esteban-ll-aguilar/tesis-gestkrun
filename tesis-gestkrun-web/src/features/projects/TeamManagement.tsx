import { useState, useCallback, useRef, useEffect } from 'react'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { assignTeam, removeAssignment, type AssignmentDTO } from './projectService'
import { useAuthStore } from '../../stores/auth'
import http from '../../services/http'

interface Props {
  projectId: string
  assignments: AssignmentDTO[]
}

interface UserOption {
  id: string
  nombre: string
  email: string
  rol: string
}

export default function TeamManagement({ projectId, assignments }: Props) {
  const queryClient = useQueryClient()
  const hasRole = useAuthStore((s) => s.hasRole)
  const [search, setSearch] = useState('')
  const [results, setResults] = useState<UserOption[]>([])
  const [selected, setSelected] = useState<UserOption | null>(null)
  const [rol, setRol] = useState<string>('DEVELOPER')
  const [open, setOpen] = useState(false)
  const ref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false)
    }
    document.addEventListener('mousedown', handler)
    return () => document.removeEventListener('mousedown', handler)
  }, [])

  const searchUsers = useCallback(async (q: string) => {
    if (q.length < 2) { setResults([]); return }
    try {
      const { data } = await http.get(`/users?search=${encodeURIComponent(q)}`)
      setResults(data)
      setOpen(true)
    } catch { setResults([]) }
  }, [])

  const mutation = useMutation({
    mutationFn: () => assignTeam(projectId, selected!.id, rol),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['assignments', projectId] })
      setSelected(null)
      setSearch('')
      setResults([])
    },
  })

  const removeMutation = useMutation({
    mutationFn: (userId: string) => removeAssignment(projectId, userId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['assignments', projectId] })
    },
  })

  return (
    <div>
      <h3 className="font-medium mb-3">Miembros del equipo</h3>

      {hasRole('PRODUCT_OWNER') && (
        <div className="mb-4 p-3 border rounded bg-gray-50 space-y-2" ref={ref}>
          <div className="relative">
            <input
              value={selected ? `${selected.nombre} (${selected.email})` : search}
              onChange={e => { setSearch(e.target.value); setSelected(null); searchUsers(e.target.value) }}
              onFocus={() => { if (results.length) setOpen(true) }}
              placeholder="Buscar usuario por nombre o email..."
              className="w-full border rounded px-3 py-1.5 text-sm"
            />
            {open && results.length > 0 && (
              <ul className="absolute z-10 w-full mt-1 bg-white border rounded shadow-lg max-h-40 overflow-y-auto">
                {results.filter(u => !assignments.some(a => a.user_id === u.id)).map(u => (
                  <li key={u.id} onClick={() => { setSelected(u); setSearch(''); setResults([]); setOpen(false) }} className="px-3 py-2 text-sm hover:bg-blue-50 cursor-pointer">
                    <span className="font-medium">{u.nombre}</span>
                    <span className="text-gray-500 ml-2">{u.email}</span>
                    <span className="text-xs text-gray-400 ml-2">{u.rol}</span>
                  </li>
                ))}
              </ul>
            )}
          </div>
          <select
            value={rol} onChange={e => setRol(e.target.value)}
            className="w-full border rounded px-3 py-1.5 text-sm"
          >
            <option value="DEVELOPER">Developer</option>
            <option value="SCRUM_MASTER">Scrum Master</option>
          </select>
          <button
            onClick={() => mutation.mutate()}
            disabled={!selected}
            className="bg-blue-600 text-white px-3 py-1.5 rounded text-sm hover:bg-blue-700 disabled:opacity-50"
          >
            Asignar
          </button>
        </div>
      )}

      <ul className="space-y-2">
        <li className="flex items-center justify-between p-2 border rounded bg-yellow-50">
          <div>
            <span className="text-sm font-medium">Propietario del proyecto</span>
            <span className="text-xs text-gray-500 ml-2">(owner)</span>
          </div>
          <span className="ml-2 text-xs px-2 py-0.5 rounded bg-green-100 text-green-700">
            PRODUCT_OWNER
          </span>
        </li>
        {assignments.map((a) => (
          <li key={a.id} className="flex items-center justify-between p-2 border rounded">
            <div>
              <span className="text-sm">{a.nombre || a.user_id}</span>
              <span className={`ml-2 text-xs px-2 py-0.5 rounded ${
                a.rol === 'SCRUM_MASTER' ? 'bg-purple-100 text-purple-700' :
                a.rol === 'PRODUCT_OWNER' ? 'bg-green-100 text-green-700' :
                'bg-blue-100 text-blue-700'
              }`}>
                {a.rol}
              </span>
            </div>
            {hasRole('PRODUCT_OWNER') && (
              <button onClick={() => removeMutation.mutate(a.user_id)} className="text-red-600 text-xs hover:underline ml-2">
                Quitar
              </button>
            )}
          </li>
        ))}
      </ul>
      {assignments.length === 0 && (
        <p className="text-gray-500 text-sm mt-2">Sin miembros adicionales asignados</p>
      )}
    </div>
  )
}
