import { useState } from 'react';
import { useParams } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  DndContext, closestCenter, KeyboardSensor, PointerSensor, useSensor, useSensors,
} from '@dnd-kit/core';
import type { DragEndEvent } from '@dnd-kit/core';
import { arrayMove, SortableContext, verticalListSortingStrategy, sortableKeyboardCoordinates } from '@dnd-kit/sortable';
import { backlogService } from '../features/backlog/backlogService';
import http from '../services/http';
import { Plus, GripVertical, Trash2, ChevronDown, ChevronRight, Pencil, Box, ListTodo } from 'lucide-react';
import { useAuthStore } from '../stores/auth';
import ModuleList from '../features/projects/ModuleList';

interface ModuleDTO { id: string; nombre: string }

export default function BacklogPage() {
  const { id: projectId } = useParams<{ id: string }>();
  const queryClient = useQueryClient();
  const hasRole = useAuthStore((s) => s.hasRole);
  const [expanded, setExpanded] = useState<Set<string>>(new Set());
  const [formType, setFormType] = useState<'epica' | null>(null);
  const [historiaFormEpica, setHistoriaFormEpica] = useState<string | null>(null);
  const [editEpica, setEditEpica] = useState<string | null>(null);
  const [editHistoria, setEditHistoria] = useState<string | null>(null);
  const [taskFormHistoria, setTaskFormHistoria] = useState<string | null>(null);
  const [showModules, setShowModules] = useState(false);

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

  const sensors = useSensors(
    useSensor(PointerSensor),
    useSensor(KeyboardSensor, { coordinateGetter: sortableKeyboardCoordinates })
  );

  const prioritizeMutation = useMutation({
    mutationFn: (ids: string[]) => backlogService.prioritize(projectId!, ids),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['backlog', projectId] }),
  });

  if (isLoading || !backlog) return <div className="p-6">Cargando backlog...</div>;

  const epicaIds = backlog.map(b => b.epica.id);
  const invalidate = () => queryClient.invalidateQueries({ queryKey: ['backlog', projectId] });

  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event;
    if (!over || active.id === over.id) return;
    const oldIdx = epicaIds.indexOf(active.id as string);
    const newIdx = epicaIds.indexOf(over.id as string);
    prioritizeMutation.mutate(arrayMove(epicaIds, oldIdx, newIdx));
  };

  const toggleExpand = (id: string) => {
    const next = new Set(expanded);
    if (next.has(id)) next.delete(id); else next.add(id);
    setExpanded(next);
  };

  const moduloName = (moduloId: string | null) => {
    if (!moduloId) return '';
    return modules.find(m => m.id === moduloId)?.nombre || '';
  };

  return (
    <div className="p-6 max-w-5xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Product Backlog</h1>
        <div className="flex items-center gap-2">
          {hasRole('PRODUCT_OWNER') && (
            <button onClick={() => setShowModules(!showModules)} className="border border-gray-300 text-gray-700 px-4 py-2 rounded-lg flex items-center gap-2 hover:bg-gray-100">
              <Box size={18} /> Módulos
            </button>
          )}
          {hasRole('PRODUCT_OWNER') && (
            <button onClick={() => setFormType('epica')} className="bg-blue-600 text-white px-4 py-2 rounded-lg flex items-center gap-2 hover:bg-blue-700">
              <Plus size={18} /> Nueva Épica
            </button>
          )}
        </div>
      </div>

      {showModules && (
        <div className="mb-6 p-4 border rounded-lg bg-gray-50">
          <ModuleList projectId={projectId!} />
        </div>
      )}

      {formType === 'epica' && (
        <EpicaForm projectId={projectId!} modules={modules} onClose={() => setFormType(null)} onSuccess={() => { setFormType(null); invalidate(); }} />
      )}

      <DndContext sensors={sensors} collisionDetection={closestCenter} onDragEnd={handleDragEnd}>
        <SortableContext items={epicaIds} strategy={verticalListSortingStrategy}>
          <div className="space-y-3">
            {backlog.map(item => (
              <div key={item.epica.id} className="bg-white rounded-lg shadow border border-gray-200 p-4">
                <div className="flex items-center gap-3">
                  <GripVertical className="text-gray-400 cursor-grab shrink-0" size={20} />
                  <button onClick={() => toggleExpand(item.epica.id)} className="text-gray-500 shrink-0">
                    {expanded.has(item.epica.id) ? <ChevronDown size={18} /> : <ChevronRight size={18} />}
                  </button>
                  <div className="flex-1 min-w-0">
                    {editEpica === item.epica.id ? (
                      <EditEpicaForm projectId={projectId!} epica={item.epica} modules={modules} onClose={() => setEditEpica(null)} onSuccess={() => { setEditEpica(null); invalidate(); }} />
                    ) : (
                      <>
                        <h3 className="font-semibold">{item.epica.titulo}</h3>
                        {item.epica.descripcion && <p className="text-gray-500 text-sm truncate">{item.epica.descripcion}</p>}
                        {item.epica.modulo_id && <span className="text-xs text-gray-400">{moduloName(item.epica.modulo_id)}</span>}
                      </>
                    )}
                  </div>
                  <span className={`px-2 py-1 rounded text-xs font-medium ${prioridadColor(item.epica.prioridad)}`}>{item.epica.prioridad}</span>
                  <span className="text-sm text-gray-500 shrink-0">{item.historias.reduce((s, h) => s + h.estimacion, 0)} pts</span>
                  {hasRole('PRODUCT_OWNER') && !editEpica && (
                    <button onClick={() => setEditEpica(item.epica.id)} className="text-blue-500 hover:text-blue-700 shrink-0"><Pencil size={14} /></button>
                  )}
                  {hasRole('PRODUCT_OWNER') && (
                    <button onClick={() => backlogService.deleteEpica(projectId!, item.epica.id).then(invalidate)} className="text-red-500 hover:text-red-700 shrink-0"><Trash2 size={16} /></button>
                  )}
                </div>

                {expanded.has(item.epica.id) && (
                  <div className="ml-10 mt-3 space-y-2">
                    {item.historias.map(h => (
                      <div key={h.id} className="space-y-1">
                        <div className="flex items-center gap-2 p-2 bg-gray-50 rounded">
                          {editHistoria === h.id ? (
                            <EditHistoriaForm projectId={projectId!} historia={h} onClose={() => setEditHistoria(null)} onSuccess={() => { setEditHistoria(null); invalidate(); }} />
                          ) : (
                            <>
                              <span className="flex-1 text-sm">{h.titulo}</span>
                              {h.sprint_nombre && <span className="text-xs bg-purple-100 text-purple-700 px-1.5 py-0.5 rounded">{h.sprint_nombre}</span>}
                              <span className="text-xs text-gray-500">{h.estimacion} pts</span>
                              <span className={`px-1.5 py-0.5 rounded text-xs ${prioridadColor(h.prioridad)}`}>{h.prioridad}</span>
                              <button onClick={() => setTaskFormHistoria(taskFormHistoria === h.id ? null : h.id)} className="text-green-500 hover:text-green-700" title="Crear tarea"><ListTodo size={14} /></button>
                              {hasRole('PRODUCT_OWNER') && !editHistoria && (
                                <button onClick={() => setEditHistoria(h.id)} className="text-blue-400 hover:text-blue-600"><Pencil size={12} /></button>
                              )}
                              {hasRole('PRODUCT_OWNER') && (
                                <button onClick={() => backlogService.deleteHistoria(projectId!, h.id).then(invalidate)} className="text-red-400 hover:text-red-600"><Trash2 size={14} /></button>
                              )}
                            </>
                          )}
                        </div>
                        {taskFormHistoria === h.id && (
                          <TaskForm historiaId={h.id} onClose={() => setTaskFormHistoria(null)} onSuccess={() => { setTaskFormHistoria(null); invalidate(); }} />
                        )}
                      </div>
                    ))}
                    {historiaFormEpica === item.epica.id ? (
                      <HistoriaForm projectId={projectId!} epicaId={item.epica.id} onClose={() => setHistoriaFormEpica(null)} onSuccess={() => { setHistoriaFormEpica(null); invalidate(); }} />
                    ) : hasRole('PRODUCT_OWNER') ? (
                      <button onClick={() => setHistoriaFormEpica(item.epica.id)} className="text-blue-600 text-sm flex items-center gap-1 hover:text-blue-800">
                        <Plus size={14} /> Añadir historia
                      </button>
                    ) : null}
                  </div>
                )}
              </div>
            ))}
          </div>
        </SortableContext>
      </DndContext>
    </div>
  );
}

