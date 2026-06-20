## Context

GESTKRUN es una plataforma web para gestión de proyectos de desarrollo de software bajo Scrumban. La documentación completa del proyecto ha sido auditada y normalizada. Existe una especificación de producto (`product.md`), una arquitectura definida (`docs/architecture.md`), invariants y SLOs (`config.yaml`), 7 ADRs, C4Model, y diagramas UML completos.

Actualmente el código base es mínimo: `tesis-gestkrun-api/` y `tesis-gestkrun-web/` existen con estructuras de carpetas vacías. No hay implementación funcional.

Este plan detalla cómo implementar el 100% de los requerimientos en 10 fases secuenciales, respetando Clean Architecture + DDD, sin SaaS, sin microservicios, sin event sourcing.

---

## Goals / Non-Goals

**Goals:**
1. Implementar backend completo con FastAPI + Clean Architecture + DDD
2. Implementar frontend completo con React + TypeScript
3. Base de datos PostgreSQL con migraciones, índices y particionamiento
4. Autenticación JWT + RBAC
5. Tablero Kanban con drag & drop y validación WIP
6. Gestión de backlog, sprints, épicas e historias de usuario
7. Mensajería asíncrona y gestión de artefactos
8. Dashboard con métricas (lead time, cycle time, velocidad)
9. Tests: unitarios (85%+), integración, E2E
10. CI/CD + Docker Compose

**Non-Goals:**
- Sin multitenancy, billing, subscriptions
- Sin microservicios, Kubernetes, event sourcing
- Sin tecnologías no justificadas en la documentación

---

## Auditoría de consistencia (pre-implementación)

Antes de comenzar la implementación, se verificó la consistencia de toda la documentación:

| Documento vs Documento | Resultado |
|------------------------|-----------|
| product.md ↔ docs/architecture.md | ✓ Consistente |
| docs/architecture.md ↔ docs/uml/ | ✓ Consistente |
| docs/c4/ ↔ docs/architecture.md | ✓ Consistente |
| docs/adr/ ↔ docs/architecture.md | ✓ Consistente |
| product.md ↔ config.yaml | ✓ Consistente |
| docs/uml/ ↔ docs/adr/ | ✓ Consistente |

**Correcciones aplicadas pre-implementación:**
- `task_state_transitions` renombrado conceptualmente a "historial de estado / audit log" (no event sourcing)
- README.md pendiente de completar (se hará en Fase 10)

---

## Decisions

### D1: Estructura del backend (Clean Architecture)
```
tesis-gestkrun-api/
├── app/
│   ├── api/v1/           # FastAPI routers por recurso
│   ├── core/             # Config, settings, logging, exceptions
│   ├── domain/           # Entities, VOs, enums, repos interfaces, events, services
│   ├── application/      # Use cases, DTOs, mappers, ports
│   ├── infrastructure/   # Persistence (SQLAlchemy), auth, cache, messaging, storage
│   └── workers/          # Celery tasks
├── tests/                # Unit, integration
├── alembic/              # Migrations
└── main.py
```

### D2: Estructura del frontend
```
tesis-gestkrun-web/
├── src/
│   ├── app/              # Router, providers, layouts
│   ├── pages/            # Page components by route
│   ├── features/         # Feature modules (auth, projects, kanban, backlog, etc.)
│   ├── components/       # Shared UI components (shadcn/ui)
│   ├── hooks/            # Custom hooks
│   ├── services/         # HTTP client, API functions
│   ├── stores/           # Zustand stores
│   ├── types/            # TypeScript types, DTOs
│   └── utils/            # Helpers, formatters
└── public/
```

### D3: Base de datos — esquema principal
Tablas: users, roles, projects, modules, epicas, historia_usuario, sprints, sprint_eventos, tasks, task_state_transitions, messages, artifacts, artifact_versions.

### D4: Autenticación
JWT access token (15 min) + refresh token (7 días, httpOnly cookie). Argon2id para hashing. RBAC con permisos granulares.

