import { create } from 'zustand'
import type { User } from '../types'
import { setAccessToken } from '../services/http'
import http from '../services/http'

interface AuthState {
  user: User | null
  isAuthenticated: boolean
  initialized: boolean
  setUser: (user: User | null) => void
  setAuth: (user: User, accessToken: string) => void
  logout: () => void
  initialize: () => void
  hasRole: (...roles: string[]) => boolean
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  isAuthenticated: false,
  initialized: false,
  setUser: (user) => set({ user, isAuthenticated: !!user }),
  setAuth: (user, accessToken) => {
    setAccessToken(accessToken)
    localStorage.setItem('accessToken', accessToken)
    set({ user, isAuthenticated: true, initialized: true })
  },
  logout: () => {
    setAccessToken(null)
    localStorage.removeItem('accessToken')
    set({ user: null, isAuthenticated: false })
  },
  initialize: async () => {
    const token = localStorage.getItem('accessToken')
    if (!token) {
      set({ initialized: true })
      return
    }
    setAccessToken(token)
    try {
      const res = await http.get('/auth/me')
      set({ user: res.data as User, isAuthenticated: true, initialized: true })
    } catch {
      localStorage.removeItem('accessToken')
      setAccessToken(null)
      set({ user: null, isAuthenticated: false, initialized: true })
    }
  },
  hasRole: (...roles) => {
    const user = get().user
    return user !== null && (roles.includes(user.rol) || user.rol === 'ADMIN')
  },
}))
