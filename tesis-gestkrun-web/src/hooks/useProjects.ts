import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { projectService } from '../services/features/project.service'

export function useProjects() {
  return useQuery({
    queryKey: ['projects'],
    queryFn: async () => {
      const res = await projectService.list()
      return res.data
    },
  })
}

export function useProject(id: string) {
  return useQuery({
    queryKey: ['projects', id],
    queryFn: async () => {
      const res = await projectService.get(id)
      return res.data
    },
    enabled: !!id,
  })
}

export function useCreateProject() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (data: { nombre: string; descripcion: string }) =>
      projectService.create(data).then((r) => r.data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['projects'] })
    },
  })
}

export function useUpdateProject(id: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (data: { nombre?: string; descripcion?: string }) =>
      projectService.update(id, data).then((r) => r.data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['projects'] })
    },
  })
}

export function useDeleteProject() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (id: string) => projectService.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['projects'] })
    },
  })
}

export function useAssignTeam(projectId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ userId, rol }: { userId: string; rol: string }) =>
      projectService.assignTeam(projectId, userId, rol).then((r) => r.data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['projects', projectId] })
    },
  })
}

export function useProjectAssignments(projectId: string) {
  return useQuery({
    queryKey: ['project-assignments', projectId],
    queryFn: async () => {
      const res = await projectService.listAssignments(projectId)
      return res.data
    },
    enabled: !!projectId,
  })
}
