import { Navigate, Outlet, useLocation } from 'react-router-dom'
import { useAuthStore } from '../../stores/auth'

export function AuthGuard() {
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated)
  const initialized = useAuthStore((s) => s.initialized)
  const location = useLocation()

  if (!initialized) {
    return <div className="flex items-center justify-center h-screen text-gray-500">Verificando sesión...</div>
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />
  }

  return <Outlet />
}

export function RoleGuard({ roles }: { roles: string[] }) {
  const user = useAuthStore((s) => s.user)

  if (!user || !roles.includes(user.rol)) {
    return <Navigate to="/dashboard" replace />
  }

  return <Outlet />
}

export function GuestGuard() {
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated)
  const initialized = useAuthStore((s) => s.initialized)

  if (!initialized) {
    return <div className="flex items-center justify-center h-screen text-gray-500">Verificando sesión...</div>
  }

  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />
  }

  return <Outlet />
}
