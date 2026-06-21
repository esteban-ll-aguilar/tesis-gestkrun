import { useParams, Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { backlogService } from '../features/backlog/backlogService';
import type { SprintDTO } from '../features/backlog/backlogService';
import { Plus } from 'lucide-react';
import { useAuthStore } from '../stores/auth';

export default function SprintListPage() {
  const { id: projectId } = useParams<{ id: string }>();
  const hasRole = useAuthStore((s) => s.hasRole);
  const { data: sprints, isLoading } = useQuery({
    queryKey: ['sprints', projectId],
    queryFn: () => backlogService.listSprints(projectId!),
    enabled: !!projectId,
  });

  if (isLoading) return <div className="p-6">Cargando sprints...</div>;

  return (
    <div className="p-6 max-w-5xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Sprints</h1>
        {hasRole('SCRUM_MASTER') && (
          <Link to={`/projects/${projectId}/sprints/plan`} className="bg-blue-600 text-white px-4 py-2 rounded-lg flex items-center gap-2 hover:bg-blue-700">
            <Plus size={18} /> Planificar Sprint
          </Link>
        )}
      </div>

      <div className="space-y-3">
        {sprints?.map(sprint => (
          <SprintCard key={sprint.id} sprint={sprint} projectId={projectId!} />
        ))}
        {!sprints?.length && (
          <p className="text-gray-500 text-center py-8">No hay sprints planificados aún.</p>
        )}
      </div>
    </div>
  );
}

function SprintCard({ sprint, projectId }: { sprint: SprintDTO; projectId: string }) {
  const estadoColors: Record<string, string> = {
    PLANIFICADO: 'bg-gray-100 text-gray-700',
    EN_EJECUCION: 'bg-green-100 text-green-700',
    FINALIZADO: 'bg-blue-100 text-blue-700',
    CANCELADO: 'bg-red-100 text-red-700',
  };

  return (
    <Link to={`/projects/${projectId}/sprints/${sprint.id}`} className="block bg-white rounded-lg shadow border border-gray-200 p-4 hover:shadow-md transition">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="font-semibold text-lg">{sprint.nombre}</h3>
          <p className="text-gray-500 text-sm">{sprint.objetivo}</p>
        </div>
        <div className="flex items-center gap-3">
          <span className={`px-2 py-1 rounded text-xs font-medium ${estadoColors[sprint.estado] || 'bg-gray-100'}`}>
            {sprint.estado}
          </span>
          <span className="text-sm text-gray-500">
            {sprint.fecha_inicio} → {sprint.fecha_fin}
          </span>
        </div>
      </div>
    </Link>
  );
}
