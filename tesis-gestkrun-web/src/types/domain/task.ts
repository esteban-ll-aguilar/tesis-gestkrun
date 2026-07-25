export type EstadoTarea = 'PENDIENTE' | 'EN_PROCESO' | 'BLOQUEADO' | 'EN_REVISION' | 'TERMINADO' | 'CANCELADO'

export interface Task {
  id: string
  titulo: string
  descripcion: string
  estado: EstadoTarea
  assigned_to: string | null
  fecha_creacion: string
  fecha_limite: string | null
}
