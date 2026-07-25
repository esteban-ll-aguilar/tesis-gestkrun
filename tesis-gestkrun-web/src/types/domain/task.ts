export type EstadoTarea = 'PENDIENTE' | 'EN_PROCESO' | 'BLOQUEADO' | 'EN_REVISION' | 'TERMINADO' | 'CANCELADO'

export const ALLOWED_TRANSITIONS: Record<EstadoTarea, EstadoTarea[]> = {
  PENDIENTE: ['EN_PROCESO', 'CANCELADO'],
  EN_PROCESO: ['BLOQUEADO', 'EN_REVISION', 'CANCELADO'],
  BLOQUEADO: ['EN_PROCESO', 'CANCELADO'],
  EN_REVISION: ['TERMINADO', 'EN_PROCESO', 'CANCELADO'],
  TERMINADO: [],
  CANCELADO: [],
}

export function canTransition(from: EstadoTarea, to: EstadoTarea): boolean {
  return ALLOWED_TRANSITIONS[from]?.includes(to) ?? false
}

export interface Task {
  id: string
  titulo: string
  descripcion: string
  estado: EstadoTarea
  assigned_to: string | null
  fecha_creacion: string
  fecha_limite: string | null
}
