import { useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  DndContext, DragOverlay, useDraggable, useDroppable, PointerSensor, useSensor, useSensors,
} from '@dnd-kit/core';
import type { DragStartEvent, DragEndEvent } from '@dnd-kit/core';
import { boardService } from '../features/boards/boardService';
import { projectService, type AssignmentDTO } from '../features/projects/projectService';
import type { KanbanTaskDTO, BoardDTO } from '../features/boards/boardService';
import { ArrowLeft, AlertTriangle, Lock, Unlock, User } from 'lucide-react';
import { useAuthStore } from '../stores/auth';
import { canTransition, type EstadoTarea } from '../types/domain/task';

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

function DraggableTask({ task, onClick, userMap, canDrag }: { task: KanbanTaskDTO; onClick: () => void; userMap: Record<string, string>; canDrag: boolean }) {
  const { attributes, listeners, setNodeRef, transform, isDragging } = useDraggable({ id: task.id });
  const style = transform ? {
    transform: `translate3d(${transform.x}px, ${transform.y}px, 0)`,
  } : undefined;
  const dragProps = canDrag ? { ...listeners, ...attributes } : {};

  return (
    <div
      ref={setNodeRef}
      {...dragProps}
      style={style}
      onClick={onClick}
      className={`bg-white rounded-lg shadow-sm border p-3 ${canDrag ? 'cursor-grab active:cursor-grabbing' : ''} hover:shadow-md transition ${
        isDragging ? 'opacity-50' : ''
      } ${task.estado === 'BLOQUEADO' ? 'border-red-300 bg-red-50' : 'border-gray-200'}`}
    >
      <div className="flex items-start justify-between">
        <p className="text-sm font-medium">{task.titulo}</p>
        {task.estado === 'BLOQUEADO' && <Lock size={14} className="text-red-500 shrink-0" />}
      </div>
      {task.assigned_to && (
        <p className="text-xs text-gray-500 mt-1 truncate flex items-center gap-1">
          <User size={12} /> {userMap[task.assigned_to] || task.assigned_to.slice(0, 8)}
        </p>
      )}
    </div>
  );
}

function DroppableColumn({ id, children, count, title, wipWarning }: {
  id: string; children: React.ReactNode; count: number; title: string; wipWarning?: boolean;
}) {
  const { setNodeRef, isOver } = useDroppable({ id });

  return (
    <div
      ref={setNodeRef}
      className={`flex-shrink-0 w-64 bg-gray-100 rounded-lg p-3 transition-colors ${
        isOver ? 'bg-blue-50 ring-2 ring-blue-300' : ''
      }`}
    >
      <div className="flex items-center justify-between mb-3">
        <h3 className="font-semibold text-sm text-gray-700">{title}</h3>
        <span className={`text-xs px-2 py-0.5 rounded-full ${
          wipWarning ? 'bg-red-100 text-red-700' :
          count >= 2 ? 'bg-yellow-100 text-yellow-700' :
          'bg-white text-gray-500'
        }`}>
          {count}
        </span>
      </div>
      <div className="space-y-2 min-h-[200px]">
        {children}
      </div>
    </div>
  );
}

