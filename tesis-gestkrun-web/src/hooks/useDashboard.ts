import { useQuery } from '@tanstack/react-query'
import { dashboardService } from '../services/features/dashboard.service'

export function useDashboardMetrics(projectId: string) {
  return useQuery({
    queryKey: ['dashboard', 'metrics', projectId],
    queryFn: async () => {
      const res = await dashboardService.getMetrics(projectId)
      return res.data
    },
    enabled: !!projectId,
  })
}

export function useDashboardVelocity(projectId: string) {
  return useQuery({
    queryKey: ['dashboard', 'velocity', projectId],
    queryFn: async () => {
      const res = await dashboardService.getVelocity(projectId)
      return res.data
    },
    enabled: !!projectId,
  })
}
