import { http } from '../../services/http';

export interface MessageDTO {
  id: string;
  contenido: string;
  sender_id: string;
  tipo: string;
  fecha_envio: string;
}

export interface PaginatedMessages {
  data: MessageDTO[];
  next_cursor: string | null;
}

export const chatService = {
  listMessages: (projectId: string, cursor?: string) =>
    http.get<PaginatedMessages>(`/projects/${projectId}/messages`, {
      params: { cursor, limit: 50 },
    }).then(r => r.data),

  sendMessage: (projectId: string, contenido: string, tipo = 'PROYECTO') =>
    http.post<MessageDTO>(`/projects/${projectId}/messages`, { contenido, tipo }).then(r => r.data),
};
