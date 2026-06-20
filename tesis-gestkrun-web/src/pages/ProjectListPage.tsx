import { useNavigate } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { listProjects, deleteProject } from '../features/projects/projectService'

export default function ProjectListPage() {
  const navigate = useNavigate()
  const queryClient = useQueryClient()

  const { data: projects = [], isLoading } = useQuery({
    queryKey: ['projects'],
    queryFn: listProjects,
  })

  const deleteMutation = useMutation({
    mutationFn: deleteProject,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['projects'] }),
  })

  if (isLoading) return <div className="text-gray-500">Cargando proyectos...</div>

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-2xl font-bold">Proyectos</h2>
        <button
          onClick={() => navigate('/projects/new')}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Nuevo proyecto
        </button>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full border-collapse">
          <thead>
            <tr className="bg-gray-100 text-left">
              <th className="px-4 py-2 border-b">Nombre</th>
              <th className="px-4 py-2 border-b">Estado</th>
              <th className="px-4 py-2 border-b">Descripción</th>
              <th className="px-4 py-2 border-b">Acciones</th>
            </tr>
          </thead>
          <tbody>
            {projects.length === 0 && (
              <tr>
                <td colSpan={4} className="px-4 py-8 text-center text-gray-500">
                  No hay proyectos creados
                </td>
              </tr>
            )}
            {projects.map((project) => (
              <tr key={project.id} className="hover:bg-gray-50 border-b">
                <td className="px-4 py-3">{project.nombre}</td>
                <td className="px-4 py-3">
                  <span className={`px-2 py-1 rounded text-xs font-medium ${
                    project.estado === 'ACTIVO' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-600'
                  }`}>
                    {project.estado}
                  </span>
                </td>
                <td className="px-4 py-3 text-gray-600 max-w-xs truncate">{project.descripcion}</td>
                <td className="px-4 py-3 space-x-2">
                  <button
                    onClick={() => navigate(`/projects/${project.id}`)}
                    className="text-blue-600 hover:underline text-sm"
                  >
                    Ver
                  </button>
                  <button
                    onClick={() => { if (confirm('¿Eliminar proyecto?')) deleteMutation.mutate(project.id) }}
                    className="text-red-600 hover:underline text-sm"
                  >
                    Eliminar
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
