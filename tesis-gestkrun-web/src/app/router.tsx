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
const BacklogPage = lazy(() => import('../pages/BacklogPage'))
const SprintListPage = lazy(() => import('../pages/SprintListPage'))
const SprintPlanningPage = lazy(() => import('../pages/SprintPlanningPage'))
const SprintDetailPage = lazy(() => import('../pages/SprintDetailPage'))
const BoardPage = lazy(() => import('../pages/BoardPage'))
const ChatPage = lazy(() => import('../pages/ChatPage'))
const ArtifactsPage = lazy(() => import('../pages/ArtifactsPage'))

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
          {
            path: 'projects/:id/backlog',
            element: <Suspense fallback={<Loading />}><BacklogPage /></Suspense>,
          },
          {
            path: 'projects/:id/sprints',
            element: <Suspense fallback={<Loading />}><SprintListPage /></Suspense>,
          },
          {
            path: 'projects/:id/sprints/plan',
            element: <Suspense fallback={<Loading />}><SprintPlanningPage /></Suspense>,
          },
          {
            path: 'projects/:id/sprints/:sprintId',
            element: <Suspense fallback={<Loading />}><SprintDetailPage /></Suspense>,
          },
          {
            path: 'projects/:id/sprints/:sprintId/board',
            element: <Suspense fallback={<Loading />}><BoardPage /></Suspense>,
          },
          {
            path: 'projects/:id/chat',
            element: <Suspense fallback={<Loading />}><ChatPage /></Suspense>,
          },
          {
            path: 'projects/:id/artifacts/:taskId',
            element: <Suspense fallback={<Loading />}><ArtifactsPage /></Suspense>,
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
