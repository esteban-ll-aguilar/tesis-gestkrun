type BadgeVariant = 'default' | 'success' | 'warning' | 'danger' | 'info'

interface BadgeProps {
  children: React.ReactNode
  variant?: BadgeVariant
}

const variantClasses: Record<BadgeVariant, string> = {
  default: 'bg-gray-100 text-gray-800',
  success: 'bg-green-100 text-green-800',
  warning: 'bg-yellow-100 text-yellow-800',
  danger: 'bg-red-100 text-red-800',
  info: 'bg-blue-100 text-blue-800',
}

export function Badge({ children, variant = 'default' }: BadgeProps) {
  return (
    <span className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${variantClasses[variant]}`}>
      {children}
    </span>
  )
}

export function EstadoTareaBadge({ estado }: { estado: string }) {
  const variantMap: Record<string, BadgeVariant> = {
    PENDIENTE: 'default',
    EN_PROCESO: 'info',
    BLOQUEADO: 'danger',
    EN_REVISION: 'warning',
    TERMINADO: 'success',
    CANCELADO: 'default',
  }
  return <Badge variant={variantMap[estado] ?? 'default'}>{estado}</Badge>
}

export function PrioridadBadge({ prioridad }: { prioridad: string }) {
  const variantMap: Record<string, BadgeVariant> = {
    BAJA: 'default',
    MEDIA: 'info',
    ALTA: 'warning',
    CRITICA: 'danger',
  }
  return <Badge variant={variantMap[prioridad] ?? 'default'}>{prioridad}</Badge>
}

export function EstadoSprintBadge({ estado }: { estado: string }) {
  const variantMap: Record<string, BadgeVariant> = {
    PLANIFICADO: 'info',
    EN_EJECUCION: 'warning',
    FINALIZADO: 'success',
    CANCELADO: 'default',
  }
  return <Badge variant={variantMap[estado] ?? 'default'}>{estado}</Badge>
}
