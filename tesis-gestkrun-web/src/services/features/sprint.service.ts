import http from '../http'
import type { Sprint, SprintEvento } from '../../types'

export const sprintService = {
  plan: (projectId: string, data: { nombre: string; objetivo?: string; duracion_dias?: number; fecha_inicio: string; historia_ids?: string[]; meeting_link?: string }) =>
    http.post<Sprint>(`/projects/${projectId}/sprints`, data),
  list: (projectId: string) => http.get<Sprint[]>(`/projects/${projectId}/sprints`),
  get: (projectId: string, sprintId: string) => http.get<Sprint>(`/projects/${projectId}/sprints/${sprintId}`),
  start: (projectId: string, sprintId: string) => http.post<Sprint>(`/projects/${projectId}/sprints/${sprintId}/start`),
  close: (projectId: string, sprintId: string) => http.post<Sprint>(`/projects/${projectId}/sprints/${sprintId}/close`),
  cancel: (projectId: string, sprintId: string) => http.post<Sprint>(`/projects/${projectId}/sprints/${sprintId}/cancel`),
  createEvento: (projectId: string, sprintId: string, data: { tipo: string; notas?: string; duracion_minutos?: number }) =>
    http.post<SprintEvento>(`/projects/${projectId}/sprints/${sprintId}/eventos`, data),
  listEventos: (projectId: string, sprintId: string) => http.get<SprintEvento[]>(`/projects/${projectId}/sprints/${sprintId}/eventos`),
}
