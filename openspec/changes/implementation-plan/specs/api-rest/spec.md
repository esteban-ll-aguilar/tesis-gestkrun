# Spec: API REST

## Description
API REST completa con FastAPI, DTOs, validación Pydantic v2, paginación cursor-based, filtros, ordenamiento y documentación OpenAPI.

## Requirements

### RAR-01: Router structure
- /api/v1/auth, /api/v1/users, /api/v1/projects, /api/v1/modules
- /api/v1/epicas, /api/v1/historias, /api/v1/sprints, /api/v1/events
- /api/v1/boards, /api/v1/tasks, /api/v1/messages, /api/v1/artifacts
- /api/v1/dashboard, /api/v1/admin/users

### RAR-02: DTOs
- Request/Response schemas con Pydantic v2
- Separación entre CreateDTO, UpdateDTO, ResponseDTO
- DTOs de listado con paginación metadata

### RAR-03: Pagination
- Cursor-based para listados grandes (backlog, historial mensajes)
- Parámetros: cursor (opaque), limit (default 50, max 100)
- Response: data[], next_cursor, has_more

### RAR-04: Filters and ordering
- Parámetros de query: estado, prioridad, assigned_to, fecha_desde, fecha_hasta
- Ordenamiento: sort_by + sort_order (asc/desc)
- Filtros combinables

### RAR-05: Error handling
- Formato Problem+JSON (RFC 7807) en todas las respuestas de error
- type, title, status, detail, instance, errors (validation)
- HTTP status codes semánticos (200, 201, 204, 400, 401, 403, 404, 409, 422, 500)

### RAR-06: OpenAPI
- Auto-generada por FastAPI
- Documentación con Redoc en /docs
- Tags por recurso, summary y description en cada endpoint