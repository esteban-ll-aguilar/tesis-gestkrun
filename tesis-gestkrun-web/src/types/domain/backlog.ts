export type Prioridad = 'BAJA' | 'MEDIA' | 'ALTA' | 'CRITICA'

export interface Epica {
  id: string
  project_id: string
  titulo: string
  descripcion: string
  prioridad: string
  estado: string
  orden: number
  modulo_id: string | null
}

export interface HistoriaUsuario {
  id: string
  epica_id: string
  modulo_id: string | null
  titulo: string
  descripcion: string
  criterios_aceptacion: string
  prioridad: string
  estimacion: number
  orden: number
  sprint_id: string | null
  sprint_nombre: string | null
}
