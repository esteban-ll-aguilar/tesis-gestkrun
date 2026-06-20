import { lazy, Suspense } from 'react'
import { createBrowserRouter, Navigate, RouterProvider } from 'react-router-dom'
import { AuthGuard, GuestGuard, RoleGuard } from '../features/auth/AuthGuard'
import { AdminLayout, AuthLayout, MainLayout } from './layouts'

const LoginPage = lazy(() => import('../pages/LoginPage'))
const RegisterPage = lazy(() => import('../pages/RegisterPage'))
const RecoverPasswordPage = lazy(() => import('../pages/RecoverPasswordPage'))
const DashboardPage = lazy(() => import('../pages/DashboardPage'))
const ProjectListPage = lazy(() => import('../pages/ProjectListPage'))
const ProjectFormPage = lazy(() => import('../pages/ProjectFormPage'))
const ProjectDetailPage = lazy(() => import('../pages/ProjectDetailPage'))
const UserManagementPage = lazy(() => import('../pages/UserManagementPage'))

function Loading() {
  return <div className="flex items-center justify-center h-screen">Cargando...</div>
}

const router = createBrowserRouter([
  {
    element: <GuestGuard />,
    children: [
      {
        element: <AuthLayout />,
        children: [
          {
            path: '/login',
            element: <Suspense fallback={<Loading />}><LoginPage /></Suspense>,
          },
          {
            path: '/register',
            element: <Suspense fallback={<Loading />}><RegisterPage /></Suspense>,
          },
          {
            path: '/recover-password',
            element: <Suspense fallback={<Loading />}><RecoverPasswordPage /></Suspense>,
          },
        ],
      },
    ],
  },
  {
    element: <AuthGuard />,
    children: [
      {
        element: <MainLayout />,
        children: [
          { index: true, element: <Navigate to="/dashboard" replace /> },
          {
            path: 'dashboard',
            element: <Suspense fallback={<Loading />}><DashboardPage /></Suspense>,
          },
          {
            path: 'projects',
            element: <Suspense fallback={<Loading />}><ProjectListPage /></Suspense>,
          },
          {
            path: 'projects/new',
            element: (
              <Suspense fallback={<Loading />}><ProjectFormPage /></Suspense>
            ),
          },
          {
            path: 'projects/:id',
            element: <Suspense fallback={<Loading />}><ProjectDetailPage /></Suspense>,
          },
        ],
      },
      {
        element: (
          <RoleGuard roles={['ADMIN']} />
        ),
        children: [
          {
            element: <AdminLayout />,
            children: [
              { path: 'admin/users', element: <Suspense fallback={<Loading />}><UserManagementPage /></Suspense> },
            ],
          },
        ],
      },
    ],
  },
])

export function AppRouter() {
  return <RouterProvider router={router} />
}
