# GESTKRUN — Software Architecture

> **Infraestructura de software para la gestión de proyectos bajo el marco Scrumban**

**Versión:** 2.0.0\
**Fecha:** 2026-06-20\
**Basado en:** [product.md](../product.md) (spec), [config.yaml](../config.yaml) (invariants y SLOs)

---

## Sección 5 — Arquitectura de Software

### Stack Tecnológico

| Componente | Tecnología | Función |
|------------|-----------|---------|
| **Frontend** | React 18 + TypeScript 5.3 + Vite + Tailwind CSS | Interfaz de usuario, tablero Kanban, dashboards, formularios |
| **State Management** | Zustand + TanStack Query v5 | Estado global y sincronización de datos del servidor |
| **Backend** | Python 3.12 + FastAPI 0.110 | API RESTful, validación Pydantic v2, inyección de dependencias |
| **ORM / DB Access** | SQLAlchemy 2.0 (async) + Alembic | Modelado declarativo, migraciones, queries optimizadas |
| **Base de datos** | PostgreSQL 16 + PgBouncer | Datos relacionales, JSONB, índices parciales, connection pooling |
| **Cache / Broker** | Redis | Caché de sesiones, pub/sub para notificaciones, Celery broker |
| **Background Tasks** | Celery + Redis | Cálculo de métricas, refresh de materialized views, notificaciones |
| **Auth** | python-jose + passlib + OAuth2PasswordBearer | JWT (access + refresh), RBAC, hashing seguro |
| **API Docs** | FastAPI native (OpenAPI 3.1) + Redoc | Documentación interactiva auto-generada |
| **Reverse Proxy** | Nginx | SSL termination, rate limiting, compresión, servicio de estáticos |
| **Monitoreo** | Prometheus + Grafana + Loki | Métricas de aplicación, logs estructurados, alertas |
| **Deploy** | Docker + Docker Compose + GitHub Actions | Contenedores, CI/CD automatizado, despliegue a staging |

### Flujo de datos

```
Usuario → React (Vite) → Nginx → FastAPI (Uvicorn/Gunicorn)
                                        ↓
                                  SQLAlchemy (async)
                                        ↓
                                  PostgreSQL 16  ←→  PgBouncer
                                        ↓
                                  Redis (Cache + Pub/Sub)
                                        ↓
                                  Celery Workers (Background)
```

### Arquitectura de capas (Clean Architecture + DDD)

```
┌──────────────────────────────────────────────────────────────┐
│  Presentation Layer (React + TanStack Query + Zustand)       │
├──────────────────────────────────────────────────────────────┤
│  API Layer (FastAPI Routers + Dependency Injection)          │
├──────────────────────────────────────────────────────────────┤
│  Application Layer (Use Cases / Services)                    │
│  - CreateProjectUseCase, MoveTaskUseCase, PlanSprintUseCase  │
│  - WIPValidationService, MetricsCalculationService           │
│  - kanbanFlowService, etc.                                   │
├──────────────────────────────────────────────────────────────┤
│  Domain Layer (Entities, Value Objects, Aggregates)          │
│  - User, Project, Sprint, Task, HistoriaUsuario, Epica       │
│  - EstadoTarea, EstadoSprint, Prioridad, Rol, EstadoModulo   │
│  - Domain Events: TaskTransitioned, WIPViolated, SprintClosed │
├──────────────────────────────────────────────────────────────┤
│  Infrastructure Layer (Repositories, DB, Cache, Email)       │
│  - SQLAlchemyRepository, RedisCache, CeleryTaskQueue         │
│  - JWTProvider, PasswordHasher, LocalFileStorage             │
└──────────────────────────────────────────────────────────────┘
```

### Bounded Contexts (DDD)

| Bounded Context | Agregado Raíz | Entidades | Value Objects | Eventos de Dominio |
|----------------|---------------|-----------|---------------|-------------------|
| **Identity & Access Management** | User | User | Email, PasswordHash, UserId | UserRegistered, UserRoleChanged, UserDeactivated |
| **Project Management** | Project | Project, Module, TeamAssignment | ProjectId, ModuleId, ProjectStatus | ProjectCreated, ModuleAdded, TeamAssigned |
| **Backlog Management** | Epica | Epica, HistoriaUsuario | HistoriaUsuarioId, Prioridad, EstimacionEsfuerzo | EpicaCreated, HistoriaUsuarioAdded, BacklogPrioritized |
| **Sprint Management** | Sprint | Sprint, SprintEvento | SprintId, Duracion, SprintStatus | SprintPlanned, SprintStarted, SprintClosed, DailyScrumRegistered |
| **Kanban Flow** | Task | Task, TaskStateTransition | TaskId, EstadoTarea, WIPCount | TaskMoved, WIPViolated, TaskBlocked |
| **Communication** | Message | Message | MessageId, TipoMensaje | MessageSent |
| **Artifact Management** | Artifact | Artifact, ArtifactVersion | ArtifactId, TipoArtefacto, VersionNumber | ArtifactUploaded, VersionCreated |

### Estrategia de persistencia

