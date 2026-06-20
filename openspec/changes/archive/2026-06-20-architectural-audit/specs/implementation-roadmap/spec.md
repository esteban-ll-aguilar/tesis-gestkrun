# Spec: Implementation Roadmap

## Description
Roadmap técnico detallado por fases para la implementación completa de GESTKRUN, incluyendo dependencias, archivos involucrados y criterios de aceptación.

## Requirements

### RR-01: Fase 1 — Infraestructura base
- Docker Compose con servicios: PostgreSQL 16, Redis, PgBouncer, Nginx
- Makefile con comandos comunes (up, down, logs, shell)
- Scripts de inicialización de BD (extensiones, roles)
- CI/CD básico: lint → test → build en GitHub Actions

### RR-02: Fase 2 — Modelo de dominio
- Implementar entidades, VOs, enums, eventos en `tesis-gestkrun-api/app/domain/`
- Implementar interfaces de repositorio
- Tests unitarios del dominio con cobertura ≥ 85%

### RR-03: Fase 3 — Persistencia
- Migraciones Alembic para todas las tablas
- Implementaciones SQLAlchemy de repositorios
- Índices compuestos, parciales, GIN, BRIN
- Particionamiento mensual en tablas de eventos y transiciones
- Materialized views para dashboards
- Soft delete + audit trail

### RR-04: Fase 4 — Autenticación y autorización
- JWT access (15 min) + refresh token (7 días, httpOnly)
- Argon2id para hashing de contraseñas
- RBAC con decoradores/dependencias por rol y recurso
- Rate limiting (100 req/min general, 20 req/min auth)
- Endpoints: register, login, logout, refresh, recover-password
- Flujo de registro con verificación de email

### RR-05: Fase 5 — Casos de uso (Application Layer)
- CreateProjectUseCase, AddModuleUseCase, AssignTeamUseCase
- CreateEpicaUseCase, AddHistoriaUsuarioUseCase, PrioritizeBacklogUseCase
- PlanSprintUseCase, StartSprintUseCase, CloseSprintUseCase
- MoveTaskUseCase (con validación WIP), BlockTaskUseCase
- RegisterDailyScrumUseCase, RegisterReviewUseCase, RegisterRetroUseCase
- SendMessageUseCase, UploadArtifactUseCase
- GetDashboardMetricsUseCase, GetSprintVelocityUseCase
- Tests de integración para cada caso de uso

### RR-06: Fase 6 — API REST
- Routers FastAPI v1: /auth, /users, /projects, /modules, /epicas, /historias, /sprints, /tasks, /messages, /artifacts, /dashboard, /metrics
- Validación Pydantic v2 en requests/responses
- Documentación OpenAPI 3.1 + Redoc
- Formato Problem+JSON (RFC 7807) para errores
- Paginación cursor-based en listados

### RR-07: Fase 7 — Frontend
- Landing / Login / Register
- Dashboard principal con métricas
- Tablero Kanban con drag & drop (@dnd-kit)
- Product Backlog con drag & drop de priorización
- Sprint Planning: selección de historias, creación de sprint
- Sprint events: Daily, Review, Retro forms
- Chat por proyecto y tarea (WebSocket + REST history)
- Gestión de artefactos (upload, versionado, preview)
- Admin panel: usuarios, roles, proyectos globales
- Responsive: desktop primario, tablet secundario
- i18n: español (primario), inglés (secundario)

### RR-08: Fase 8 — Workers y tareas background
- Celery tasks: refresh materialized views (cada 5 min)
- Celery tasks: notificaciones (WebSocket push)
- Celery tasks: auditoría WIP (reporte diario)
- Monitoreo con Flower

### RR-09: Fase 9 — Pruebas
- Backend: tests unitarios (dominio), integración (API + DB con TestContainers), async workers
- Frontend: unitarios (Vitest + RTL), integración (MSW), E2E (Playwright: login, Kanban, WIP)
- Cobertura mínima: 85% backend, 75% frontend

### RR-10: Fase 10 — CI/CD y despliegue
- GitHub Actions: lint (Ruff, ESLint), test (pytest, Vitest, Playwright), build, security scan (Bandit, Semgrep, npm audit)
- Docker multi-stage builds
- Despliegue a staging con Docker Compose
- Monitoreo: Prometheus + Grafana + Loki + Alertmanager

## Invariants
- Las fases deben ejecutarse en orden secuencial (cada fase depende de la anterior)
- No se puede saltar una fase
- Cada fase debe completar todos sus criterios de aceptación antes de avanzar