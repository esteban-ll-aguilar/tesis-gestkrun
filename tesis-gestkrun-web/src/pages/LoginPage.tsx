import { useForm } from 'react-hook-form'
import { useNavigate } from 'react-router-dom'
import { useAuthStore } from '../stores/auth'

type LoginForm = {
  email: string
  password: string
}

export default function LoginPage() {
  const navigate = useNavigate()
  const setAuth = useAuthStore((s) => s.setAuth)
  const {
    register, handleSubmit, setError, formState: { errors, isSubmitting },
  } = useForm<LoginForm>()

  const onSubmit = async (data: LoginForm) => {
    try {
      const res = await fetch('/api/v1/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
        credentials: 'include',
      })
      if (!res.ok) {
        throw new Error('Credenciales inválidas')
      }
      const json = await res.json()
      const userRes = await fetch('/api/v1/auth/me', {
        headers: { Authorization: `Bearer ${json.accessToken}` },
      })
      if (!userRes.ok) throw new Error('Error al obtener usuario')
      const user = await userRes.json()
      setAuth(user, json.accessToken)
      navigate('/dashboard')
    } catch {
      setError('root', { message: 'Credenciales inválidas' })
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <h2 className="text-2xl font-bold text-center">Iniciar sesión</h2>
      {errors.root && <p className="text-red-500 text-sm">{errors.root.message}</p>}
      <div>
        <label className="block text-sm font-medium mb-1">Email</label>
        <input type="email" {...register('email')} className="w-full border rounded px-3 py-2" />
        {errors.email && <p className="text-red-500 text-xs mt-1">{errors.email.message}</p>}
      </div>
      <div>
        <label className="block text-sm font-medium mb-1">Contraseña</label>
        <input type="password" {...register('password')} className="w-full border rounded px-3 py-2" />
        {errors.password && <p className="text-red-500 text-xs mt-1">{errors.password.message}</p>}
      </div>
      <button
        type="submit" disabled={isSubmitting}
        className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 disabled:opacity-50"
      >
        {isSubmitting ? 'Ingresando...' : 'Ingresar'}
      </button>
      <p className="text-sm text-center space-x-2">
        <a href="/register" className="text-blue-600">Registrarse</a>
        <span>|</span>
        <a href="/recover-password" className="text-blue-600">Recuperar contraseña</a>
      </p>
    </form>
  )
}
