export type EstadoProyecto = 'ACTIVO' | 'INACTIVO' | 'FINALIZADO' | 'CANCELADO'

export interface Project {
  id: string
  nombre: string
  descripcion: string
  estado: EstadoProyecto
  fechaInicio: string
  owner: import('./auth').User
}