function EpicaForm({ projectId, modules, onClose, onSuccess }: { projectId: string; modules: ModuleDTO[]; onClose: () => void; onSuccess: () => void }) {
  const [titulo, setTitulo] = useState('');
  const [descripcion, setDescripcion] = useState('');
  const [prioridad, setPrioridad] = useState('MEDIA');
  const [moduloId, setModuloId] = useState('');
  const mutation = useMutation({
    mutationFn: () => backlogService.createEpica(projectId, { titulo, descripcion, prioridad, modulo_id: moduloId || null }),
    onSuccess,
  });
  return (
    <div className="bg-gray-50 p-4 rounded-lg mb-4 border">
      <input value={titulo} onChange={e => setTitulo(e.target.value)} placeholder="Título de la épica" className="w-full p-2 border rounded mb-2" />
      <textarea value={descripcion} onChange={e => setDescripcion(e.target.value)} placeholder="Descripción" className="w-full p-2 border rounded mb-2" rows={2} />
      <div className="flex gap-2 mb-2">
        <select value={prioridad} onChange={e => setPrioridad(e.target.value)} className="p-2 border rounded flex-1">
          <option value="BAJA">Baja</option><option value="MEDIA">Media</option><option value="ALTA">Alta</option><option value="CRITICA">Crítica</option>
        </select>
        <select value={moduloId} onChange={e => setModuloId(e.target.value)} className="p-2 border rounded flex-1">
          <option value="">Sin módulo</option>
          {modules.map(m => <option key={m.id} value={m.id}>{m.nombre}</option>)}
        </select>
      </div>
      <div className="flex gap-2">
        <button onClick={() => mutation.mutate()} disabled={!titulo || mutation.isPending} className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">Guardar</button>
        <button onClick={onClose} className="px-4 py-2 rounded border hover:bg-gray-100">Cancelar</button>
      </div>
    </div>
  );
}