### D5: WIP Validation
Domain service `WIPValidationService` con conteo por usuario. Frontend: optimistic update + rollback. Backend: validación síncrona (< 50ms).

### D6: CQRS ligero
Materialized views para dashboards, refresco cada 5 min vía Celery. Modelos de lectura separados (SQLAlchemy Core).

---

## Roadmap de implementación

### Fase 1: Infraestructura base (backend + frontend)
**Objetivo:** Setup del proyecto, dependencias, configuración, Docker Compose
**Dependencias:** Ninguna
**Entregables:**
- Docker Compose con PostgreSQL 16, Redis, PgBouncer, Nginx
- Backend: FastAPI app con health endpoints, settings, logging, exception handlers
- Frontend: Vite + React + TS + Tailwind + shadcn/ui + Router
- Makefile con comandos comunes
- CI/CD base: lint → test → build
**Criterios de aceptación:**
- `make up` levanta todos los servicios
- `GET /health` responde 200
- Frontend compila sin errores
- Lint pasa sin warnings

### Fase 2: Modelo de dominio
**Objetivo:** Implementar entidades, VOs, enums, eventos de dominio e interfaces de repositorio
**Dependencias:** Fase 1
**Entregables:**
- Entidades: User, Project, Module, Epica, HistoriaUsuario, Sprint, SprintEvento, Task, TaskStateTransition, Message, Artifact, ArtifactVersion
- Value Objects: Email, PasswordHash, EstimacionEsfuerzo, UserId, ProjectId, TaskId, SprintId, EpicaId, WIPCount
- Enums: Rol, EstadoTarea, EstadoSprint, EstadoProyecto, EstadoModulo, Prioridad, TipoArtefacto, TipoMensaje, TipoEventoScrum
- Domain Events: UserRegistered, TaskMoved, WIPViolated, SprintClosed, etc. (13 eventos)
- Repository interfaces: IUserRepository, IProjectRepository, etc.
- Domain Services: WIPValidationService, KanbanFlowService, MetricsCalculationService
- Tests unitarios del dominio (sin dependencias externas)
**Criterios de aceptación:**
- Cobertura de tests del dominio ≥ 90%
- Todos los invariants del dominio implementados y testeados
- Las entidades no dependen de infraestructura

### Fase 3: Persistencia
**Objetivo:** Migraciones Alembic, repositorios SQLAlchemy, índices, particionamiento
**Dependencias:** Fase 2
**Entregables:**
- Migración inicial con todas las tablas
- Índices: compuestos (cardinalidad descendente), parciales (soft-delete), GIN (JSONB), BRIN (temporales)
- Particionamiento mensual en task_state_transitions, audit_log
- Materialized views para dashboards
- Soft-delete en todas las entidades
- Audit trail (created_at, updated_at, created_by, updated_by)
- Implementaciones SQLAlchemy de todos los repositorios
- Tests de integración con base de datos real (TestContainers)
**Criterios de aceptación:**
- `alembic upgrade head` aplica todas las migraciones
- Tests de integración pasan con PostgreSQL en contenedor
- Índices documentados en la migración

### Fase 4: Autenticación y autorización
**Objetivo:** Registro, login, JWT, RBAC, rate limiting
**Dependencias:** Fase 2, Fase 3
**Entregables:**
- Endpoints: POST /auth/register, POST /auth/login, POST /auth/logout, POST /auth/refresh, POST /auth/recover-password
- JWTProvider: access token (15 min), refresh token (7 días, httpOnly)
- PasswordHasher: Argon2id
- Dependencias FastAPI: get_current_user, require_role, require_permission
- Rate limiting: 100 req/min general, 20 req/min auth
- Flujo de registro con validación de email
- Frontend: login page, register page, recovery page, auth guard, refresh interceptor
- Tests de integración de auth
**Criterios de aceptación:**
- Login/register/logout funcionan end-to-end
- Token refresh automático sin perder sesión
- Endpoints protegidos rechazan requests sin token
- Rate limiting bloquea después de N requests

