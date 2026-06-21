import { useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { backlogService } from '../features/backlog/backlogService';
import { Play, Square, Calendar, Clock, ArrowLeft } from 'lucide-react';

export default function SprintDetailPage() {
  const { id: projectId, sprintId } = useParams<{ id: string; sprintId: string }>();
  const queryClient = useQueryClient();
  const [showEventForm, setShowEventForm] = useState(false);

  const { data: sprint, isLoading } = useQuery({
    queryKey: ['sprint', projectId, sprintId],
    queryFn: () => backlogService.getSprint(projectId!, sprintId!),
    enabled: !!projectId && !!sprintId,
  });

  const { data: eventos } = useQuery({
    queryKey: ['sprint-eventos', sprintId],
    queryFn: () => backlogService.listEventos(projectId!, sprintId!),
    enabled: !!projectId && !!sprintId,
  });

  const [error, setError] = useState('');

  const startMutation = useMutation({
    mutationFn: () => backlogService.startSprint(projectId!, sprintId!),
    onSuccess: () => { queryClient.invalidateQueries({ queryKey: ['sprint', projectId, sprintId] }); setError(''); },
    onError: (e: Error) => setError(e.message),
  });

  const closeMutation = useMutation({
    mutationFn: () => backlogService.closeSprint(projectId!, sprintId!),
    onSuccess: () => { queryClient.invalidateQueries({ queryKey: ['sprint', projectId, sprintId] }); setError(''); },
    onError: (e: Error) => setError(e.message),
  });

  if (isLoading || !sprint) return <div className="p-6">Cargando sprint...</div>;

  const isActive = sprint.estado === 'EN_EJECUCION';
  const isPlanned = sprint.estado === 'PLANIFICADO';

  return (
    <div className="p-6 max-w-5xl mx-auto">
      <Link to={`/projects/${projectId}/sprints`} className="text-blue-600 flex items-center gap-1 mb-4 hover:underline">
        <ArrowLeft size={16} /> Volver a sprints
      </Link>

      <div className="bg-white rounded-lg shadow border border-gray-200 p-6 mb-6">
        <div className="flex justify-between items-start">
          <div>
            <h1 className="text-2xl font-bold">{sprint.nombre}</h1>
            <p className="text-gray-500 mt-1">{sprint.objetivo}</p>
              <div className="flex items-center gap-4 mt-3 text-sm text-gray-600">
                <span className="flex items-center gap-1"><Calendar size={14} /> {sprint.fecha_inicio} → {sprint.fecha_fin}</span>
                <span className="flex items-center gap-1"><Clock size={14} /> {sprint.duracion_dias} días</span>
                {sprint.meeting_link && (
                  <a href={sprint.meeting_link} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">
                    Link reunión
                  </a>
                )}
              </div>
          </div>
          <div className="flex items-center gap-2">
            <span className={`px-3 py-1 rounded text-sm font-medium ${
              sprint.estado === 'EN_EJECUCION' ? 'bg-green-100 text-green-700' :
              sprint.estado === 'FINALIZADO' ? 'bg-blue-100 text-blue-700' :
              sprint.estado === 'CANCELADO' ? 'bg-red-100 text-red-700' :
              'bg-gray-100 text-gray-700'
            }`}>{sprint.estado}</span>
          </div>
        </div>

        <div className="flex gap-2 mt-4">
          {isPlanned && (
            <button onClick={() => startMutation.mutate()} disabled={startMutation.isPending} className="bg-green-600 text-white px-4 py-2 rounded flex items-center gap-2 hover:bg-green-700 disabled:bg-gray-300">
              <Play size={16} /> {startMutation.isPending ? 'Iniciando...' : 'Iniciar Sprint'}
            </button>
          )}
          {isActive && (
            <button onClick={() => closeMutation.mutate()} disabled={closeMutation.isPending} className="bg-blue-600 text-white px-4 py-2 rounded flex items-center gap-2 hover:bg-blue-700 disabled:bg-gray-300">
              <Square size={16} /> {closeMutation.isPending ? 'Cerrando...' : 'Cerrar Sprint'}
            </button>
          )}
          {isActive && (
            <Link to={`/projects/${projectId}/sprints/${sprintId}/board`} className="bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700">
              Ver Tablero
            </Link>
          )}
        </div>
        {error && <p className="text-red-500 text-sm mt-2">{error}</p>}
      </div>

      <div className="bg-white rounded-lg shadow border border-gray-200 p-6">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold">Eventos Scrum</h2>
          {isActive && (
            <button onClick={() => setShowEventForm(true)} className="bg-blue-600 text-white px-3 py-1.5 rounded text-sm hover:bg-blue-700">
              + Nuevo Evento
            </button>
          )}
        </div>

        {showEventForm && (
          <EventForm projectId={projectId!} sprintId={sprintId!} onClose={() => setShowEventForm(false)} onSuccess={() => { setShowEventForm(false); queryClient.invalidateQueries({ queryKey: ['sprint-eventos', sprintId] }); }} />
        )}

        <div className="space-y-2">
          {eventos?.map(e => (
            <div key={e.id} className="flex items-center gap-3 p-3 bg-gray-50 rounded">
              <span className="px-2 py-1 rounded text-xs font-medium bg-purple-100 text-purple-700">{e.tipo}</span>
              <span className="flex-1 text-sm">{e.notas}</span>
              <span className="text-xs text-gray-500">{e.fecha.slice(0, 10)}</span>
              <span className="text-xs text-gray-500">{e.duracion_minutos} min</span>
            </div>
          ))}
          {!eventos?.length && <p className="text-gray-500 text-sm">No hay eventos registrados.</p>}
        </div>
      </div>
    </div>
  );
}

function EventForm({ projectId, sprintId, onClose, onSuccess }: { projectId: string; sprintId: string; onClose: () => void; onSuccess: () => void }) {
  const [tipo, setTipo] = useState('DAILY_SCRUM');
  const [notas, setNotas] = useState('');
  const [duracion, setDuracion] = useState(15);
  const mutation = useMutation({
    mutationFn: () => backlogService.createEvento(projectId, sprintId, { tipo, notas, duracion_minutos: duracion }),
    onSuccess,
  });
  return (
    <div className="bg-gray-50 p-4 rounded mb-4 border">
      <select value={tipo} onChange={e => setTipo(e.target.value)} className="p-2 border rounded mb-2 w-full">
        <option value="SPRINT_PLANNING">Sprint Planning</option>
        <option value="DAILY_SCRUM">Daily Scrum</option>
        <option value="SPRINT_REVIEW">Sprint Review</option>
        <option value="SPRINT_RETROSPECTIVE">Sprint Retrospective</option>
      </select>
      <textarea value={notas} onChange={e => setNotas(e.target.value)} placeholder="Notas del evento" className="w-full p-2 border rounded mb-2" rows={3} />
      <input type="number" value={duracion} onChange={e => setDuracion(Number(e.target.value))} placeholder="Duración (min)" className="w-full p-2 border rounded mb-2" />
      <div className="flex gap-2">
        <button onClick={() => mutation.mutate()} disabled={mutation.isPending} className="bg-blue-600 text-white px-3 py-1.5 rounded text-sm hover:bg-blue-700">Guardar</button>
        <button onClick={onClose} className="px-3 py-1.5 rounded border text-sm hover:bg-gray-100">Cancelar</button>
      </div>
    </div>
  );
}
