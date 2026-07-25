import { useQuery } from '@tanstack/react-query'
import { taskService } from '../services/features/task.service'

export function useTasks(projectId: string, sprintId?: string, assignedTo?: string) {
  return useQuery({
    queryKey: ['tasks', projectId, sprintId, assignedTo],
    queryFn: async () => {
      const res = await taskService.list(projectId, sprintId, assignedTo)
      return res.data
    },
    enabled: !!projectId,
  })
}