### Fase 5: API REST — Proyectos, Módulos, Equipos
**Objetivo:** CRUD de proyectos, módulos, asignación de equipo
**Dependencias:** Fase 4
**Entregables:**
- Backend: routers + use cases para projects, modules, team assignments
- Frontend: project list, project detail, project form, module management, team management
- Validaciones: solo PO crea proyectos, solo PO asigna equipo
- Paginación cursor-based en listados de proyectos
**Criterios de aceptación:**
- PO puede crear/editar proyectos
- PO puede asignar SM y Developers
- Admin NO puede crear proyectos (invariante)
- Frontend responsivo

### Fase 6: Backlog y Sprints
**Objetivo:** Épicas, historias de usuario, priorización, sprints, eventos ágiles
**Dependencias:** Fase 5
**Entregables:**
- Backend: CRUD épicas, CRUD historias, priorización drag & drop, sprint planning, sprint lifecycle
- Frontend: backlog view con drag & drop, sprint planning wizard, sprint list, sprint detail
- Validaciones: backlog debe estar priorizado para sprint planning, solo SM cierra sprints
- Transiciones de sprint: PLANIFICADO → EN_EJECUCION → FINALIZADO
- Sprint eventos: Daily, Review, Retro forms
**Criterios de aceptación:**
- PO puede crear/priorizar backlog
- SM puede planificar sprint desde backlog priorizado
- Sistema bloquea si backlog no está priorizado
- Eventos ágiles se registran dentro del sprint activo

### Fase 7: Tablero Kanban
**Objetivo:** Kanban board con drag & drop, WIP validation, transiciones, bloqueos
**Dependencias:** Fase 6
**Entregables:**
- Backend: PATCH /tasks/{id}/transition, GET /boards/{sprintId}
- WIPValidationService con conteo por usuario (máx 3 EN_PROCESO)
- TaskStateTransition audit log automático
- Frontend: Kanban board con @dnd-kit, optimistic update + rollback
- Columnas: Pendiente, En Proceso, Bloqueado, En Revisión, Terminado, Cancelado
- Alerta visual WIP (2/3 yellow, 3/3 block)
- Filtro de tareas bloqueadas (Scrum Master)
- Gestión de impedimentos: causa, responsable de desbloqueo
**Criterios de aceptación:**
- Drag & drop funciona con feedback visual inmediato
- WIP validation: bloquea en frontend y backend
- Rollback visual si backend rechaza
- Audit log registra cada transición
- Tests E2E con Playwright del flujo Kanban

### Fase 8: Mensajería y Artefactos
**Objetivo:** Chat asíncrono por proyecto/tarea, gestión de artefactos con versionado
**Dependencias:** Fase 7
**Entregables:**
- Backend: endpoints de mensajes (proyecto y tarea), WebSocket para tiempo real
- Frontend: chat panel, historial con paginación cursor-based
- Backend: endpoints de artefactos, versionado automático
- Frontend: upload, preview, version history, download
- Categorías: Requisito, Diagrama, Acta, Documento, Código
**Criterios de aceptación:**
- Mensajes en tiempo real vía WebSocket
- Historial con paginación
- Upload de artefactos con versionado
- Visualización de versiones previas

### Fase 9: Dashboard y Métricas
**Objetivo:** Dashboard con velocidad, lead time, cycle time, throughput, materialized views
**Dependencias:** Fase 8
**Entregables:**
- Materialized views para métricas agregadas
- Celery tasks: refresh cada 5 min
- Backend: endpoints GET /dashboard/{projectId}/metrics
- Frontend: dashboard con Recharts/Tremor (gráficos de velocidad, lead time, cycle time)
- Alerta de tareas bloqueadas activas
- Conteo de tareas por estado del Kanban
**Criterios de aceptación:**
- Dashboard carga en < 2s (desde MV)
- Métricas reflejan datos actuales (máx 5 min de desfase)
- Gráficos responsivos

