export type Rol = 'ADMIN' | 'PRODUCT_OWNER' | 'SCRUM_MASTER' | 'DEVELOPER'

export interface User {
  id: string
  nombre: string
  email: string
  rol: Rol
  fechaRegistro: string
}
