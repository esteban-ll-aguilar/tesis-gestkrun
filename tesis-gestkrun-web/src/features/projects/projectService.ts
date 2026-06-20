import http from '../../services/http'
import type { Project } from '../../types'

export interface ProjectDTO {
  id: string
  nombre: string
  descripcion: string
  estado: string
  owner_id: string
}

export async function listProjects(): Promise<ProjectDTO[]> {
  const { data } = await http.get('/projects')
  return data
}

export async function getProject(id: string): Promise<ProjectDTO> {
  const { data } = await http.get(`/projects/${id}`)
  return data
}

export async function createProject(nombre: string, descripcion: string): Promise<ProjectDTO> {
  const { data } = await http.post('/projects', { nombre, descripcion })
  return data
}

export async function updateProject(id: string, payload: { nombre?: string; descripcion?: string }): Promise<ProjectDTO> {
  const { data } = await http.patch(`/projects/${id}`, payload)
  return data
}

export async function deleteProject(id: string): Promise<void> {
  await http.delete(`/projects/${id}`)
}

export interface AssignmentDTO {
  id: string
  user_id: string
  rol: string
  nombre?: string
}

export async function listAssignments(projectId: string): Promise<AssignmentDTO[]> {
  const { data } = await http.get(`/projects/${projectId}/assignments`)
  return data
}

export async function assignTeam(projectId: string, userId: string, rol: string): Promise<AssignmentDTO> {
  const { data } = await http.post(`/projects/${projectId}/assignments`, { user_id: userId, rol })
  return data
}