### Fase 10: Calidad, CI/CD y documentación
**Objetivo:** Tests completos, CI/CD pipeline, Docker multi-stage, README
**Dependencias:** Fases 1-9
**Entregables:**
- Backend tests: unitarios (dominio ≥ 90%), integración (API + DB con TestContainers ≥ 85%)
- Frontend tests: unitarios (Vitest + RTL ≥ 75%), E2E (Playwright: login, Kanban, WIP)
- CI/CD: GitHub Actions (lint → test → build → security scan → deploy)
- Docker multi-stage builds (optimizados)
- README.md completo con instrucciones de setup
- Convenciones verificadas: Ruff, ESLint, Prettier, Conventional Commits
**Criterios de aceptación:**
- `pytest` pasa con cobertura ≥ 85%
- `vitest` pasa con cobertura ≥ 75%
- Playwright E2E pasa en CI
- `make docker-build` produce imágenes optimizadas
- README permite a un nuevo dev levantar el proyecto en < 10 min

---

## Esquema de base de datos

### Tablas principales

**users** — id, nombre, email (unique), contraseña_hash, rol_id, fecha_registro, deleted_at, created_at, updated_at, created_by, updated_by
**roles** — id, nombre (ADMIN|PO|SM|DEVELOPER)
**projects** — id, nombre, descripcion, estado (ACTIVO|INACTIVO|FINALIZADO|CANCELADO), fecha_inicio, owner_id (FK users), deleted_at, audit cols
**project_assignments** — id, project_id, user_id, rol (SM|DEVELOPER), deleted_at
**modules** — id, project_id, nombre, descripcion, estado (ACTIVO|INACTIVO), deleted_at
**epicas** — id, project_id, titulo, descripcion, prioridad, estado, orden, deleted_at
**historias_usuario** — id, epica_id, modulo_id, titulo, descripcion, criterios_aceptacion, prioridad, estimacion, orden, deleted_at
**sprints** — id, project_id, nombre, objetivo, duracion_dias, fecha_inicio, fecha_fin, estado, deleted_at
**sprint_eventos** — id, sprint_id, tipo, fecha, notas, duracion_minutos, created_by
**tasks** — id, historia_usuario_id, sprint_id, assigned_to (FK users), titulo, descripcion, estado, fecha_creacion, fecha_limite, deleted_at
**task_state_transitions** — id, task_id, from_estado, to_estado, timestamp, user_id, reason
**messages** — id, proyecto_id (nullable), task_id (nullable), sender_id, contenido, fecha_envio, tipo (PROYECTO|TAREA)
**artifacts** — id, task_id, nombre, tipo, version_actual, deleted_at
**artifact_versions** — id, artifact_id, version, contenido_url, uploaded_by, created_at

### Índices clave
- users: unique(email) WHERE deleted_at IS NULL
- tasks: (assigned_to, estado) WHERE deleted_at IS NULL — para WIP count
- tasks: (sprint_id, estado) WHERE deleted_at IS NULL — para board query
- task_state_transitions: (task_id, timestamp) — historial
- task_state_transitions: particionado por mes en timestamp
- messages: (proyecto_id, fecha_envio) — chat history
- messages: (task_id, fecha_envio) — chat history
- epicas: (project_id, orden) — backlog ordering
- historias_usuario: (epica_id, orden) — backlog ordering

### Materialized Views
- mv_dashboard_metrics: project_id, sprint_id, total_tasks, tasks_by_status (jsonb), lead_time_avg, cycle_time_avg, throughput, wip_violations_count
- mv_sprint_velocity: sprint_id, project_id, planned_points, completed_points, velocity_percentage

---

## API REST endpoints

### Auth
- POST /api/v1/auth/register
- POST /api/v1/auth/login
- POST /api/v1/auth/logout
- POST /api/v1/auth/refresh
- POST /api/v1/auth/recover-password

### Users (Admin only)
- GET /api/v1/users, GET /api/v1/users/{id}, PATCH /api/v1/users/{id}, DELETE /api/v1/users/{id} (deactivate)
- PATCH /api/v1/users/{id}/role

