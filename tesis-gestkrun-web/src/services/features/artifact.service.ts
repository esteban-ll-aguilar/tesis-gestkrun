import http from '../http'
import type { Artifact, ArtifactVersion } from '../../types'

export const artifactService = {
  listByTask: (taskId: string) => http.get<Artifact[]>(`/tasks/${taskId}/artifacts`),
  create: (taskId: string, data: { nombre: string; tipo: string }) =>
    http.post<Artifact>(`/tasks/${taskId}/artifacts`, data),
  uploadVersion: (artifactId: string, formData: FormData) =>
    http.post<ArtifactVersion>(`/artifacts/${artifactId}/versions`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),
  listVersions: (artifactId: string) => http.get<ArtifactVersion[]>(`/artifacts/${artifactId}/versions`),
}
