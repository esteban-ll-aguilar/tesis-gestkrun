import { Navigate, Outlet, useLocation } from 'react-router-dom'
import { useAuthStore } from '../../stores/auth'

export function AuthGuard() {
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated)
  const location = useLocation()

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />
  }

  return <Outlet />
}

export function RoleGuard({ roles }: { roles: string[] }) {
  const user = useAuthStore((s) => s.user)
  const location = useLocation()

  if (!user || !roles.includes(user.rol)) {
    return <Navigate to="/dashboard" replace />
  }

  return <Outlet />
}

export function GuestGuard() {
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated)

  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />
  }

  return <Outlet />
}
