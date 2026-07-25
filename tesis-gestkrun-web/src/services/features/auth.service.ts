import http from '../http'
import type { User } from '../../types'

export const authService = {
  login: (email: string, password: string) =>
    http.post<{ user: User; accessToken: string; refreshToken: string }>('/auth/login', { email, password }),
  register: (nombre: string, email: string, password: string) =>
    http.post<{ user: User; accessToken: string; refreshToken: string }>('/auth/register', { nombre, email, password }),
  me: () => http.get<User>('/auth/me'),
  refresh: () => http.post<{ accessToken: string }>('/auth/refresh', {}, { withCredentials: true }),
  logout: () => http.post('/auth/logout'),
}
