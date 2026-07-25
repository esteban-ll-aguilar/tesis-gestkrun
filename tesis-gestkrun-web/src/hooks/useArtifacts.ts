import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { artifactService } from '../services/features/artifact.service'

export function useArtifacts(taskId: string) {
  return useQuery({
    queryKey: ['artifacts', taskId],
    queryFn: async () => {
      const res = await artifactService.listByTask(taskId)
      return res.data
    },
    enabled: !!taskId,
  })
}

export function useArtifactVersions(artifactId: string) {
  return useQuery({
    queryKey: ['artifact-versions', artifactId],
    queryFn: async () => {
      const res = await artifactService.listVersions(artifactId)
      return res.data
    },
    enabled: !!artifactId,
  })
}

export function useCreateArtifact(taskId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (data: { nombre: string; tipo: string }) =>
      artifactService.create(taskId, data).then((r) => r.data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['artifacts', taskId] })
    },
  })
}

export function useUploadVersion(artifactId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (formData: FormData) =>
      artifactService.uploadVersion(artifactId, formData).then((r) => r.data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['artifact-versions', artifactId] })
    },
  })
}