### Projects
- GET/POST /api/v1/projects, GET/PATCH/DELETE /api/v1/projects/{id}
- GET/POST /api/v1/projects/{id}/modules, GET/PATCH/DELETE /api/v1/projects/{id}/modules/{id}
- GET/POST/DELETE /api/v1/projects/{id}/assignments

### Backlog
- GET/POST /api/v1/projects/{id}/epicas, PATCH/DELETE /api/v1/projects/{id}/epicas/{id}
- POST /api/v1/projects/{id}/epicas/{id}/historias, PATCH/DELETE /api/v1/projects/{id}/epicas/{id}/historias/{id}
- PUT /api/v1/projects/{id}/backlog/prioritize

### Sprints
- GET/POST /api/v1/projects/{id}/sprints, GET/PATCH/DELETE /api/v1/sprints/{id}
- POST /api/v1/sprints/{id}/start, POST /api/v1/sprints/{id}/close
- GET/POST /api/v1/sprints/{id}/events, PATCH/DELETE /api/v1/sprints/{id}/events/{id}

### Kanban
- GET /api/v1/boards/{sprintId}
- PATCH /api/v1/tasks/{id}/transition
- PATCH /api/v1/tasks/{id}/block, PATCH /api/v1/tasks/{id}/unblock

### Messages
- GET /api/v1/projects/{id}/messages, POST /api/v1/projects/{id}/messages
- GET /api/v1/tasks/{id}/messages, POST /api/v1/tasks/{id}/messages

### Artifacts
- GET/POST /api/v1/tasks/{id}/artifacts
- GET /api/v1/artifacts/{id}/versions, POST /api/v1/artifacts/{id}/versions

### Dashboard
- GET /api/v1/dashboard/{projectId}/metrics
- GET /api/v1/dashboard/{projectId}/velocity

### Health
- GET /health, GET /ready, GET /metrics

---

## Frontend routes

| Route | Page | Roles |
|-------|------|-------|
| /login | Login | Todos |
| /register | Register | Todos |
| /recover-password | RecoverPassword | Todos |
| /dashboard | Dashboard principal | PO, SM |
| /projects | ProjectList | PO, SM, Developer |
| /projects/new | ProjectForm | PO |
| /projects/:id | ProjectDetail | PO, SM, Developer |
| /projects/:id/backlog | Backlog | PO |
| /projects/:id/sprints | SprintList | SM, PO |
| /projects/:id/sprints/new | SprintPlanning | SM |
| /projects/:id/sprints/:sid | SprintDetail | SM, PO, Developer |
| /projects/:id/sprints/:sid/board | KanbanBoard | SM, PO, Developer |
| /projects/:id/sprints/:sid/events/:eid | SprintEventForm | SM |
| /admin/users | UserManagement | Admin |
| /profile | Profile | Todos |

---

## Risks / Trade-offs

| Riesgo | Mitigación |
|--------|-----------|
| Celery añade complejidad operativa para un proyecto pequeño | Simplificar a tareas sincrónicas o crontab si Celery resulta excesivo; el ADR permite esta flexibilidad |
| Materialized views pueden desactualizarse | Refresco cada 5 min es aceptable para dashboards; se muestra indicador de "última actualización" |
| WIP validation con race condition | Usar SELECT ... FOR UPDATE en la transacción o isolation level SERIALIZABLE |
| Drag & drop en frontend puede tener bugs sutiles | Tests E2E con Playwright cubriendo todos los escenarios de movimiento y error |
| Cobertura de tests 85% puede ser ambiciosa para frontend | Priorizar tests de integración y E2E sobre unitarios en frontend |

---

## Open Questions

1. ¿Almacenamiento de artefactos en filesystem local o interfaz para S3 futuro? → Local en v1, con interface IFileStorage para migrar a S3
2. ¿PgBouncer necesario en desarrollo? → Sí para simular producción, pero opcional en dev
3. ¿Notificaciones WebSocket deben persistirse? → Solo en memoria con Redis pub/sub; historial via REST
4. ¿Refresh token rotativo debe invalidar el anterior? → Sí, rotación con invalidación