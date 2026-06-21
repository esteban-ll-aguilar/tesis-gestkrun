import http from '../../services/http';

export interface KanbanTaskDTO {
  id: string;
  titulo: string;
  descripcion: string;
  estado: string;
  assigned_to: string | null;
  fecha_limite: string | null;
  fecha_creacion: string;
}

export interface BoardColumn {
  items: KanbanTaskDTO[];
  count: number;
}

export interface BoardDTO {
  sprint_id: string;
  columns: Record<string, BoardColumn>;
}

export const boardService = {
  getBoard: (sprintId: string) =>
    http.get<BoardDTO>(`/boards/${sprintId}`).then(r => r.data),

  transitionTask: (taskId: string, to_estado: string, reason?: string) =>
    http.patch<{ id: string; estado: string; transition: { from: string; to: string; timestamp: string } }>(
      `/boards/tasks/${taskId}/transition`, { to_estado, reason }
    ).then(r => r.data),

  assignTask: (taskId: string, userId: string) =>
    http.patch<{ id: string; assigned_to: string }>(
      `/boards/tasks/${taskId}/assign`, { user_id: userId }
    ).then(r => r.data),

  blockTask: (taskId: string, reason: string) =>
    http.patch<{ id: string; estado: string; blocked: boolean }>(
      `/boards/tasks/${taskId}/block`, { reason }
    ).then(r => r.data),

  unblockTask: (taskId: string) =>
    http.patch<{ id: string; estado: string; blocked: boolean }>(
      `/boards/tasks/${taskId}/unblock`
    ).then(r => r.data),
};
