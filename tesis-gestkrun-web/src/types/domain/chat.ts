export type TipoMensaje = 'PROYECTO' | 'TAREA'

export interface Message {
  id: string
  proyecto_id: string | null
  task_id: string | null
  sender_id: string
  contenido: string
  fecha_envio: string
  tipo: TipoMensaje
}
