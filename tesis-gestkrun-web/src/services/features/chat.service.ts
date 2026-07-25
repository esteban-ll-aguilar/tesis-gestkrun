import http from '../http'
import type { Message } from '../../types'

export const chatService = {
  listByProject: (projectId: string, cursor?: string, limit = 50) => {
    const params = new URLSearchParams({ limit: String(limit) })
    if (cursor) params.set('cursor', cursor)
    return http.get<Message[]>(`/projects/${projectId}/messages?${params}`)
  },
  listByTask: (taskId: string, cursor?: string, limit = 50) => {
    const params = new URLSearchParams({ limit: String(limit) })
    if (cursor) params.set('cursor', cursor)
    return http.get<Message[]>(`/tasks/${taskId}/messages?${params}`)
  },
  send: (data: { proyecto_id?: string; task_id?: string; contenido: string; tipo: string }) =>
    http.post<Message>('/messages', data),
}
