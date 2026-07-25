import http from '../http'
import type { Epica, HistoriaUsuario } from '../../types'

export const backlogService = {
  getBacklog: (projectId: string) => http.get(`/projects/${projectId}/backlog`),
  createEpica: (projectId: string, data: { titulo: string; descripcion?: string; prioridad?: string; modulo_id?: string | null }) =>
    http.post<Epica>(`/projects/${projectId}/backlog/epicas`, data),
  listEpicas: (projectId: string) => http.get<Epica[]>(`/projects/${projectId}/backlog/epicas`),
  updateEpica: (projectId: string, epicaId: string, data: Record<string, unknown>) =>
    http.patch<Epica>(`/projects/${projectId}/backlog/epicas/${epicaId}`, data),
  deleteEpica: (projectId: string, epicaId: string) =>
    http.delete(`/projects/${projectId}/backlog/epicas/${epicaId}`),
  createHistoria: (projectId: string, data: { epica_id: string; titulo: string; descripcion?: string; criterios_aceptacion?: string; prioridad?: string; estimacion?: number; modulo_id?: string | null }) =>
    http.post<HistoriaUsuario>(`/projects/${projectId}/backlog/historias`, data),
  updateHistoria: (projectId: string, historiaId: string, data: Record<string, unknown>) =>
    http.patch<HistoriaUsuario>(`/projects/${projectId}/backlog/historias/${historiaId}`, data),
  deleteHistoria: (projectId: string, historiaId: string) =>
    http.delete(`/projects/${projectId}/backlog/historias/${historiaId}`),
  prioritize: (projectId: string, epicaIds?: string[], historiaIds?: string[]) =>
    http.put(`/projects/${projectId}/backlog/prioritize`, { epica_ids: epicaIds, historia_ids: historiaIds }),
}
