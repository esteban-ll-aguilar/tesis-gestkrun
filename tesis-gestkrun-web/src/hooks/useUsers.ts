import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { userService } from '../services/features/user.service'

export function useUsers(search?: string) {
  return useQuery({
    queryKey: ['users', search],
    queryFn: async () => {
      const res = await userService.list(search)
      return res.data
    },
  })
}

export function useUpdateUserRol() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ userId, rol }: { userId: string; rol: string }) =>
      userService.updateRol(userId, rol).then((r) => r.data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] })
    },
  })
}
