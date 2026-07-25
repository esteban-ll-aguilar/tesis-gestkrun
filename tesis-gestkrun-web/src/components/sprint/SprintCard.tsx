import type { Sprint } from '../../types'
import { EstadoSprintBadge } from '../ui/Badge'

interface SprintCardProps {
  sprint: Sprint
  onClick?: (sprint: Sprint) => void
}

export function SprintCard({ sprint, onClick }: SprintCardProps) {
  return (
    <div
      onClick={() => onClick?.(sprint)}
      className="cursor-pointer rounded-lg border border-gray-200 bg-white p-4 shadow-sm transition-shadow hover:shadow-md"
    >
      <div className="flex items-start justify-between">
        <div>
          <h4 className="text-sm font-semibold text-gray-900">{sprint.nombre}</h4>
          <p className="mt-1 text-xs text-gray-600 line-clamp-1">{sprint.objetivo}</p>
        </div>
        <EstadoSprintBadge estado={sprint.estado} />
      </div>
      <div className="mt-3 flex items-center gap-4 text-xs text-gray-500">
        <span>{sprint.duracion_dias} días</span>
        <span>{sprint.fecha_inicio} → {sprint.fecha_fin}</span>
      </div>
    </div>
  )
}
