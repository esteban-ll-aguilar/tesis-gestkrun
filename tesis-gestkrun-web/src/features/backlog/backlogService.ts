import http from '../../services/http';

export interface EpicaDTO {
  id: string;
  project_id: string;
  titulo: string;
  descripcion: string;
  prioridad: string;
  estado: string;
  orden: number;
  modulo_id: string | null;
}

export interface HistoriaDTO {
  id: string;
  epica_id: string;
  modulo_id: string | null;
  titulo: string;
  descripcion: string;
  criterios_aceptacion: string;
  prioridad: string;
  estimacion: number;
  orden: number;
  sprint_id: string | null;
  sprint_nombre: string | null;
}

export interface HistoriaWithEpica {
  epica: EpicaDTO;
  historias: HistoriaDTO[];
}

export interface SprintDTO {
  id: string;
  project_id: string;
  nombre: string;
  objetivo: string;
  duracion_dias: number;
  fecha_inicio: string;
  fecha_fin: string;
  estado: string;
  meeting_link?: string;
}

export interface SprintEventoDTO {
  id: string;
  sprint_id: string;
  tipo: string;
  fecha: string;
  notas: string;
  duracion_minutos: number;
  created_by: string;
}

export const backlogService = {
  getBacklog: (projectId: string) =>
    http.get<HistoriaWithEpica[]>(`/projects/${projectId}/backlog`).then(r => r.data),

  createEpica: (projectId: string, data: { titulo: string; descripcion?: string; prioridad?: string; modulo_id?: string | null }) =>
    http.post<EpicaDTO>(`/projects/${projectId}/backlog/epicas`, data).then(r => r.data),

  updateEpica: (projectId: string, epicaId: string, data: { titulo?: string; descripcion?: string; prioridad?: string; modulo_id?: string | null }) =>
    http.patch<EpicaDTO>(`/projects/${projectId}/backlog/epicas/${epicaId}`, data).then(r => r.data),

  deleteEpica: (projectId: string, epicaId: string) =>
    http.delete(`/projects/${projectId}/backlog/epicas/${epicaId}`),

  createHistoria: (projectId: string, data: { epica_id: string; titulo: string; descripcion?: string; criterios_aceptacion?: string; prioridad?: string; estimacion?: number; modulo_id?: string | null }) =>
    http.post<HistoriaDTO>(`/projects/${projectId}/backlog/historias`, data).then(r => r.data),

  updateHistoria: (projectId: string, historiaId: string, data: { titulo?: string; descripcion?: string; criterios_aceptacion?: string; prioridad?: string; estimacion?: number; modulo_id?: string | null }) =>
    http.patch<HistoriaDTO>(`/projects/${projectId}/backlog/historias/${historiaId}`, data).then(r => r.data),

  deleteHistoria: (projectId: string, historiaId: string) =>
    http.delete(`/projects/${projectId}/backlog/historias/${historiaId}`),

  prioritize: (projectId: string, epica_ids?: string[], historia_ids?: string[]) =>
    http.put(`/projects/${projectId}/backlog/prioritize`, { epica_ids, historia_ids }),

  listSprints: (projectId: string) =>
    http.get<SprintDTO[]>(`/projects/${projectId}/sprints`).then(r => r.data),

  getSprint: (projectId: string, sprintId: string) =>
    http.get<SprintDTO>(`/projects/${projectId}/sprints/${sprintId}`).then(r => r.data),

  planSprint: (projectId: string, data: { nombre: string; objetivo?: string; duracion_dias?: number; fecha_inicio: string; historia_ids?: string[]; meeting_link?: string }) =>
    http.post<SprintDTO>(`/projects/${projectId}/sprints`, data).then(r => r.data),

  startSprint: (projectId: string, sprintId: string) =>
    http.post<SprintDTO>(`/projects/${projectId}/sprints/${sprintId}/start`).then(r => r.data),

  closeSprint: (projectId: string, sprintId: string) =>
    http.post<SprintDTO>(`/projects/${projectId}/sprints/${sprintId}/close`).then(r => r.data),

  cancelSprint: (projectId: string, sprintId: string) =>
    http.post<SprintDTO>(`/projects/${projectId}/sprints/${sprintId}/cancel`).then(r => r.data),

  createEvento: (projectId: string, sprintId: string, data: { tipo: string; notas?: string; duracion_minutos?: number }) =>
    http.post<SprintEventoDTO>(`/projects/${projectId}/sprints/${sprintId}/eventos`, data).then(r => r.data),

  listEventos: (projectId: string, sprintId: string) =>
    http.get<SprintEventoDTO[]>(`/projects/${projectId}/sprints/${sprintId}/eventos`).then(r => r.data),

  createTask: (historiaId: string, data: { titulo: string; descripcion?: string }) =>
    http.post(`/boards/tasks`, { historia_id: historiaId, ...data }).then(r => r.data),
};
