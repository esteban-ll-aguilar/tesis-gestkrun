import { useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  DndContext, DragOverlay, DragStartEvent, DragEndEvent, PointerSensor, useSensor, useSensors,
} from '@dnd-kit/core';
import { boardService, KanbanTaskDTO, BoardDTO } from '../features/boards/boardService';
import { ArrowLeft, AlertTriangle, Lock, Unlock } from 'lucide-react';

const COLUMNS = ['PENDIENTE', 'EN_PROCESO', 'BLOQUEADO', 'EN_REVISION', 'TERMINADO', 'CANCELADO'];

const COLUMN_TITLES: Record<string, string> = {
  PENDIENTE: 'Pendiente',
  EN_PROCESO: 'En Proceso',
  BLOQUEADO: 'Bloqueado',
  EN_REVISION: 'En Revisión',
  TERMINADO: 'Terminado',
  CANCELADO: 'Cancelado',
};

const WIP_LIMIT = 3;

export default function BoardPage() {
  const { id: projectId, sprintId } = useParams<{ id: string; sprintId: string }>();
  const queryClient = useQueryClient();
  const [activeTask, setActiveTask] = useState<KanbanTaskDTO | null>(null);
  const [taskModal, setTaskModal] = useState<KanbanTaskDTO | null>(null);
  const [blockModal, setBlockModal] = useState<string | null>(null);

  const { data: board, isLoading } = useQuery({
    queryKey: ['board', sprintId],
    queryFn: () => boardService.getBoard(sprintId!),
    enabled: !!sprintId,
  });

  const transitionMutation = useMutation({
    mutationFn: ({ taskId, toEstado }: { taskId: string; toEstado: string }) =>
      boardService.transitionTask(taskId, toEstado),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['board', sprintId] }),
  });

  const blockMutation = useMutation({
    mutationFn: ({ taskId, reason }: { taskId: string; reason: string }) =>
      boardService.blockTask(taskId, reason),
    onSuccess: () => { queryClient.invalidateQueries({ queryKey: ['board', sprintId] }); setBlockModal(null); },
  });

  const unblockMutation = useMutation({
    mutationFn: (taskId: string) => boardService.unblockTask(taskId),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['board', sprintId] }),
  });

  const sensors = useSensors(
    useSensor(PointerSensor, { activationConstraint: { distance: 8 } })
  );

  if (isLoading || !board) return <div className="p-6">Cargando tablero...</div>;

  const handleDragStart = (event: DragStartEvent) => {
    const task = findTask(board, event.active.id as string);
    setActiveTask(task || null);
  };

  const handleDragEnd = (event: DragEndEvent) => {
    setActiveTask(null);
    const { active, over } = event;
    if (!over) return;

    const taskId = active.id as string;
    const targetColumn = over.id as string;

    if (!COLUMNS.includes(targetColumn)) return;
    if (targetColumn === 'EN_PROCESO') {
      const inProgressCount = board.columns['EN_PROCESO']?.items?.length || 0;
      if (inProgressCount >= WIP_LIMIT) return;
    }

    transitionMutation.mutate({ taskId, toEstado: targetColumn });
  };

  const inProgressCount = board.columns['EN_PROCESO']?.items?.length || 0;
  const wipWarning = inProgressCount >= WIP_LIMIT;
  const wipYellow = inProgressCount >= 2;

  return (
    <div className="p-6">
      <Link to={`/projects/${projectId}/sprints/${sprintId}`} className="text-blue-600 flex items-center gap-1 mb-4 hover:underline">
        <ArrowLeft size={16} /> Volver al sprint
      </Link>

      <div className="flex items-center justify-between mb-4">
        <h1 className="text-2xl font-bold">Tablero Kanban</h1>
        <div className="flex items-center gap-2">
          {wipYellow && !wipWarning && (
            <span className="flex items-center gap-1 text-yellow-600 bg-yellow-50 px-3 py-1 rounded text-sm">
              <AlertTriangle size={14} /> WIP: {inProgressCount}/{WIP_LIMIT}
            </span>
          )}
          {wipWarning && (
            <span className="flex items-center gap-1 text-red-600 bg-red-50 px-3 py-1 rounded text-sm font-medium">
              <AlertTriangle size={14} /> WIP Límite alcanzado ({inProgressCount}/{WIP_LIMIT})
            </span>
          )}
        </div>
      </div>

      <div className="flex gap-4 overflow-x-auto pb-4">
        <DndContext sensors={sensors} onDragStart={handleDragStart} onDragEnd={handleDragEnd}>
          {COLUMNS.map(col => (
            <div key={col} className="flex-shrink-0 w-64 bg-gray-100 rounded-lg p-3">
              <div className="flex items-center justify-between mb-3">
                <h3 className="font-semibold text-sm text-gray-700">{COLUMN_TITLES[col]}</h3>
                <span className="text-xs text-gray-500 bg-white px-2 py-0.5 rounded-full">
                  {board.columns[col]?.count || 0}
                </span>
              </div>

              <div className="space-y-2 min-h-[200px]">
                {(board.columns[col]?.items || []).map(task => (
                  <div
                    key={task.id}
                    className={`bg-white rounded-lg shadow-sm border p-3 cursor-grab active:cursor-grabbing hover:shadow-md transition ${
                      task.estado === 'BLOQUEADO' ? 'border-red-300 bg-red-50' : 'border-gray-200'
                    }`}
                    onClick={() => setTaskModal(task)}
                  >
                    <div className="flex items-start justify-between">
                      <p className="text-sm font-medium">{task.titulo}</p>
                      {task.estado === 'BLOQUEADO' && <Lock size={14} className="text-red-500 shrink-0" />}
                    </div>
                    {task.assigned_to && (
                      <p className="text-xs text-gray-500 mt-1">
                        {task.assigned_to.slice(0, 8)}...
                      </p>
                    )}
                  </div>
                ))}
              </div>
            </div>
          ))}

          <DragOverlay>
            {activeTask && (
              <div className="bg-white rounded-lg shadow-lg border border-blue-300 p-3 w-64">
                <p className="text-sm font-medium">{activeTask.titulo}</p>
              </div>
            )}
          </DragOverlay>
        </DndContext>
      </div>

      {taskModal && (
        <TaskDetailModal
          task={taskModal}
          onClose={() => setTaskModal(null)}
          onBlock={() => { setBlockModal(taskModal.id); setTaskModal(null); }}
          onUnblock={() => { unblockMutation.mutate(taskModal.id); setTaskModal(null); }}
        />
      )}

      {blockModal && (
        <BlockModal
          taskId={blockModal}
          onClose={() => setBlockModal(null)}
          onConfirm={(reason) => blockMutation.mutate({ taskId: blockModal, reason })}
        />
      )}
    </div>
  );
}

