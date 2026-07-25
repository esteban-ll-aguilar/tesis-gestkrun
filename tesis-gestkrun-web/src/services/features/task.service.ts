import http from '../http'
import type { Task } from '../../types'

export const taskService = {
  list: (projectId: string, sprintId?: string, assignedTo?: string) => {
    const params = new URLSearchParams()
    if (sprintId) params.set('sprint_id', sprintId)
    if (assignedTo) params.set('assigned_to', assignedTo)
    const qs = params.toString()
    return http.get<Task[]>(`/projects/${projectId}/tasks${qs ? `?${qs}` : ''}`)
  },
}
