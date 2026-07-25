import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { boardService } from '../services/features/board.service'
import type { KanbanBoard } from '../types'

export function useProjectBoard(projectId: string, sprintId?: string, assignedTo?: string) {
  return useQuery({
    queryKey: ['board', 'project', projectId, sprintId, assignedTo],
    queryFn: async () => {
      const res = await boardService.getProjectBoard(projectId, sprintId, assignedTo)
      return res.data as KanbanBoard
    },
    enabled: !!projectId,
  })
}

export function useSprintBoard(sprintId: string) {
  return useQuery({
    queryKey: ['board', 'sprint', sprintId],
    queryFn: async () => {
      const res = await boardService.getSprintBoard(sprintId)
      return res.data as KanbanBoard
    },
    enabled: !!sprintId,
  })
}

export function useCreateTask() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (data: { historia_id: string; titulo: string; descripcion?: string }) =>
      boardService.createTask(data).then((r) => r.data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['board'] })
    },
  })
}

export function useTransitionTask() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ taskId, toEstado, reason }: { taskId: string; toEstado: string; reason?: string }) =>
      boardService.transitionTask(taskId, toEstado, reason).then((r) => r.data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['board'] })
    },
  })
}

export function useAssignTask() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ taskId, userId }: { taskId: string; userId: string }) =>
      boardService.assignTask(taskId, userId).then((r) => r.data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['board'] })
    },
  })
}

export function useBlockTask() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ taskId, reason }: { taskId: string; reason: string }) =>
      boardService.blockTask(taskId, reason).then((r) => r.data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['board'] })
    },
  })
}

export function useUnblockTask() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (taskId: string) =>
      boardService.unblockTask(taskId).then((r) => r.data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['board'] })
    },
  })
}
