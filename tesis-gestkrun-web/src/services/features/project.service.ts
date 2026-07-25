import http from '../http'
import type { Project } from '../../types'

export const projectService = {
  list: () => http.get<Project[]>('/projects'),
  get: (id: string) => http.get<Project>(`/projects/${id}`),
  create: (data: { nombre: string; descripcion: string }) => http.post<Project>('/projects', data),
  update: (id: string, data: { nombre?: string; descripcion?: string }) => http.patch<Project>(`/projects/${id}`, data),
  delete: (id: string) => http.delete(`/projects/${id}`),
  assignTeam: (projectId: string, userId: string, rol: string) =>
    http.post(`/projects/${projectId}/assignments`, { user_id: userId, rol }),
  removeAssignment: (projectId: string, userId: string) =>
    http.delete(`/projects/${projectId}/assignments/${userId}`),
  listAssignments: (projectId: string) =>
    http.get(`/projects/${projectId}/assignments`),
}
