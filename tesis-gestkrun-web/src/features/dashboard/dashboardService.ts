import http from '../../services/http';

export interface MetricsDTO {
  total_tasks: number;
  in_progress: number;
  blocked: number;
  completed: number;
  completion_percentage: number;
}

export interface SprintVelocityDTO {
  sprint_id: string;
  sprint_nombre: string;
  fecha_inicio: string;
  fecha_fin: string;
  estado: string;
  total_tasks: number;
  completed_tasks: number;
  velocity: number;
}

export interface TaskDistributionDTO {
  estado: string;
  count: number;
}

export const dashboardService = {
  getMetrics: (projectId: string) =>
    http.get<MetricsDTO>(`/dashboard/${projectId}/metrics`).then(r => r.data),

  getVelocity: (projectId: string) =>
    http.get<SprintVelocityDTO[]>(`/dashboard/${projectId}/velocity`).then(r => r.data),

  getTaskDistribution: (projectId: string) =>
    http.get<TaskDistributionDTO[]>(`/dashboard/${projectId}/task-distribution`).then(r => r.data),
};
