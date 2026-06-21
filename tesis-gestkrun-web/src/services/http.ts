import axios, { AxiosError } from 'axios'
import type { InternalAxiosRequestConfig } from 'axios'

const http = axios.create({
  baseURL: '/api/v1',
  headers: { 'Content-Type': 'application/json' },
})

let accessToken: string | null = null

export function setAccessToken(token: string | null) {
  accessToken = token
}

export function getAccessToken(): string | null {
  return accessToken
}

http.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  if (accessToken && config.headers) {
    config.headers.Authorization = `Bearer ${accessToken}`
  }
  return config
})

let refreshPromise: Promise<string | null> | null = null

http.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean }

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      if (!refreshPromise) {
        refreshPromise = http.post('/auth/refresh', {}, { withCredentials: true })
          .then((res) => {
            const token = res.data.accessToken
            setAccessToken(token)
            return token
          })
          .catch(() => {
            setAccessToken(null)
            return null
          })
          .finally(() => { refreshPromise = null })
      }

      const token = await refreshPromise
      if (token && originalRequest.headers) {
        originalRequest.headers.Authorization = `Bearer ${token}`
        return http(originalRequest)
      }
    }

    return Promise.reject(error)
  }
)

export default http
