export type TipoArtefacto = string

export interface Artifact {
  id: string
  task_id: string
  nombre: string
  tipo: TipoArtefacto
  version_actual: number
}

export interface ArtifactVersion {
  id: string
  artifact_id: string
  version: number
  content_url: string
  uploaded_by: string
  created_at: string
}
