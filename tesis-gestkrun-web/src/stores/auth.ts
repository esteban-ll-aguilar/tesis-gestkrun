import { create } from 'zustand'
import type { User } from '../types'
import { setAccessToken, getAccessToken } from '../services/http'

interface AuthState {
  user: User | null
  isAuthenticated: boolean
  setUser: (user: User | null) => void
  setAuth: (user: User, accessToken: string) => void
  logout: () => void
  initialize: () => void
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: false,
  setUser: (user) => set({ user, isAuthenticated: !!user }),
  setAuth: (user, accessToken) => {
    setAccessToken(accessToken)
    localStorage.setItem('accessToken', accessToken)
    set({ user, isAuthenticated: true })
  },
  logout: () => {
    setAccessToken(null)
    localStorage.removeItem('accessToken')
    set({ user: null, isAuthenticated: false })
  },
  initialize: () => {
    const token = localStorage.getItem('accessToken')
    if (token) {
      setAccessToken(token)
      fetch('/api/v1/auth/me', {
        headers: { Authorization: `Bearer ${token}` },
      })
        .then((res) => res.ok ? res.json() : null)
        .then((user) => {
          if (user) set({ user: user as User, isAuthenticated: true })
          else { localStorage.removeItem('accessToken'); setAccessToken(null) }
        })
        .catch(() => { localStorage.removeItem('accessToken'); setAccessToken(null) })
    }
  },
}))
