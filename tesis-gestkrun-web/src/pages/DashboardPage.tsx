import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer,
  LineChart, Line, AreaChart, Area, PieChart, Pie, Cell, Legend,
} from 'recharts';
import type { PieLabelRenderProps } from 'recharts';
import { projectService } from '../features/projects/projectService';
import { dashboardService } from '../features/dashboard/dashboardService';
import { CheckCircle, Clock, AlertTriangle, ListChecks } from 'lucide-react';

const COLORS = ['#3B82F6', '#F59E0B', '#EF4444', '#10B981', '#6B7280', '#8B5CF6'];

export default function DashboardPage() {
  const [selectedProjectId, setSelectedProjectId] = useState<string | null>(null);

  const { data: projects } = useQuery({
    queryKey: ['projects'],
    queryFn: projectService.listProjects,
  });

  const { data: metrics } = useQuery({
    queryKey: ['dashboard-metrics', selectedProjectId],
    queryFn: () => dashboardService.getMetrics(selectedProjectId!),
    enabled: !!selectedProjectId,
  });

  const { data: velocity } = useQuery({
    queryKey: ['dashboard-velocity', selectedProjectId],
    queryFn: () => dashboardService.getVelocity(selectedProjectId!),
    enabled: !!selectedProjectId,
  });

  const { data: distribution } = useQuery({
    queryKey: ['dashboard-distribution', selectedProjectId],
    queryFn: () => dashboardService.getTaskDistribution(selectedProjectId!),
    enabled: !!selectedProjectId,
  });

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold">Dashboard</h1>
        <select
          value={selectedProjectId || ''}
          onChange={e => setSelectedProjectId(e.target.value || null)}
          className="p-2 border rounded-lg"
        >
          <option value="">Seleccionar proyecto</option>
          {projects?.map(p => (
            <option key={p.id} value={p.id}>{p.nombre}</option>
          ))}
        </select>
      </div>

      {!selectedProjectId && (
        <div className="text-center py-20 text-gray-500">
          <ListChecks size={48} className="mx-auto mb-4 text-gray-300" />
          <p className="text-lg">Selecciona un proyecto para ver sus métricas</p>
        </div>
      )}

      {selectedProjectId && (
        <>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
            <MetricCard
              icon={<ListChecks size={24} />}
              label="Total Tareas"
              value={metrics?.total_tasks ?? 0}
              color="blue"
            />
            <MetricCard
              icon={<Clock size={24} />}
              label="En Progreso"
              value={metrics?.in_progress ?? 0}
              color="yellow"
            />
            <MetricCard
              icon={<AlertTriangle size={24} />}
              label="Bloqueadas"
              value={metrics?.blocked ?? 0}
              color="red"
            />
            <MetricCard
              icon={<CheckCircle size={24} />}
              label="Completadas"
              value={metrics?.completed ?? 0}
              color="green"
            />
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
            <div className="bg-white rounded-lg shadow border border-gray-200 p-6">
              <h2 className="text-lg font-semibold mb-4">Velocity (por Sprint)</h2>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={velocity || []}>
                  <XAxis dataKey="sprint_nombre" tick={{ fontSize: 12 }} />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="velocity" fill="#3B82F6" radius={[4, 4, 0, 0]} name="Tareas Completadas" />
                </BarChart>
              </ResponsiveContainer>
            </div>

            <div className="bg-white rounded-lg shadow border border-gray-200 p-6">
              <h2 className="text-lg font-semibold mb-4">Distribución de Tareas</h2>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={distribution || []}
                    dataKey="count"
                    nameKey="estado"
                    cx="50%"
                    cy="50%"
                    outerRadius={100}
                    label={({ name, percent }: PieLabelRenderProps) => `${name ?? ''} ${((percent ?? 0) * 100).toFixed(0)}%`}
                  >
                    {(distribution || []).map((_, i) => (
                      <Cell key={i} fill={COLORS[i % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            </div>

            <div className="bg-white rounded-lg shadow border border-gray-200 p-6">
              <h2 className="text-lg font-semibold mb-4">Tendencia de Velocidad</h2>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={velocity || []}>
                  <XAxis dataKey="sprint_nombre" tick={{ fontSize: 12 }} />
                  <YAxis />
                  <Tooltip />
                  <Line type="monotone" dataKey="velocity" stroke="#10B981" strokeWidth={2} dot={{ fill: '#10B981' }} name="Velocity" />
                </LineChart>
              </ResponsiveContainer>
            </div>

            <div className="bg-white rounded-lg shadow border border-gray-200 p-6">
              <h2 className="text-lg font-semibold mb-4">Rendimiento General</h2>
              <ResponsiveContainer width="100%" height={300}>
                <AreaChart data={[
                  { name: 'Pendiente', value: ((metrics?.total_tasks ?? 0) - (metrics?.in_progress ?? 0) - (metrics?.completed ?? 0) - (metrics?.blocked ?? 0)) || 0 },
                  { name: 'En Progreso', value: metrics?.in_progress ?? 0 },
                  { name: 'Bloqueado', value: metrics?.blocked ?? 0 },
                  { name: 'Completado', value: metrics?.completed ?? 0 },
                ]}>
                  <XAxis dataKey="name" tick={{ fontSize: 12 }} />
                  <YAxis />
                  <Tooltip />
                  <Area type="monotone" dataKey="value" stroke="#8B5CF6" fill="#8B5CF6" fillOpacity={0.2} name="Tareas" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>

          {metrics && metrics.blocked > 0 && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-center gap-3 mb-4">
              <AlertTriangle size={20} className="text-red-500" />
              <p className="text-red-700 font-medium">
                Hay <strong>{metrics.blocked}</strong> tareas bloqueadas que requieren atención.
              </p>
            </div>
          )}
        </>
      )}
    </div>
  );
}

function MetricCard({ icon, label, value, color }: {
  icon: React.ReactNode; label: string; value: number; color: 'blue' | 'yellow' | 'red' | 'green';
}) {
  const colors = {
    blue: 'bg-blue-50 text-blue-600 border-blue-200',
    yellow: 'bg-yellow-50 text-yellow-600 border-yellow-200',
    red: 'bg-red-50 text-red-600 border-red-200',
    green: 'bg-green-50 text-green-600 border-green-200',
  };

  return (
    <div className={`rounded-lg border p-4 ${colors[color]}`}>
      <div className="flex items-center gap-3">
        {icon}
        <div>
          <p className="text-sm opacity-75">{label}</p>
          <p className="text-2xl font-bold">{value}</p>
        </div>
      </div>
    </div>
  );
}
