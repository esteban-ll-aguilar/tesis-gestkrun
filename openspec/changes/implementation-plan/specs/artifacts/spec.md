# Spec: Artifact Management

## Description
Gestión de artefactos documentales con versionado, categorización por tipo, y descarga de versiones.

## Requirements

### RAR-01: Upload
- POST /tasks/{id}/artifacts — subir artefacto
- Tipos: Requisito, Diagrama, Acta, Documento, Código
- Almacenamiento: filesystem local (interface para S3 futuro)

### RAR-02: Versioning
- Nuevo upload = nueva versión automática
- Versionado incremental (1, 2, 3...)
- GET /artifacts/{id}/versions — listar versiones
- POST /artifacts/{id}/versions — subir nueva versión

### RAR-03: Download
- GET /artifacts/{id}/versions/{version}/download
- GET /artifacts/{id}/download — última versión

### RAR-04: Frontend
- Upload zone con drag & drop
- Lista de artefactos con tipo, versión, fecha
- Preview de versiones anteriores
- Download button