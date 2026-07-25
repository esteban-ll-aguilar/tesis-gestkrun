export type EstadoSprint = 'PLANIFICADO' | 'EN_EJECUCION' | 'FINALIZADO' | 'CANCELADO'
export type TipoEventoScrum = 'SPRINT_PLANNING' | 'DAILY_SCRUM' | 'SPRINT_REVIEW' | 'SPRINT_RETROSPECTIVE'

export interface Sprint {
  id: string
  project_id: string
  nombre: string
  objetivo: string
  duracion_dias: number
  fecha_inicio: string
  fecha_fin: string
  estado: EstadoSprint
  meeting_link: string
}

export interface SprintEvento {
  id: string
  sprint_id: string
  tipo: TipoEventoScrum
  fecha: string
  notas: string
  duracion_minutos: number
  created_by: string
}
