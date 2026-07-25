import type { Project } from '../../types'
import { Badge } from '../ui/Badge'

interface ProjectCardProps {
  project: Project
  onClick?: (project: Project) => void
}

export function ProjectCard({ project, onClick }: ProjectCardProps) {
  return (
    <div
      onClick={() => onClick?.(project)}
      className="cursor-pointer rounded-lg border border-gray-200 bg-white p-5 shadow-sm transition-shadow hover:shadow-md"
    >
      <div className="flex items-start justify-between">
        <h3 className="text-lg font-semibold text-gray-900">{project.nombre}</h3>
        <Badge variant={project.estado === 'ACTIVO' ? 'success' : 'default'}>
          {project.estado}
        </Badge>
      </div>
      <p className="mt-2 text-sm text-gray-600 line-clamp-2">{project.descripcion}</p>
      <div className="mt-4 flex items-center text-xs text-gray-500">
        <span>Owner: {project.owner?.nombre ?? project.owner_id}</span>
      </div>
    </div>
  )
}
