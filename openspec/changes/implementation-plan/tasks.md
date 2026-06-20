## 1. Infraestructura base

- [x] 1.1 Crear Docker Compose con PostgreSQL 16, Redis, PgBouncer, Nginx
- [x] 1.2 Crear Makefile con comandos: up, down, logs, shell, test, lint, migrate
- [x] 1.3 Inicializar proyecto FastAPI con Poetry: estructura de carpetas, dependencias
- [x] 1.4 Implementar Pydantic BaseSettings (configuración vía .env)
- [x] 1.5 Implementar logging con structlog + correlation_id
- [x] 1.6 Implementar manejador centralizado de excepciones (Problem+JSON)
- [x] 1.7 Implementar health endpoints: /health, /ready, /metrics
- [x] 1.8 Inicializar proyecto React con Vite + TypeScript + Tailwind + shadcn/ui
- [x] 1.9 Configurar React Router v6 con lazy loading
- [x] 1.10 Configurar providers: QueryClient, Theme, i18n
- [x] 1.11 Implementar layouts: AuthLayout, MainLayout, AdminLayout
- [x] 1.12 Configurar CI/CD base: lint → test → build en GitHub Actions

## 2. Modelo de dominio

- [x] 2.1 Crear enums: Rol, EstadoTarea, EstadoSprint, EstadoProyecto, EstadoModulo, Prioridad, TipoArtefacto, TipoMensaje, TipoEventoScrum
- [x] 2.2 Crear Value Objects: Email, PasswordHash, EstimacionEsfuerzo (1-21), UserId, ProjectId, TaskId, SprintId, EpicaId, WIPCount
- [x] 2.3 Crear entidad User con Email, PasswordHash, Rol
- [x] 2.4 Crear entidad Project con EstadoProyecto
- [x] 2.5 Crear entidad Module con EstadoModulo
- [x] 2.6 Crear entidad Epica con Prioridad
- [x] 2.7 Crear entidad HistoriaUsuario con Prioridad, EstimacionEsfuerzo
- [x] 2.8 Crear entidad Sprint con EstadoSprint
- [x] 2.9 Crear entidad SprintEvento con TipoEventoScrum
- [x] 2.10 Crear entidad Task con EstadoTarea
- [x] 2.11 Crear entidad TaskStateTransition (audit log de transiciones)
- [x] 2.12 Crear entidad Message con TipoMensaje
- [x] 2.13 Crear entidad Artifact con TipoArtefacto
- [x] 2.14 Crear entidad ArtifactVersion
- [x] 2.15 Crear Domain Events (13 eventos)
- [x] 2.16 Crear Domain Services: WIPValidationService, KanbanFlowService, MetricsCalculationService
- [x] 2.17 Crear interfaces de repositorio por aggregate
- [x] 2.18 Escribir tests unitarios del dominio (entidades, VOs, servicios, eventos)
- [x] 2.19 Verificar invariantes en tests (WIP ≤ 3, solo PO prioriza, etc.)

## 3. Persistencia

- [x] 3.1 Crear migración Alembic inicial con tabla users + roles (seed data)
- [x] 3.2 Crear tablas: projects, project_assignments, modules
- [x] 3.3 Crear tablas: epicas, historias_usuario
- [x] 3.4 Crear tablas: sprints, sprint_eventos, tasks
- [x] 3.5 Crear tabla task_state_transitions con particionamiento mensual
- [x] 3.6 Crear tablas: messages, artifacts, artifact_versions
- [x] 3.7 Crear índices compuestos y parciales
- [x] 3.8 Crear materialized views: mv_dashboard_metrics, mv_sprint_velocity
- [x] 3.9 Implementar SQLAlchemy repositories (todos los aggregates)
- [x] 3.10 Implementar soft-delete + audit trail (campos created_by, updated_by)
- [x] 3.11 Escribir tests de integración con TestContainers

## 4. Autenticación y autorización

- [ ] 4.1 Implementar PasswordHasher (Argon2id)
- [ ] 4.2 Implementar JWTProvider (access 15 min, refresh 7 días)
- [ ] 4.3 Implementar endpoint POST /auth/register
- [ ] 4.4 Implementar endpoint POST /auth/login
- [ ] 4.5 Implementar endpoint POST /auth/refresh (rotación con invalidación)
- [ ] 4.6 Implementar endpoint POST /auth/logout
- [ ] 4.7 Implementar endpoint POST /auth/recover-password
- [ ] 4.8 Implementar dependencias: get_current_user, require_role, require_project_role
- [ ] 4.9 Implementar rate limiting (100 req/min general, 20 req/min auth)
- [ ] 4.10 Frontend: Login page con validación Zod
- [ ] 4.11 Frontend: Register page
- [ ] 4.12 Frontend: RecoverPassword page
- [ ] 4.13 Frontend: Auth guard y role guards en React Router
- [ ] 4.14 Frontend: Refresh token interceptor
- [ ] 4.15 Frontend: Auth store (Zustand)
- [ ] 4.16 Tests de integración de auth

## 5. API REST — Proyectos, Módulos, Equipos

