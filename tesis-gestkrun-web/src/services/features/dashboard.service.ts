import http from '../http'

export const dashboardService = {
  getMetrics: (projectId: string) => http.get(`/dashboard/${projectId}/metrics`),
  getVelocity: (projectId: string) => http.get(`/dashboard/${projectId}/velocity`),
}
