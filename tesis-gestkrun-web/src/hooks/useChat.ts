import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { chatService } from '../services/features/chat.service'

export function useProjectMessages(projectId: string, cursor?: string) {
  return useQuery({
    queryKey: ['messages', projectId, cursor],
    queryFn: async () => {
      const res = await chatService.listByProject(projectId, cursor)
      return res.data
    },
    enabled: !!projectId,
  })
}

export function useTaskMessages(taskId: string, cursor?: string) {
  return useQuery({
    queryKey: ['messages', 'task', taskId, cursor],
    queryFn: async () => {
      const res = await chatService.listByTask(taskId, cursor)
      return res.data
    },
    enabled: !!taskId,
  })
}

export function useSendMessage() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (data: { proyecto_id?: string; task_id?: string; contenido: string; tipo: string }) =>
      chatService.send(data).then((r) => r.data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['messages'] })
    },
  })
}
