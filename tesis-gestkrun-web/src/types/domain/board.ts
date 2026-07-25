import type { EstadoTarea } from './task'

export interface KanbanColumn {
  items: KanbanTask[]
  count: number
}

export interface KanbanBoard {
  project_id?: string
  sprint_id?: string
  columns: Record<string, KanbanColumn>
}

export interface KanbanTask {
  id: string
  titulo: string
  descripcion: string
  estado: EstadoTarea
  assigned_to: string | null
  fecha_limite: string | null
  fecha_creacion: string
}
