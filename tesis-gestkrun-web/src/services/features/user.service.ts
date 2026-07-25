import http from '../http'
import type { User } from '../../types'

export const userService = {
  list: (search?: string) => {
    const qs = search ? `?search=${encodeURIComponent(search)}` : ''
    return http.get<User[]>(`/users${qs}`)
  },
  updateRol: (userId: string, rol: string) =>
    http.patch(`/users/${userId}/rol`, { rol }),
}