function EditEpicaForm({ projectId, epica, modules, onClose, onSuccess }: { projectId: string; epica: any; modules: ModuleDTO[]; onClose: () => void; onSuccess: () => void }) {
  const [titulo, setTitulo] = useState(epica.titulo);
  const [descripcion, setDescripcion] = useState(epica.descripcion || '');
  const [prioridad, setPrioridad] = useState(epica.prioridad);
  const [moduloId, setModuloId] = useState(epica.modulo_id || '');
  const mutation = useMutation({
    mutationFn: () => backlogService.updateEpica(projectId, epica.id, { titulo, descripcion, prioridad, modulo_id: moduloId || null }),
    onSuccess,
  });
  return (
    <div className="space-y-2">
      <input value={titulo} onChange={e => setTitulo(e.target.value)} className="w-full p-1.5 border rounded text-sm" />
      <textarea value={descripcion} onChange={e => setDescripcion(e.target.value)} className="w-full p-1.5 border rounded text-sm" rows={2} />
      <div className="flex gap-2">
        <select value={prioridad} onChange={e => setPrioridad(e.target.value)} className="p-1.5 border rounded text-sm flex-1">
          <option value="BAJA">Baja</option><option value="MEDIA">Media</option><option value="ALTA">Alta</option><option value="CRITICA">Crítica</option>
        </select>
        <select value={moduloId} onChange={e => setModuloId(e.target.value)} className="p-1.5 border rounded text-sm flex-1">
          <option value="">Sin módulo</option>
          {modules.map(m => <option key={m.id} value={m.id}>{m.nombre}</option>)}
        </select>
      </div>
      <div className="flex gap-2">
        <button onClick={() => mutation.mutate()} disabled={!titulo} className="text-xs text-blue-600 hover:underline">Guardar</button>
        <button onClick={onClose} className="text-xs text-gray-500 hover:underline">Cancelar</button>
      </div>
    </div>
  );
}

