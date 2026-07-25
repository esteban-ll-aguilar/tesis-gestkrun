import { useSortable } from '@dnd-kit/sortable'
import { CSS } from '@dnd-kit/utilities'
import { EstadoTareaBadge } from '../ui/Badge'
import type { KanbanTask } from '../../types'

interface KanbanCardProps {
  task: KanbanTask
  onClick?: (task: KanbanTask) => void
}

export function KanbanCard({ task, onClick }: KanbanCardProps) {
  const {
    attributes, listeners, setNodeRef, transform, transition, isDragging,
  } = useSortable({ id: task.id })

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.5 : 1,
  }

  return (
    <div
      ref={setNodeRef}
      style={style}
      {...attributes}
      {...listeners}
      onClick={() => onClick?.(task)}
      className="cursor-grab rounded-md border border-gray-200 bg-white p-3 shadow-sm hover:shadow-md active:cursor-grabbing"
    >
      <p className="text-sm font-medium text-gray-900">{task.titulo}</p>
      <div className="mt-2 flex items-center justify-between">
        <EstadoTareaBadge estado={task.estado} />
        {task.assigned_to && (
          <span className="text-xs text-gray-500">
            {task.assigned_to}
          </span>
        )}
      </div>
    </div>
  )
}
