import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { backlogService } from '../services/features/backlog.service'

export function useBacklog(projectId: string) {
  return useQuery({
    queryKey: ['backlog', projectId],
    queryFn: async () => {
      const res = await backlogService.getBacklog(projectId)
      return res.data
    },
    enabled: !!projectId,
  })
}

export function useEpicas(projectId: string) {
  return useQuery({
    queryKey: ['epicas', projectId],
    queryFn: async () => {
      const res = await backlogService.listEpicas(projectId)
      return res.data
    },
    enabled: !!projectId,
  })
}

export function useCreateEpica(projectId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (data: { titulo: string; descripcion?: string; prioridad?: string; modulo_id?: string | null }) =>
      backlogService.createEpica(projectId, data).then((r) => r.data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['backlog', projectId] })
      queryClient.invalidateQueries({ queryKey: ['epicas', projectId] })
    },
  })
}

export function useUpdateEpica(projectId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ epicaId, data }: { epicaId: string; data: Record<string, unknown> }) =>
      backlogService.updateEpica(projectId, epicaId, data).then((r) => r.data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['backlog', projectId] })
      queryClient.invalidateQueries({ queryKey: ['epicas', projectId] })
    },
  })
}

export function useDeleteEpica(projectId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (epicaId: string) => backlogService.deleteEpica(projectId, epicaId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['backlog', projectId] })
      queryClient.invalidateQueries({ queryKey: ['epicas', projectId] })
    },
  })
}

export function useCreateHistoria(projectId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (data: { epica_id: string; titulo: string; descripcion?: string; criterios_aceptacion?: string; prioridad?: string; estimacion?: number; modulo_id?: string | null }) =>
      backlogService.createHistoria(projectId, data).then((r) => r.data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['backlog', projectId] })
    },
  })
}

export function useUpdateHistoria(projectId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ historiaId, data }: { historiaId: string; data: Record<string, unknown> }) =>
      backlogService.updateHistoria(projectId, historiaId, data).then((r) => r.data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['backlog', projectId] })
    },
  })
}

export function useDeleteHistoria(projectId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (historiaId: string) => backlogService.deleteHistoria(projectId, historiaId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['backlog', projectId] })
    },
  })
}

export function usePrioritizeBacklog(projectId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ epicaIds, historiaIds }: { epicaIds?: string[]; historiaIds?: string[] }) =>
      backlogService.prioritize(projectId, epicaIds, historiaIds),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['backlog', projectId] })
    },
  })
}