function HistoriaForm({ projectId, epicaId, onClose, onSuccess }: { projectId: string; epicaId: string; onClose: () => void; onSuccess: () => void }) {
  const [titulo, setTitulo] = useState('');
  const [descripcion, setDescripcion] = useState('');
  const [estimacion, setEstimacion] = useState(1);
  const mutation = useMutation({
    mutationFn: () => backlogService.createHistoria(projectId, { epica_id: epicaId, titulo, descripcion, estimacion }),
    onSuccess,
  });
  return (
    <div className="bg-gray-50 p-3 rounded border">
      <input value={titulo} onChange={e => setTitulo(e.target.value)} placeholder="Título" className="w-full p-2 border rounded mb-2" />
      <textarea value={descripcion} onChange={e => setDescripcion(e.target.value)} placeholder="Descripción" className="w-full p-2 border rounded mb-2" rows={2} />
      <div className="flex gap-2 mb-2">
        <select value={estimacion} onChange={e => setEstimacion(Number(e.target.value))} className="p-2 border rounded flex-1">
          {[1, 2, 3, 5, 8, 13, 21].map(v => <option key={v} value={v}>{v} pts</option>)}
        </select>
      </div>
      <div className="flex gap-2">
        <button onClick={() => mutation.mutate()} disabled={!titulo || mutation.isPending} className="bg-blue-600 text-white px-3 py-1.5 rounded text-sm hover:bg-blue-700">Guardar</button>
        <button onClick={onClose} className="px-3 py-1.5 rounded border text-sm hover:bg-gray-100">Cancelar</button>
      </div>
    </div>
  );
}

function EditHistoriaForm({ projectId, historia, onClose, onSuccess }: { projectId: string; historia: any; onClose: () => void; onSuccess: () => void }) {
  const [titulo, setTitulo] = useState(historia.titulo);
  const [estimacion, setEstimacion] = useState(historia.estimacion);
  const mutation = useMutation({
    mutationFn: () => backlogService.updateHistoria(projectId, historia.id, { titulo, estimacion }),
    onSuccess,
  });
  return (
    <div className="flex-1 flex items-center gap-2">
      <input value={titulo} onChange={e => setTitulo(e.target.value)} className="p-1 border rounded text-sm flex-1" />
      <select value={estimacion} onChange={e => setEstimacion(Number(e.target.value))} className="p-1 border rounded text-sm">
        {[1, 2, 3, 5, 8, 13, 21].map(v => <option key={v} value={v}>{v} pts</option>)}
      </select>
      <button onClick={() => mutation.mutate()} disabled={!titulo} className="text-xs text-blue-600 hover:underline">Guardar</button>
      <button onClick={onClose} className="text-xs text-gray-500 hover:underline">Cancelar</button>
    </div>
  );
}

function TaskForm({ historiaId, onClose, onSuccess }: { historiaId: string; onClose: () => void; onSuccess: () => void }) {
  const [titulo, setTitulo] = useState('');
  const [descripcion, setDescripcion] = useState('');
  const mutation = useMutation({
    mutationFn: () => backlogService.createTask(historiaId, { titulo, descripcion }),
    onSuccess,
  });
  return (
    <div className="bg-green-50 p-3 rounded border border-green-200 ml-4">
      <input value={titulo} onChange={e => setTitulo(e.target.value)} placeholder="Título de la tarea" className="w-full p-2 border rounded mb-2 text-sm" />
      <textarea value={descripcion} onChange={e => setDescripcion(e.target.value)} placeholder="Descripción (opcional)" className="w-full p-2 border rounded mb-2 text-sm" rows={2} />
      <div className="flex gap-2">
        <button onClick={() => mutation.mutate()} disabled={!titulo || mutation.isPending} className="bg-green-600 text-white px-3 py-1 rounded text-sm hover:bg-green-700">Crear tarea</button>
        <button onClick={onClose} className="px-3 py-1 rounded border text-sm hover:bg-gray-100">Cancelar</button>
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
