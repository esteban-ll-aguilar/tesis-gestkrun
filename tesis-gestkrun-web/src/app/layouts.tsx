import { Outlet } from 'react-router-dom'

export function MainLayout() {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b px-6 py-3 flex items-center justify-between">
        <h1 className="text-xl font-bold">GESTKRUN</h1>
        <nav className="flex gap-4">
          <a href="/dashboard" className="text-sm text-gray-600 hover:text-gray-900">Dashboard</a>
          <a href="/projects" className="text-sm text-gray-600 hover:text-gray-900">Proyectos</a>
        </nav>
      </header>
      <main className="p-6">
        <Outlet />
      </main>
    </div>
  )
}

export function AuthLayout() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="w-full max-w-md p-8 bg-white rounded-lg shadow">
        <Outlet />
      </div>
    </div>
  )
}

export function AdminLayout() {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b px-6 py-3">
        <h1 className="text-xl font-bold">Administración</h1>
      </header>
      <main className="p-6">
        <Outlet />
      </main>
    </div>
  )
}
