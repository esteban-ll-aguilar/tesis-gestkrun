import { useDroppable } from '@dnd-kit/core'
import { SortableContext, verticalListSortingStrategy } from '@dnd-kit/sortable'
import { KanbanCard } from './KanbanCard'
import type { KanbanTask } from '../../types'

interface KanbanColumnProps {
  id: string
  title: string
  items: KanbanTask[]
  count: number
  wipLimit?: number
}

const columnColors: Record<string, string> = {
  PENDIENTE: 'border-t-gray-400',
  EN_PROCESO: 'border-t-blue-500',
  BLOQUEADO: 'border-t-red-500',
  EN_REVISION: 'border-t-yellow-500',
  TERMINADO: 'border-t-green-500',
  CANCELADO: 'border-t-gray-400',
}

export function KanbanColumn({ id, title, items, count, wipLimit }: KanbanColumnProps) {
  const { setNodeRef, isOver } = useDroppable({ id })
  const borderColor = columnColors[id] ?? 'border-t-gray-400'
  const isOverWip = wipLimit !== undefined && count >= wipLimit

  return (
    <div
      ref={setNodeRef}
      className={`flex min-h-[200px] w-72 flex-col rounded-lg border bg-gray-50 border-t-4 ${borderColor} ${
        isOver ? 'ring-2 ring-blue-400' : ''
      }`}
    >
      <div className="flex items-center justify-between border-b border-gray-200 px-3 py-2">
        <h3 className="text-sm font-semibold text-gray-700">{title}</h3>
        <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${
          isOverWip ? 'bg-red-100 text-red-700' : 'bg-gray-200 text-gray-600'
        }`}>
          {count}{wipLimit !== undefined ? `/${wipLimit}` : ''}
        </span>
      </div>
      <div className="flex flex-1 flex-col gap-2 p-2">
        <SortableContext items={items.map((i) => i.id)} strategy={verticalListSortingStrategy}>
          {items.map((task) => (
            <KanbanCard key={task.id} task={task} />
          ))}
        </SortableContext>
      </div>
    </div>
  )
}
