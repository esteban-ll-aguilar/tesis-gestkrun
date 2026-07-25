import http from '../http'
import type { KanbanBoard } from '../../types'

export const boardService = {
  getProjectBoard: (projectId: string, sprintId?: string, assignedTo?: string) => {
    const params = new URLSearchParams()
    if (sprintId) params.set('sprint_id', sprintId)
    if (assignedTo) params.set('assigned_to', assignedTo)
    const qs = params.toString()
    return http.get<KanbanBoard>(`/boards/project/${projectId}${qs ? `?${qs}` : ''}`)
  },
  getSprintBoard: (sprintId: string) => http.get<KanbanBoard>(`/boards/${sprintId}`),
  createTask: (data: { historia_id: string; titulo: string; descripcion?: string }) =>
    http.post('/boards/tasks', data),
  assignTask: (taskId: string, userId: string) =>
    http.patch(`/boards/tasks/${taskId}/assign`, { user_id: userId }),
  transitionTask: (taskId: string, toEstado: string, reason?: string) =>
    http.patch(`/boards/tasks/${taskId}/transition`, { to_estado: toEstado, reason }),
  blockTask: (taskId: string, reason: string) =>
    http.patch(`/boards/tasks/${taskId}/block`, { reason }),
  unblockTask: (taskId: string) =>
    http.patch(`/boards/tasks/${taskId}/unblock`),
}