export default function BoardPage() {
  const { id: projectId, sprintId } = useParams<{ id: string; sprintId: string }>();
  const queryClient = useQueryClient();
  const currentUser = useAuthStore((s) => s.user);
  const [activeTask, setActiveTask] = useState<KanbanTaskDTO | null>(null);
  const [taskModal, setTaskModal] = useState<KanbanTaskDTO | null>(null);
  const [blockModal, setBlockModal] = useState<string | null>(null);
  const [error, setError] = useState('');

  const { data: board, isLoading } = useQuery({
    queryKey: ['board', sprintId],
    queryFn: () => boardService.getBoard(sprintId!),
    enabled: !!sprintId,
  });

  const { data: assignments = [] } = useQuery({
    queryKey: ['assignments', projectId],
    queryFn: () => projectService.listAssignments(projectId!),
    enabled: !!projectId,
  });

  const transitionMutation = useMutation({
    mutationFn: ({ taskId, toEstado }: { taskId: string; toEstado: string }) =>
      boardService.transitionTask(taskId, toEstado),
    onSuccess: () => { queryClient.invalidateQueries({ queryKey: ['board', sprintId] }); setError(''); },
    onError: (e: Error) => setError(e.message),
  });

  const assignMutation = useMutation({
    mutationFn: ({ taskId, userId }: { taskId: string; userId: string }) =>
      boardService.assignTask(taskId, userId),
    onSuccess: () => { queryClient.invalidateQueries({ queryKey: ['board', sprintId] }); setError(''); },
    onError: (e: Error) => setError(e.message),
  });

  const blockMutation = useMutation({
    mutationFn: ({ taskId, reason }: { taskId: string; reason: string }) =>
      boardService.blockTask(taskId, reason),
    onSuccess: () => { queryClient.invalidateQueries({ queryKey: ['board', sprintId] }); setBlockModal(null); setError(''); },
    onError: (e: Error) => setError(e.message),
  });

  const unblockMutation = useMutation({
    mutationFn: (taskId: string) => boardService.unblockTask(taskId),
    onSuccess: () => { queryClient.invalidateQueries({ queryKey: ['board', sprintId] }); setError(''); },
    onError: (e: Error) => setError(e.message),
  });

  const sensors = useSensors(
    useSensor(PointerSensor, { activationConstraint: { distance: 8 } })
  );

  if (isLoading || !board) return <div className="p-6">Cargando tablero...</div>;

  const userMap = Object.fromEntries(assignments.map(a => [a.user_id, a.nombre || a.email || a.user_id]));
  const isAdmin = currentUser?.rol === 'ADMIN';
  const canDragTask = (task: KanbanTaskDTO): boolean => isAdmin || (!!currentUser && task.assigned_to === currentUser.id);

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

    const task = findTask(board, taskId);
    if (!task || task.estado === targetColumn) return;

    if (!canDragTask(task)) {
      setError('Solo el desarrollador asignado puede mover esta tarea');
      return;
    }

    if (!canTransition(task.estado as EstadoTarea, targetColumn as EstadoTarea)) {
      setError(`Transición inválida: de ${task.estado} a ${targetColumn}`);
      return;
    }

    transitionMutation.mutate({ taskId, toEstado: targetColumn });
  };

  const inProgressCount = board.columns['EN_PROCESO']?.items?.length || 0;
  const wipWarning = inProgressCount >= WIP_LIMIT;

  return (
    <div className="p-6">
      <Link to={`/projects/${projectId}/sprints/${sprintId}`} className="text-blue-600 flex items-center gap-1 mb-4 hover:underline">
        <ArrowLeft size={16} /> Volver al sprint
      </Link>

      <div className="flex items-center justify-between mb-4">
        <h1 className="text-2xl font-bold">Tablero Kanban</h1>
        {wipWarning && (
          <span className="flex items-center gap-1 text-red-600 bg-red-50 px-3 py-1 rounded text-sm font-medium">
            <AlertTriangle size={14} /> WIP Límite alcanzado ({inProgressCount}/{WIP_LIMIT})
          </span>
        )}
      </div>

      {error && <p className="text-red-500 text-sm mb-4">{error}</p>}

      <div className="flex gap-4 overflow-x-auto pb-4">
        <DndContext sensors={sensors} onDragStart={handleDragStart} onDragEnd={handleDragEnd}>
          {COLUMNS.map(col => (
            <DroppableColumn key={col} id={col} title={COLUMN_TITLES[col]} count={board.columns[col]?.count || 0} wipWarning={col === 'EN_PROCESO' && wipWarning}>
              {(board.columns[col]?.items || []).map(task => (
                <DraggableTask key={task.id} task={task} userMap={userMap} canDrag={canDragTask(task)} onClick={() => setTaskModal(task)} />
              ))}
            </DroppableColumn>
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
          assignments={assignments}
          userMap={userMap}
          onClose={() => setTaskModal(null)}
          onAssign={(userId) => { assignMutation.mutate({ taskId: taskModal.id, userId }); }}
          onBlock={() => { setBlockModal(taskModal.id); setTaskModal(null); }}
          onUnblock={() => { unblockMutation.mutate(taskModal.id); setTaskModal(null); }}
        />
      )}

      {blockModal && (
        <BlockModal
          onClose={() => setBlockModal(null)}
          onConfirm={(reason) => blockMutation.mutate({ taskId: blockModal, reason })}
        />
      )}
    </div>
  );
}

function TaskDetailModal({ task, assignments, userMap, onClose, onAssign, onBlock, onUnblock }: {
  task: KanbanTaskDTO; assignments: AssignmentDTO[]; userMap: Record<string, string>; onClose: () => void;
  onAssign: (userId: string) => void; onBlock: () => void; onUnblock: () => void;
}) {
  const [assignId, setAssignId] = useState(task.assigned_to || '');
  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50" onClick={onClose}>
      <div className="bg-white rounded-lg p-6 w-full max-w-md" onClick={e => e.stopPropagation()}>
        <h2 className="text-lg font-semibold mb-2">{task.titulo}</h2>
        <p className="text-gray-600 text-sm mb-4">{task.descripcion}</p>
        <div className="space-y-3 text-sm text-gray-600 mb-4">
          <p><strong>Estado:</strong> {task.estado.replace(/_/g, ' ')}</p>
          {task.assigned_to && <p><strong>Asignado a:</strong> {userMap[task.assigned_to] || task.assigned_to}</p>}
          <div>
            <label className="text-xs text-gray-500 block mb-1"><strong>Cambiar asignación:</strong></label>
            <div className="flex gap-2">
              <select value={assignId} onChange={e => setAssignId(e.target.value)} className="flex-1 p-2 border rounded text-sm">
                <option value="">Sin asignar</option>
                {assignments.map(a => (
                  <option key={a.user_id} value={a.user_id}>{a.nombre || a.email}</option>
                ))}
              </select>
              <button
                onClick={() => { if (assignId) onAssign(assignId); }}
                disabled={!assignId || assignId === task.assigned_to}
                className="bg-blue-600 text-white px-3 py-1.5 rounded text-sm hover:bg-blue-700 disabled:bg-gray-300"
              >
                Asignar
              </button>
            </div>
          </div>
          {task.fecha_limite && <p><strong>Fecha límite:</strong> {task.fecha_limite}</p>}
        </div>
        <div className="flex gap-2">
          {canTransition(task.estado as EstadoTarea, 'BLOQUEADO') && (
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