- [ ] 5.1 Backend: CreateProjectUseCase + endpoint POST /projects
- [ ] 5.2 Backend: GetProjectsUseCase + endpoint GET /projects (paginación cursor)
- [ ] 5.3 Backend: UpdateProjectUseCase + PATCH /projects/{id}
- [ ] 5.4 Backend: DeleteProjectUseCase (soft) + DELETE /projects/{id}
- [ ] 5.5 Backend: Módulos CRUD + endpoints
- [ ] 5.6 Backend: Team assignment + endpoint POST /projects/{id}/assignments
- [ ] 5.7 Frontend: ProjectList page con DataTable
- [ ] 5.8 Frontend: ProjectForm (create/edit) con React Hook Form + Zod
- [ ] 5.9 Frontend: ProjectDetail page con tabs (módulos, equipo)
- [ ] 5.10 Frontend: Team management UI

## 6. Backlog y Sprints

- [ ] 6.1 Backend: CRUD épicas + endpoints
- [ ] 6.2 Backend: CRUD historias de usuario + endpoints
- [ ] 6.3 Backend: Priorización de backlog (PUT /backlog/prioritize)
- [ ] 6.4 Backend: PlanSprintUseCase + POST /sprints
- [ ] 6.5 Backend: StartSprintUseCase + POST /sprints/{id}/start
- [ ] 6.6 Backend: CloseSprintUseCase + POST /sprints/{id}/close
- [ ] 6.7 Backend: CRUD sprint eventos + endpoints
- [ ] 6.8 Frontend: Backlog page con drag & drop (épicas + historias)
- [ ] 6.9 Frontend: SprintPlanning wizard con selección de historias
- [ ] 6.10 Frontend: SprintList + SprintDetail pages
- [ ] 6.11 Frontend: SprintEvent forms (Daily, Review, Retro)

## 7. Tablero Kanban

- [ ] 7.1 Backend: WIPValidationService (conteo por usuario, máx 3)
- [ ] 7.2 Backend: KanbanFlowService (transiciones válidas)
- [ ] 7.3 Backend: PATCH /tasks/{id}/transition (con validación WIP + audit log)
- [ ] 7.4 Backend: PATCH /tasks/{id}/block, /tasks/{id}/unblock
- [ ] 7.5 Backend: GET /boards/{sprintId}
- [ ] 7.6 Frontend: KanbanBoard con @dnd-kit (6 columnas)
- [ ] 7.7 Frontend: Optimistic update + rollback en drag & drop
- [ ] 7.8 Frontend: Alerta visual WIP (2/3 amarillo, 3/3 bloqueo)
- [ ] 7.9 Frontend: Task detail modal (transiciones, bloqueo, asignación)
- [ ] 7.10 Frontend: Impediment management (causa, responsable)
- [ ] 7.11 Tests E2E con Playwright del flujo Kanban

## 8. Mensajería y Artefactos

- [ ] 8.1 Backend: SendMessageUseCase + POST messages
- [ ] 8.2 Backend: GetMessagesUseCase (paginación cursor-based)
- [ ] 8.3 Backend: WebSocket handler para mensajes en tiempo real
- [ ] 8.4 Frontend: Chat panel con scroll infinito
- [ ] 8.5 Frontend: WebSocket connection para tiempo real
- [ ] 8.6 Backend: UploadArtifactUseCase + POST /artifacts
- [ ] 8.7 Backend: Versionado automático + endpoints de versiones
- [ ] 8.8 Backend: Download endpoint
- [ ] 8.9 Frontend: Upload zone con drag & drop
- [ ] 8.10 Frontend: Artifact list + version history + preview

## 9. Dashboard y Métricas

- [ ] 9.1 Backend: Celery task para refresh de materialized views (cada 5 min)
- [ ] 9.2 Backend: GET /dashboard/{projectId}/metrics
- [ ] 9.3 Backend: GET /dashboard/{projectId}/velocity
- [ ] 9.4 Frontend: Dashboard page con cards de métricas
- [ ] 9.5 Frontend: Velocity chart (Recharts bar chart)
- [ ] 9.6 Frontend: Lead time / Cycle time chart (line chart)
- [ ] 9.7 Frontend: Throughput chart (area chart)
- [ ] 9.8 Frontend: Task distribution by status (donut chart)
- [ ] 9.9 Frontend: Bloqueadas activas alert

## 10. Calidad, CI/CD y documentación

- [ ] 10.1 Backend: Tests unitarios del dominio (meta: ≥ 90%)
- [ ] 10.2 Backend: Tests de integración API + DB (meta: ≥ 85%)
- [ ] 10.3 Frontend: Tests unitarios con Vitest + RTL (meta: ≥ 75%)
- [ ] 10.4 Frontend: Tests de integración con MSW
- [ ] 10.5 E2E: Login flow con Playwright
- [ ] 10.6 E2E: Kanban drag & drop + WIP validation
- [ ] 10.7 E2E: Sprint planning flow
- [ ] 10.8 CI/CD: Ruff lint en GitHub Actions
- [ ] 10.9 CI/CD: ESLint + Prettier en GitHub Actions
- [ ] 10.10 CI/CD: Security scan (Bandit, Semgrep, npm audit)
- [ ] 10.11 CI/CD: Docker multi-stage builds
- [ ] 10.12 Completar README.md con instrucciones de setup
- [ ] 10.13 Verificar cobertura ≥ 85% backend
- [ ] 10.14 Verificar cobertura ≥ 75% frontend