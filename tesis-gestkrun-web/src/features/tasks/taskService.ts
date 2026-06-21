import http from '../../services/http';

export interface TaskDTO {
  id: string
  titulo: string
  descripcion: string
  estado: string
  assigned_to: string | null
  fecha_creacion: string
  fecha_limite: string | null
}

export const taskService = {
  listTasks: (projectId: string, params?: { sprint_id?: string; assigned_to?: string }) =>
    http.get<TaskDTO[]>('/projects/' + projectId + '/tasks', { params }).then(r => r.data),
};
