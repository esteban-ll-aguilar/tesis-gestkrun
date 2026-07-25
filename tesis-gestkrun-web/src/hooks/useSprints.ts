import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { sprintService } from '../services/features/sprint.service'

export function useSprints(projectId: string) {
  return useQuery({
    queryKey: ['sprints', projectId],
    queryFn: async () => {
      const res = await sprintService.list(projectId)
      return res.data
    },
    enabled: !!projectId,
  })
}

export function useSprint(projectId: string, sprintId: string) {
  return useQuery({
    queryKey: ['sprints', projectId, sprintId],
    queryFn: async () => {
      const res = await sprintService.get(projectId, sprintId)
      return res.data
    },
    enabled: !!projectId && !!sprintId,
  })
}

export function usePlanSprint(projectId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (data: { nombre: string; objetivo?: string; duracion_dias?: number; fecha_inicio: string; historia_ids?: string[]; meeting_link?: string }) =>
      sprintService.plan(projectId, data).then((r) => r.data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['sprints', projectId] })
    },
  })
}

export function useStartSprint(projectId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (sprintId: string) =>
      sprintService.start(projectId, sprintId).then((r) => r.data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['sprints', projectId] })
    },
  })
}

export function useCloseSprint(projectId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (sprintId: string) =>
      sprintService.close(projectId, sprintId).then((r) => r.data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['sprints', projectId] })
    },
  })
}

export function useCancelSprint(projectId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (sprintId: string) =>
      sprintService.cancel(projectId, sprintId).then((r) => r.data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['sprints', projectId] })
    },
  })
}

export function useSprintEventos(projectId: string, sprintId: string) {
  return useQuery({
    queryKey: ['sprint-eventos', projectId, sprintId],
    queryFn: async () => {
      const res = await sprintService.listEventos(projectId, sprintId)
      return res.data
    },
    enabled: !!projectId && !!sprintId,
  })
}

export function useCreateSprintEvento(projectId: string, sprintId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (data: { tipo: string; notas?: string; duracion_minutos?: number }) =>
      sprintService.createEvento(projectId, sprintId, data).then((r) => r.data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['sprint-eventos', projectId, sprintId] })
    },
  })
}
