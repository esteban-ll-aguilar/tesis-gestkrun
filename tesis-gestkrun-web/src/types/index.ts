export type Rol = 'ADMIN' | 'PRODUCT_OWNER' | 'SCRUM_MASTER' | 'DEVELOPER'

export type EstadoTarea = 'PENDIENTE' | 'EN_PROCESO' | 'BLOQUEADO' | 'EN_REVISION' | 'TERMINADO' | 'CANCELADO'

export type EstadoSprint = 'PLANIFICADO' | 'EN_EJECUCION' | 'FINALIZADO' | 'CANCELADO'

export type EstadoProyecto = 'ACTIVO' | 'INACTIVO' | 'FINALIZADO' | 'CANCELADO'

export type Prioridad = 'BAJA' | 'MEDIA' | 'ALTA' | 'CRITICA'

export type TipoMensaje = 'PROYECTO' | 'TAREA'

export type TipoEventoScrum = 'SPRINT_PLANNING' | 'DAILY_SCRUM' | 'SPRINT_REVIEW' | 'SPRINT_RETROSPECTIVE'

export interface User {
  id: string
  nombre: string
  email: string
  rol: Rol
  fechaRegistro: string
}

export interface Project {
  id: string
  nombre: string
  descripcion: string
  estado: EstadoProyecto
  fechaInicio: string
  owner: User
}

export interface PaginatedResponse<T> {
  data: T[]
  nextCursor: string | null
  hasMore: boolean
}

export interface ApiError {
  type: string
  title: string
  status: number
  detail: string
  errors?: Record<string, string[]>
}
