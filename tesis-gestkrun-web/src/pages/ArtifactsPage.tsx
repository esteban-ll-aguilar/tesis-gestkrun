import { useState } from 'react';
import { useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { artifactService, ArtifactDTO } from '../features/artifacts/artifactService';
import { Upload, FileText, Download, ChevronDown, ChevronRight } from 'lucide-react';

export default function ArtifactsPage() {
  const { taskId } = useParams<{ id: string; taskId: string }>();
  const [uploading, setUploading] = useState(false);

  const queryFn = () => artifactService.listByTask(taskId!);
  const { data: artifacts, isLoading, refetch } = useQuery({
    queryKey: ['artifacts', taskId],
    queryFn,
    enabled: !!taskId,
  });

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file || !taskId) return;
    setUploading(true);
    try {
      await artifactService.upload(taskId, file.name, 'DOCUMENTO', file);
      refetch();
      e.target.value = '';
    } finally {
      setUploading(false);
    }
  };

  if (!taskId) return <div className="p-6">Selecciona una tarea para ver sus artefactos</div>;

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Artefactos</h1>
        <label className="bg-blue-600 text-white px-4 py-2 rounded-lg flex items-center gap-2 hover:bg-blue-700 cursor-pointer">
          <Upload size={18} />
          {uploading ? 'Subiendo...' : 'Subir archivo'}
          <input type="file" className="hidden" onChange={handleUpload} disabled={uploading} />
        </label>
      </div>

      {isLoading && <p className="text-gray-500">Cargando artefactos...</p>}

      <div className="space-y-3">
        {artifacts?.map(a => (
          <ArtifactCard key={a.id} artifact={a} />
        ))}
        {!isLoading && (!artifacts || artifacts.length === 0) && (
          <p className="text-gray-500 text-center py-8">No hay artefactos subidos.</p>
        )}
      </div>
    </div>
  );
}

function ArtifactCard({ artifact }: { artifact: ArtifactDTO }) {
  const [expanded, setExpanded] = useState(false);
  const { data: versions } = useQuery({
    queryKey: ['artifact-versions', artifact.id],
    queryFn: () => artifactService.listVersions(artifact.id),
    enabled: expanded,
  });

  return (
    <div className="bg-white rounded-lg shadow border border-gray-200 p-4">
      <button onClick={() => setExpanded(!expanded)} className="flex items-center gap-3 w-full text-left">
        {expanded ? <ChevronDown size={18} className="text-gray-400" /> : <ChevronRight size={18} className="text-gray-400" />}
        <FileText size={20} className="text-blue-500" />
        <span className="flex-1 font-medium">{artifact.nombre}</span>
        <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded">{artifact.tipo}</span>
        <span className="text-xs text-gray-500">v{artifact.version_actual}</span>
      </button>

      {expanded && versions && (
        <div className="ml-9 mt-3 space-y-2">
          {versions.map(v => (
            <div key={v.id} className="flex items-center gap-3 p-2 bg-gray-50 rounded text-sm">
              <span className="text-gray-500">v{v.version}</span>
              <span className="text-xs text-gray-400">{new Date(v.created_at).toLocaleDateString()}</span>
              <span className="text-xs text-gray-400">por {v.uploaded_by.slice(0, 8)}...</span>
              <a href={v.content_url} download className="ml-auto text-blue-600 hover:text-blue-800">
                <Download size={16} />
              </a>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