function TaskDetailModal({ task, onClose, onBlock, onUnblock }: {
  task: KanbanTaskDTO; onClose: () => void; onBlock: () => void; onUnblock: () => void;
}) {
  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50" onClick={onClose}>
      <div className="bg-white rounded-lg p-6 w-full max-w-md" onClick={e => e.stopPropagation()}>
        <h2 className="text-lg font-semibold mb-2">{task.titulo}</h2>
        <p className="text-gray-600 text-sm mb-4">{task.descripcion}</p>
        <div className="space-y-2 text-sm text-gray-600 mb-4">
          <p><strong>Estado:</strong> {task.estado}</p>
          {task.assigned_to && <p><strong>Asignado a:</strong> {task.assigned_to}</p>}
          {task.fecha_limite && <p><strong>Fecha límite:</strong> {task.fecha_limite}</p>}
        </div>
        <div className="flex gap-2">
          {task.estado !== 'BLOQUEADO' && task.estado !== 'TERMINADO' && task.estado !== 'CANCELADO' && (
            <button onClick={onBlock} className="bg-red-600 text-white px-3 py-1.5 rounded text-sm hover:bg-red-700 flex items-center gap-1">
              <Lock size={14} /> Bloquear
            </button>
          )}
          {task.estado === 'BLOQUEADO' && (
            <button onClick={onUnblock} className="bg-green-600 text-white px-3 py-1.5 rounded text-sm hover:bg-green-700 flex items-center gap-1">
              <Unlock size={14} /> Desbloquear
            </button>
          )}
          <button onClick={onClose} className="px-3 py-1.5 rounded border text-sm hover:bg-gray-100">Cerrar</button>
        </div>
      </div>
    </div>
  );
}

function BlockModal({ onClose, onConfirm }: { onClose: () => void; onConfirm: (reason: string) => void }) {
  const [reason, setReason] = useState('');
  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50" onClick={onClose}>
      <div className="bg-white rounded-lg p-6 w-full max-w-md" onClick={e => e.stopPropagation()}>
        <h2 className="text-lg font-semibold mb-4">Bloquear Tarea</h2>
        <textarea
          value={reason}
          onChange={e => setReason(e.target.value)}
          placeholder="Motivo del bloqueo..."
          className="w-full p-2 border rounded mb-4"
          rows={3}
        />
        <div className="flex gap-2">
          <button onClick={() => onConfirm(reason)} disabled={!reason} className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700 disabled:bg-gray-300">Confirmar</button>
          <button onClick={onClose} className="px-4 py-2 rounded border hover:bg-gray-100">Cancelar</button>
        </div>
      </div>
    </div>
  );
}

function findTask(board: BoardDTO, taskId: string): KanbanTaskDTO | undefined {
  for (const col of Object.values(board.columns)) {
    const found = col.items.find(t => t.id === taskId);
    if (found) return found;
  }
  return undefined;
}
