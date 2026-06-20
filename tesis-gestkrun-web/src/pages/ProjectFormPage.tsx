import { useForm } from 'react-hook-form'
import { useNavigate, useParams } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { z } from 'zod'
import { getProject, createProject, updateProject } from '../features/projects/projectService'

const projectSchema = z.object({
  nombre: z.string().min(1, 'El nombre es requerido').max(200, 'Máximo 200 caracteres'),
  descripcion: z.string().max(1000, 'Máximo 1000 caracteres').optional().default(''),
})

type ProjectForm = z.infer<typeof projectSchema>

export default function ProjectFormPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const isEdit = Boolean(id)

  const { data: project } = useQuery({
    queryKey: ['project', id],
    queryFn: () => getProject(id!),
    enabled: isEdit,
  })

  const {
    register, handleSubmit, formState: { errors, isSubmitting },
  } = useForm<ProjectForm>({
    defaultValues: { nombre: project?.nombre ?? '', descripcion: project?.descripcion ?? '' },
    values: project ? { nombre: project.nombre, descripcion: project.descripcion } : undefined,
  })

  const mutation = useMutation({
    mutationFn: (data: ProjectForm) =>
      isEdit ? updateProject(id!, data) : createProject(data.nombre, data.descripcion),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['projects'] })
      navigate('/projects')
    },
  })

  return (
    <div className="max-w-lg mx-auto">
      <h2 className="text-2xl font-bold mb-4">{isEdit ? 'Editar proyecto' : 'Nuevo proyecto'}</h2>
      <form onSubmit={handleSubmit((data) => mutation.mutate(data))} className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-1">Nombre</label>
          <input
            type="text" {...register('nombre')}
            className="w-full border rounded px-3 py-2"
          />
          {errors.nombre && <p className="text-red-500 text-xs mt-1">{errors.nombre.message}</p>}
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Descripción</label>
          <textarea
            {...register('descripcion')} rows={4}
            className="w-full border rounded px-3 py-2"
          />
          {errors.descripcion && <p className="text-red-500 text-xs mt-1">{errors.descripcion.message}</p>}
        </div>
        <div className="flex gap-2">
          <button
            type="submit" disabled={isSubmitting}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
          >
            {isSubmitting ? 'Guardando...' : 'Guardar'}
          </button>
          <button
            type="button" onClick={() => navigate('/projects')}
            className="bg-gray-200 text-gray-700 px-4 py-2 rounded hover:bg-gray-300"
          >
            Cancelar
          </button>
        </div>
      </form>
    </div>
  )
}
