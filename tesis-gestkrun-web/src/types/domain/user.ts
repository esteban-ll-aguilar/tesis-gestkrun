import type { Rol } from './auth'

export interface UserListItem {
  id: string
  nombre: string
  email: string
  rol: Rol
  fechaRegistro: string
}
