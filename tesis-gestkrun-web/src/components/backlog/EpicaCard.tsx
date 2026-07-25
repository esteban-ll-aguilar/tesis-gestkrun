import type { Epica } from '../../types'
import { PrioridadBadge } from '../ui/Badge'

interface EpicaCardProps {
  epica: Epica
  onEdit?: (epica: Epica) => void
  onDelete?: (epica: Epica) => void
}

export function EpicaCard({ epica, onEdit, onDelete }: EpicaCardProps) {
  return (
    <div className="rounded-lg border border-gray-200 bg-white p-4 shadow-sm">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <h4 className="text-sm font-semibold text-gray-900">{epica.titulo}</h4>
          <p className="mt-1 text-sm text-gray-600 line-clamp-2">{epica.descripcion}</p>
        </div>
        <PrioridadBadge prioridad={epica.prioridad} />
      </div>
      <div className="mt-3 flex items-center justify-between">
        <span className="text-xs text-gray-500">#{epica.orden}</span>
        <div className="flex gap-2">
          {onEdit && (
            <button onClick={() => onEdit(epica)} className="text-xs text-blue-600 hover:text-blue-800">
              Editar
            </button>
          )}
          {onDelete && (
            <button onClick={() => onDelete(epica)} className="text-xs text-red-600 hover:text-red-800">
              Eliminar
            </button>
          )}
        </div>
      </div>
    </div>
  )
}