- **Aggregates principales:** `Project`, `Sprint`, `Task`, `User`, `Epica`, `HistoriaUsuario`.
- **Cada aggregate tiene su propio repositorio** con interfaz en dominio e implementación en infraestructura.
- **Event sourcing ligero** para transiciones de estado de tareas (tabla `task_state_transitions`).
- **Soft delete** en todas las entidades con `deleted_at` + índices parciales.
- **Audit trail** vía triggers en PostgreSQL para campos `created_at`, `updated_at`, `created_by`, `updated_by`.
- **Particionamiento mensual** en tablas de alta cardinalidad (task_state_transitions, eventos, métricas).
- **Materialized views** para dashboards de métricas (refresco cada 5 min vía Celery).

---

## Sección 6 — Requisitos No Funcionales

### Rendimiento
- El cambio de estado de una tarea (drag & drop) debe reflejarse visualmente en < 100ms (optimistic UI).
- La validación WIP en backend debe responder en < 50ms.
- El Dashboard del proyecto debe cargarse completamente en < 2s con conexión estándar.
- Las métricas agregadas (lead time, cycle time) deben servirse desde materialized views con latencia < 3s.
- La lista de backlog con > 500 historias debe paginarse con cursor-based (50 items/página) en < 200ms.

### Seguridad
- Autenticación con JWT: access token de 15 min, refresh token de 7 días en httpOnly cookie.
- RBAC estricto: control de acceso a rutas y recursos según rol global y rol de proyecto.
- Rate limiting: 100 req/min por usuario en endpoints generales, 20 req/min en autenticación.
- Hashing de contraseñas con Argon2id (configuración OWASP recomendada).
- Sanitización de inputs para prevenir XSS e inyección SQL (SQLAlchemy ORM + Pydantic validación).
- Registro de logs de auditoría para cambios críticos: transiciones de estado, eliminación de artefactos, cambios de rol.
- Secrets management: variables de entorno en `.env` nunca commiteadas; uso de Docker secrets en producción.

### Fiabilidad y Consistencia
- Validación WIP estricta **desde el backend**; el frontend solo es capa de presentación.
- Transacciones atómicas para operaciones complejas (crear sprint + derivar tareas + asignar a tablero).
- Manejo de excepciones centralizado con formato Problem+JSON (RFC 7807).
- Retry automático con backoff exponencial en operaciones de Celery.
- Health checks en `/health`, `/ready` y `/metrics` para orquestación de contenedores.

### Compatibilidad y Accesibilidad
- Compatible con Chrome, Firefox, Edge y Safari en últimas 2 versiones.
- Responsive Design: escritorio (primario) y tablet (secundario). No móvil nativo en v1.
- Cumplimiento WCAG 2.1 nivel AA: contraste de colores, navegación por teclado, etiquetas ARIA en tablero Kanban.
- Internacionalización: español (primario) e inglés (secundario).

### Escalabilidad
- Arquitectura stateless: cualquier instancia de FastAPI puede atender cualquier request.
- Horizontal scaling: múltiples workers Uvicorn detrás de Nginx load balancer.
- PostgreSQL: read replicas para consultas de reportes y dashboards (CQRS).
- Redis: cache de sesiones y resultados de métricas frecuentes (TTL 5 min).
- Celery: workers independientes para procesamiento asíncrono de métricas y notificaciones.

### Mantenibilidad
- Cobertura de tests: mínimo 85% backend, 75% frontend.
- Documentación de API auto-generada y siempre actualizada (OpenAPI 3.1).
- ADRs para decisiones arquitectónicas críticas (ver `/docs/adr/`).
- C4 Model para documentación visual de arquitectura (ver `/docs/c4/`).
- Conventional Commits + semantic versioning para releases.
- Monorepo estructurado: `/backend`, `/frontend`, `/docs`, `/infra`, `/scripts`.

---

## Estructura del proyecto

```
GESTKRUN
│
├── tesis-gestkrun-api/
│   ├── app/
│   │   ├── api/
│   │   │   ├── v1/
│   │   │   ├── dependencies.py
│   │   │   └── router.py
│   │   ├── core/
│   │   ├── domain/
│   │   │   ├── entities/
│   │   │   ├── value_objects/
│   │   │   ├── repositories/
│   │   │   └── services/
│   │   ├── application/
│   │   │   ├── use_cases/
│   │   │   ├── dto/
│   │   │   └── interfaces/
│   │   ├── infrastructure/
│   │   │   ├── persistence/
│   │   │   ├── cache/
│   │   │   ├── auth/
│   │   │   └── messaging/
│   │   ├── workers/
│   │   └── main.py
│   └── tests/
│
├── tesis-gestkrun-web/
│   ├── src/
│   │   ├── app/
│   │   ├── pages/
│   │   ├── features/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── services/
│   │   ├── stores/
│   │   ├── types/
│   │   └── utils/
│   └── public/
│
├── docs/
│   ├── adr/           (Architecture Decision Records)
│   ├── c4/            (C4 Model diagrams)
│   └── uml/           (UML diagrams)
├── infra/
├── docker/
├── scripts/
├── product.md
├── config.yaml
└── README.md
```

---

*Documento de arquitectura. La especificación del producto está en [product.md](../product.md). Los invariants y SLOs están en [config.yaml](../config.yaml).*
