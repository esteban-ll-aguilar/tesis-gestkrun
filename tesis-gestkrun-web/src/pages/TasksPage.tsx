import { useState } from 'react';
import { useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { taskService } from '../features/tasks/taskService';
import { backlogService } from '../features/backlog/backlogService';
import { projectService } from '../features/projects/projectService';
import { Filter } from 'lucide-react';

const COLORS: Record<string, string> = {
  PENDIENTE: 'bg-gray-100 text-gray-700',
  EN_PROCESO: 'bg-blue-100 text-blue-700',
  BLOQUEADO: 'bg-red-100 text-red-700',
  EN_REVISION: 'bg-yellow-100 text-yellow-700',
  TERMINADO: 'bg-green-100 text-green-700',
  CANCELADO: 'bg-gray-100 text-gray-500',
};

export default function TasksPage() {
  const { id: projectId } = useParams<{ id: string }>();
  const [sprintFilter, setSprintFilter] = useState('');
  const [devFilter, setDevFilter] = useState('');

  const { data: tasks, isLoading } = useQuery({
    queryKey: ['tasks', projectId, sprintFilter, devFilter],
    queryFn: () => taskService.listTasks(projectId!, {
      ...(sprintFilter ? { sprint_id: sprintFilter } : {}),
      ...(devFilter ? { assigned_to: devFilter } : {}),
    }),
    enabled: !!projectId,
  });

  const { data: sprints = [] } = useQuery({
    queryKey: ['sprints', projectId],
    queryFn: () => backlogService.listSprints(projectId!),
    enabled: !!projectId,
  });

  const { data: assignments = [] } = useQuery({
    queryKey: ['assignments', projectId],
    queryFn: () => projectService.listAssignments(projectId!),
    enabled: !!projectId,
  });

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">Tareas del Proyecto</h1>

      <div className="flex gap-4 mb-6 p-4 bg-white rounded-lg shadow border border-gray-200">
        <div className="flex items-center gap-2">
          <Filter size={16} className="text-gray-400" />
          <select value={sprintFilter} onChange={e => setSprintFilter(e.target.value)} className="border rounded px-2 py-1.5 text-sm">
            <option value="">Todos los sprints</option>
            {sprints.map(s => (
              <option key={s.id} value={s.id}>{s.nombre}</option>
            ))}
          </select>
        </div>
        <select value={devFilter} onChange={e => setDevFilter(e.target.value)} className="border rounded px-2 py-1.5 text-sm">
          <option value="">Todos los desarrolladores</option>
          {assignments.filter(a => a.rol === 'DEVELOPER' || a.rol === 'SCRUM_MASTER').map(a => (
            <option key={a.user_id} value={a.user_id}>{a.nombre || a.email}</option>
          ))}
        </select>
      </div>

      {isLoading ? (
        <div className="p-6">Cargando tareas...</div>
      ) : !tasks || tasks.length === 0 ? (
        <p className="text-gray-500">No hay tareas en este proyecto.</p>
      ) : (
        <div className="bg-white rounded-lg shadow border border-gray-200 overflow-hidden">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-gray-50 border-b">
                <th className="text-left p-3 font-medium">Título</th>
                <th className="text-left p-3 font-medium">Estado</th>
                <th className="text-left p-3 font-medium">Asignado a</th>
                <th className="text-left p-3 font-medium">Creado</th>
              </tr>
            </thead>
            <tbody>
              {tasks.map(t => {
                const user = assignments.find(a => a.user_id === t.assigned_to);
                return (
                  <tr key={t.id} className="border-b hover:bg-gray-50">
                    <td className="p-3 font-medium">{t.titulo}</td>
                    <td className="p-3">
                      <span className={`px-2 py-0.5 rounded text-xs font-medium ${COLORS[t.estado] || ''}`}>
                        {t.estado.replace(/_/g, ' ')}
                      </span>
                    </td>
                    <td className="p-3 text-gray-600">{user?.nombre || t.assigned_to?.slice(0, 8) || '—'}</td>
                    <td className="p-3 text-gray-500">{t.fecha_creacion.slice(0, 10)}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
