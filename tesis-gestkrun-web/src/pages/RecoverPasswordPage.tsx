import { useState } from 'react'

export default function RecoverPasswordPage() {
  const [email, setEmail] = useState('')
  const [sent, setSent] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    await fetch('/api/v1/auth/recover-password', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email }),
    })
    setSent(true)
  }

  if (sent) {
    return (
      <div className="text-center space-y-4">
        <h2 className="text-2xl font-bold">Correo enviado</h2>
        <p className="text-gray-600">
          Si el email está registrado, recibirás instrucciones para recuperar tu contraseña.
        </p>
        <a href="/login" className="text-blue-600">Volver al inicio</a>
      </div>
    )
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <h2 className="text-2xl font-bold text-center">Recuperar contraseña</h2>
      <div>
        <label className="block text-sm font-medium mb-1">Email</label>
        <input
          type="email" required value={email} onChange={e => setEmail(e.target.value)}
          className="w-full border rounded px-3 py-2"
        />
      </div>
      <button type="submit" className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700">
        Enviar
      </button>
      <p className="text-sm text-center">
        <a href="/login" className="text-blue-600">Volver</a>
      </p>
    </form>
  )
}
