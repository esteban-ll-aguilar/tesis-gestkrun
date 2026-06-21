import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { backlogService } from '../features/backlog/backlogService';
import type { HistoriaWithEpica } from '../features/backlog/backlogService';
import http from '../services/http';
import { ArrowLeft } from 'lucide-react';

interface ModuleDTO {
  id: string
  nombre: string
}

export default function SprintPlanningPage() {
  const { id: projectId } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const [nombre, setNombre] = useState('');
  const [objetivo, setObjetivo] = useState('');
  const [duracionDias, setDuracionDias] = useState(14);
  const [fechaInicio, setFechaInicio] = useState(new Date().toISOString().slice(0, 10));
  const [meetingLink, setMeetingLink] = useState('');
  const [selectedHistoriaIds, setSelectedHistoriaIds] = useState<Set<string>>(new Set());
  const [moduloFilter, setModuloFilter] = useState<string>('');

  const { data: backlog, isLoading } = useQuery({
    queryKey: ['backlog', projectId],
    queryFn: () => backlogService.getBacklog(projectId!),
    enabled: !!projectId,
  });

  const { data: modules = [] } = useQuery({
    queryKey: ['modules', projectId],
    queryFn: () => http.get<ModuleDTO[]>(`/projects/${projectId}/modules`).then(r => r.data),
    enabled: !!projectId,
  });

  const planMutation = useMutation({
    mutationFn: () => backlogService.planSprint(projectId!, {
      nombre,
      objetivo,
      duracion_dias: duracionDias,
      fecha_inicio: fechaInicio,
      historia_ids: Array.from(selectedHistoriaIds),
      meeting_link: meetingLink,
    }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['sprints', projectId] });
      navigate(`/projects/${projectId}/sprints`);
    },
  });

  if (isLoading || !backlog) return <div className="p-6">Cargando backlog...</div>;

  const filteredBacklog = moduloFilter
    ? backlog.map((item: HistoriaWithEpica) => ({
        ...item,
        historias: item.historias.filter(h => h.modulo_id === moduloFilter),
      })).filter((item: HistoriaWithEpica) => item.historias.length > 0)
    : backlog;

  const totalEstimacion = backlog
    .flatMap(b => b.historias)
    .filter(h => selectedHistoriaIds.has(h.id))
    .reduce((sum, h) => sum + h.estimacion, 0);

  const toggleHistoria = (id: string) => {
    const next = new Set(selectedHistoriaIds);
    if (next.has(id)) next.delete(id);
    else next.add(id);
    setSelectedHistoriaIds(next);
  };

  return (
    <div className="p-6 max-w-5xl mx-auto">
      <button onClick={() => navigate(-1)} className="text-blue-600 flex items-center gap-1 mb-4 hover:underline">
        <ArrowLeft size={16} /> Volver
      </button>

      <h1 className="text-2xl font-bold mb-6">Planificar Sprint</h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow border border-gray-200 p-6">
          <h2 className="text-lg font-semibold mb-4">Datos del Sprint</h2>
          <div className="space-y-3">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Nombre</label>
              <input value={nombre} onChange={e => setNombre(e.target.value)} className="w-full p-2 border rounded" placeholder="Sprint 1" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Objetivo</label>
              <textarea value={objetivo} onChange={e => setObjetivo(e.target.value)} className="w-full p-2 border rounded" rows={2} placeholder="Objetivo del sprint" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Duración (días)</label>
              <input type="number" value={duracionDias} onChange={e => setDuracionDias(Number(e.target.value))} className="w-full p-2 border rounded" min={1} max={30} />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Fecha de inicio</label>
              <input type="date" value={fechaInicio} onChange={e => setFechaInicio(e.target.value)} className="w-full p-2 border rounded" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Link de reunión (opcional)</label>
              <input value={meetingLink} onChange={e => setMeetingLink(e.target.value)} className="w-full p-2 border rounded" placeholder="https://meet.google.com/..." />
            </div>

            <div className="pt-4">
              <p className="text-sm text-gray-600 mb-1">Estimación seleccionada: <strong>{totalEstimacion} pts</strong></p>
              <p className="text-sm text-gray-600 mb-1">Historias seleccionadas: <strong>{selectedHistoriaIds.size}</strong></p>
              <button
                onClick={() => planMutation.mutate()}
                disabled={!nombre || !selectedHistoriaIds.size || planMutation.isPending}
                className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed"
              >
                {planMutation.isPending ? 'Creando...' : 'Crear Sprint'}
              </button>
              {planMutation.isError && (
                <p className="text-red-500 text-sm mt-2">Error al crear el sprint</p>
              )}
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold">Historias del Backlog</h2>
            <select value={moduloFilter} onChange={e => setModuloFilter(e.target.value)} className="border rounded px-2 py-1 text-sm">
              <option value="">Todos los módulos</option>
              {modules.map((m) => (
                <option key={m.id} value={m.id}>{m.nombre}</option>
              ))}
            </select>
          </div>
          <p className="text-sm text-gray-500 mb-3">Selecciona las historias para incluir en el sprint</p>
          <div className="space-y-4 max-h-[500px] overflow-y-auto">
            {filteredBacklog.map((item: HistoriaWithEpica) => (
              <div key={item.epica.id}>
                <h3 className="font-medium text-sm text-gray-700 mb-1">{item.epica.titulo}</h3>
                {item.historias.map(h => (
                  <label key={h.id} className={`flex items-center gap-3 p-2 rounded cursor-pointer transition ${selectedHistoriaIds.has(h.id) ? 'bg-blue-50 border border-blue-200' : 'hover:bg-gray-50'}`}>
                    <input
                      type="checkbox"
                      checked={selectedHistoriaIds.has(h.id)}
                      onChange={() => toggleHistoria(h.id)}
                      className="rounded"
                    />
                    <span className="flex-1 text-sm">{h.titulo}</span>
                    {h.modulo_id && <span className="text-xs text-gray-400">{modules.find(m => m.id === h.modulo_id)?.nombre || ''}</span>}
                    <span className="text-xs text-gray-500">{h.estimacion} pts</span>
                    <span className={`px-1.5 py-0.5 rounded text-xs ${prioridadColor(h.prioridad)}`}>{h.prioridad}</span>
                  </label>
                ))}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

function prioridadColor(p: string) {
  switch (p) {
    case 'CRITICA': return 'bg-red-100 text-red-700';
    case 'ALTA': return 'bg-orange-100 text-orange-700';
    case 'MEDIA': return 'bg-blue-100 text-blue-700';
    default: return 'bg-gray-100 text-gray-700';
  }
}
