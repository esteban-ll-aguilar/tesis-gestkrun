import http from '../../services/http';

export interface ArtifactDTO {
  id: string;
  nombre: string;
  tipo: string;
  version_actual: number;
}

export interface ArtifactVersionDTO {
  id: string;
  version: number;
  content_url: string;
  uploaded_by: string;
  created_at: string;
}

export const artifactService = {
  upload: (taskId: string, nombre: string, tipo: string, file: File) => {
    const form = new FormData();
    form.append('task_id', taskId);
    form.append('nombre', nombre);
    form.append('tipo', tipo);
    form.append('file', file);
    return http.post<{ id: string; nombre: string; tipo: string; version: number; content_url: string }>(
      '/artifacts', form
    ).then(r => r.data);
  },

  listByTask: (taskId: string) =>
    http.get<ArtifactDTO[]>(`/artifacts/task/${taskId}`).then(r => r.data),

  listVersions: (artifactId: string) =>
    http.get<ArtifactVersionDTO[]>(`/artifacts/${artifactId}/versions`).then(r => r.data),

  download: (artifactId: string, version: number) =>
    http.get<{ content_url: string; version: number }>(`/artifacts/${artifactId}/download/${version}`).then(r => r.data),
};
