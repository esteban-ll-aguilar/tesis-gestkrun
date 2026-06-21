import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import http from '../services/http'

interface UserDTO {
  id: string
  nombre: string
  email: string
  rol: string
  fechaRegistro: string
}

export default function UserManagementPage() {
  const queryClient = useQueryClient()
  const [search, setSearch] = useState('')
  const [editingId, setEditingId] = useState<string | null>(null)
  const [editRol, setEditRol] = useState('')

  const { data: users = [], isLoading } = useQuery({
    queryKey: ['users', search],
    queryFn: () => http.get(`/users?search=${encodeURIComponent(search)}`).then(r => r.data as UserDTO[]),
  })

  const updateRolMutation = useMutation({
    mutationFn: ({ userId, rol }: { userId: string; rol: string }) =>
      http.patch(`/users/${userId}/rol`, { rol }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] })
      setEditingId(null)
    },
  })

  const startEdit = (u: UserDTO) => {
    setEditingId(u.id)
    setEditRol(u.rol)
  }

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Usuarios</h2>

      <div className="mb-4">
        <input
          value={search} onChange={e => setSearch(e.target.value)}
          placeholder="Buscar por nombre o email..."
          className="w-full max-w-md border rounded px-3 py-2 text-sm"
        />
      </div>

      {isLoading ? (
        <p className="text-gray-500">Cargando...</p>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full border-collapse">
            <thead>
              <tr className="bg-gray-100 text-left">
                <th className="px-4 py-2 border-b text-sm">Nombre</th>
                <th className="px-4 py-2 border-b text-sm">Email</th>
                <th className="px-4 py-2 border-b text-sm">Rol</th>
                <th className="px-4 py-2 border-b text-sm">Registro</th>
                <th className="px-4 py-2 border-b text-sm">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {users.map(u => (
                <tr key={u.id} className="hover:bg-gray-50 border-b">
                  <td className="px-4 py-3 text-sm">{u.nombre}</td>
                  <td className="px-4 py-3 text-sm text-gray-600">{u.email}</td>
                  <td className="px-4 py-3 text-sm">
                    {editingId === u.id ? (
                      <select value={editRol} onChange={e => setEditRol(e.target.value)} className="border rounded px-2 py-1 text-sm">
                        <option value="ADMIN">ADMIN</option>
                        <option value="PRODUCT_OWNER">PRODUCT_OWNER</option>
                        <option value="SCRUM_MASTER">SCRUM_MASTER</option>
                        <option value="DEVELOPER">DEVELOPER</option>
                      </select>
                    ) : (
                      <span className={`px-2 py-1 rounded text-xs font-medium ${
                        u.rol === 'ADMIN' ? 'bg-red-100 text-red-700' :
                        u.rol === 'PRODUCT_OWNER' ? 'bg-green-100 text-green-700' :
                        u.rol === 'SCRUM_MASTER' ? 'bg-purple-100 text-purple-700' :
                        'bg-blue-100 text-blue-700'
                      }`}>{u.rol}</span>
                    )}
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-500">{new Date(u.fechaRegistro).toLocaleDateString()}</td>
                  <td className="px-4 py-3 text-sm">
                    {editingId === u.id ? (
                      <div className="flex gap-2">
                        <button onClick={() => updateRolMutation.mutate({ userId: u.id, rol: editRol })} className="text-blue-600 hover:underline text-xs">Guardar</button>
                        <button onClick={() => setEditingId(null)} className="text-gray-500 hover:underline text-xs">Cancelar</button>
                      </div>
                    ) : (
                      <button onClick={() => startEdit(u)} className="text-blue-600 hover:underline text-xs">Cambiar rol</button>
                    )}
                  </td>
                </tr>
              ))}
              {users.length === 0 && (
                <tr>
                  <td colSpan={5} className="px-4 py-8 text-center text-gray-500">No se encontraron usuarios</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
