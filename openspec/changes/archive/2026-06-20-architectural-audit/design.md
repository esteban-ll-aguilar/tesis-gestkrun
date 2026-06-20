## Context

GESTKRUN es una plataforma web para gestión de proyectos de desarrollo de software bajo Scrumban. Actualmente la documentación del proyecto consiste en un único archivo `docs/architecture.md` (569 líneas) que mezcla:
- Especificación del producto (visión, usuarios, funcionalidades, flujos)
- Arquitectura de software (stack, capas, bounded contexts)
- Requisitos no funcionales (rendimiento, seguridad, escalabilidad)

Adicionalmente existe:
- `docs/uml/Scrum-Diagrama de clases.json`: diagrama de clases en formato Draw.io
- `openspec/config.yaml`: configuración del proceso SDD con invariants y SLOs

No existen: `product.md` independiente, `config.yaml` en raíz, diagramas UML de secuencia/estado/actividad, ADRs, C4Model, ni specs formales en `openspec/specs/`.

Esta auditoría analiza toda la documentación existente, identifica inconsistencias, elementos faltantes y genera un plan de acción completo.

---

## Hallazgos de la Auditoría

### 1. Inconsistencias encontradas

| # | Inconsistencia | Detalle |
|---|---------------|---------|
| I1 | Architecture.md referencia `config.yaml` en raíz para invariants pero no existe | Sección 6 dice "Invariants documentadas en config.yaml", pero el único config.yaml está en `openspec/` |
| I2 | El diagrama UML usa `Rol` como clase en lugar de Enum | El dominio define 4 roles fijos (Admin, PO, SM, Developer), debería ser un enumeration |
| I3 | El UML tiene `Modulo` con relación 1..* a Sprint, pero la spec dice que los Sprints pertenecen al Proyecto directamente | Contradicción: la tabla de casos de uso dice "SM configura Sprints", no que los módulos los organicen |
| I4 | `TipoMensaje` incluye `MODULO` y `PRIVADO` que no aparecen en la spec | product.md Área 9 solo menciona mensajería a nivel de proyecto y tarea. No hay concepto de mensaje privado ni por módulo |
| I5 | `EstadoProyecto` incluye `PAUSADO` no documentado en funcionalidades | La spec Área 2 solo menciona activo/inactivo |
| I6 | `HistoriaUsuario` sin relación al `Modulo` en UML | product.md Área 3 dice "asociar historias a módulos", pero el UML conecta Proyecto→HistoriaUsuario directamente |
| I7 | Invariants en `openspec/config.yaml` línea 183-190 mencionan reglas no documentadas en product.md | Ej: "Admin no puede crear proyectos" no aparece explícito en las tablas de casos de uso |
| I8 | SLOs en `openspec/config.yaml` (línea 196-203) tienen métricas diferentes a architecture.md | Ej: architecture.md dice dashboard < 2s, config.yaml dice < 2s (consistentes) pero architecture.md dice WIP backend < 50ms (consistente) — sin embargo, P99 no está definido en architecture.md |
| I9 | El UML tiene `validarLimiteWIP()` en `Usuario`, pero la validación WIP debería estar en el **dominio del tablero Kanban**, no en el usuario | Responsabilidad mal ubicada: el WIP es una invariante del flujo de trabajo, no del usuario |
| I10 | No existe la entidad `Épica` en el UML | product.md Área 3 menciona épicas como primer-class citizen del backlog, pero el UML solo tiene `HistoriaUsuario` |

### 2. Elementos faltantes

| # | Elemento faltante | Justificación |
|---|------------------|---------------|
| F1 | `product.md` independiente en la raíz | Especificación pura del producto, referenciada por `docs/architecture.md` y por el proceso SDD |
| F2 | `config.yaml` en la raíz con invariants + SLOs | Referenciado desde `docs/architecture.md` sección 6; contenido actualmente en `openspec/config.yaml` pero debe separarse |
| F3 | Entidad `Épica` en el dominio | Backlog tiene épicas como contenedores de historias de usuario |
| F4 | Value Object `Email`, `ContraseñaHash`, `EstimacionEsfuerzo` | Clean Architecture + DDD: atributos con comportamiento de validación propio |
| F5 | Enum `EstadoModulo` en UML | Existe en el JSON (referencia `EstadoModulo`) pero sin definición de valores |
| F6 | Enum `Rol` como enumeration en UML | Actualmente modelado como clase, debe ser enum con ADMIN, PO, SM, DEVELOPER |
| F7 | Domain Events completos: `TaskTransitioned`, `WIPViolated`, `SprintClosed`, `UserAssigned`, `ArtifactUploaded` | Architecture.md menciona solo `TaskTransitioned` y `WIPViolated`; hacen falta los demás |
| F8 | Agregados DDD formales: `Project`, `Sprint`, `Task`, `User`, `HistoriaUsuario` están nombrados pero sin definir boundaries ni reglas de consistencia transaccional | Architecture.md los menciona pero no define qué va dentro de cada aggregate |
| F9 | Repositorios: solo mencionados genéricamente, falta definir interfaces de repositorio por aggregate | Se necesitan `IUserRepository`, `IProjectRepository`, `ISprintRepository`, `ITaskRepository`, `IHistoriaUsuarioRepository` |
| F10 | Casos de uso formales: la spec lista funcionalidades pero no como casos de uso con pre/post condiciones | Faltan UC: `CreateProjectUseCase`, `MoveTaskUseCase`, `PlanSprintUseCase`, `RegisterDailyScrumUseCase`, etc. |
| F11 | Diagrama de secuencia: flujo de transición WIP (feliz + error) | Documentado textualmente en product.md Flujo 1 y 2, pero sin diagrama |
| F12 | Diagrama de secuencia: Sprint Planning | Documentado textualmente en product.md Flujo 3 y 4 |
| F13 | Diagrama de estado: ciclo de vida de `Tarea` | PENDIENTE → EN_PROCESO → BLOQUEADO → EN_REVISION → TERMINADO / CANCELADO (con transiciones válidas) |
| F14 | Diagrama de estado: ciclo de vida de `Sprint` | PLANIFICADO → EN_EJECUCION → FINALIZADO / CANCELADO |
| F15 | Diagrama de actividad: flujo completo backlog → sprint → kanban | Flujo cross-bounded context que merece diagrama |
| F16 | ADRs: decisiones arquitectónicas ya tomadas sin documentar | Ej: por qué FastAPI sobre Django, por qué CQRS, por qué Celery + Redis, por qué PostgreSQL, por qué Zustand + TanStack Query |
| F17 | C4Model: diagrama de Context (sistema, actores externos) | No existe |
| F18 | C4Model: diagrama de Container (backend, frontend, DB, cache, workers) | No existe |
| F19 | C4Model: diagrama de Component (dentro de backend: API, Application, Domain, Infrastructure) | No existe |
| F20 | Índices de base de datos compuestos documentados | Mencionados genéricamente pero sin especificar índices por tabla |
| F21 | Particionamiento de tablas de alta cardinalidad | Mencionado pero sin especificar clave de partición para cada tabla |
| F22 | Tabla `task_state_transitions` (event sourcing ligero) | Mencionada en architecture.md pero sin atributos definidos |
| F23 | Audit trail: tabla genérica o columnas `created_by`, `updated_by` | Mencionado pero sin schema definido |
| F24 | Materialized views para dashboards | Mencionadas sin especificar columnas ni frecuencia de refresco |

---

## Goals / Non-Goals

**Goals:**
1. Separar docs/architecture.md en archivos independientes: product.md, architecture.md puro, config.yaml
2. Auditar y corregir el diagrama de clases UML
3. Crear diagramas UML faltantes (secuencia x2, estado x2, actividad x1)
4. Crear ADRs para las decisiones arquitectónicas clave ya tomadas
5. Crear C4Model base (Context, Container, Component)
6. Definir Bounded Contexts formales con agregados, entidades, value objects, eventos
7. Definir interfaces de repositorio y casos de uso
8. Generar roadmap de implementación con fases, archivos, dependencias y criterios de aceptación
9. Actualizar modelado del dominio completo

**Non-Goals:**
- No se escribe código backend/frontend
- No se modifican archivos en `tesis-gestkrun-api/` ni `tesis-gestkrun-web/`
- No se configura CI/CD, infraestructura Docker, ni herramientas
- No se generan migraciones Alembic
- No se modifica `openspec/config.yaml` ni el proceso SDD

---

## Decisions

### D1: Separar docs/architecture.md en 3 archivos independientes
**Decisión:** El archivo actual será dividido en:
- `/product.md`: Secciones 1-4 (Visión, Usuarios, Funcionalidades, Flujos) + Fuera de alcance + Checklist
- `/config.yaml`: Invariants del dominio + SLOs de rendimiento
- `/docs/architecture.md`: Secciones 5-6 (Stack, Arquitectura, Bounded Contexts, Persistencia, NFRs mantenibles)
**Rationale:** Spec-First requiere que la especificación del producto sea un documento independiente y autónomo. La arquitectura debe ser un documento técnico separado. Los invariants y SLOs necesitan un formato estructurado (YAML) para validación automatizada.
**Alternativas consideradas:** Mantener un solo archivo — rechazado porque viola el principio de separación de concerns y dificulta la trazabilidad.

### D2: Rol como enumeration, no como clase
**Decisión:** `Rol` pasa de clase con atributos (`id`, `nombre`, `descripcion`, `permisos`) a `«enumeration» Rol` con valores: `ADMIN`, `PRODUCT_OWNER`, `SCRUM_MASTER`, `DEVELOPER`.
**Rationale:** Los roles del dominio son fijos y conocidos en tiempo de diseño. Modelarlos como tabla dinámica añade complejidad innecesaria (over-engineering). Si en el futuro se requieren roles dinámicos, se puede migrar a tabla sin romper la interfaz.
**Alternativas consideradas:** Mantener como clase — viola KISS y no hay requerimiento de roles dinámicos en el alcance v1.

### D3: WIP validation en el dominio del Kanban, no en Usuario
**Decisión:** `validarLimiteWIP()` se mueve de la entidad `Usuario` al `KanbanFlowService` (Domain Service). La responsabilidad de contar tareas en EN_PROCESO por usuario recae en el servicio de dominio, no en el usuario.
**Rationale:** El WIP es una invariante del flujo de trabajo, no una propiedad del usuario. El usuario "tiene" tareas, pero la validación del límite es una regla de negocio que cruza múltiples agregados (User + Task + Sprint).
**Alternativas consideradas:** Mantener en Usuario — acoplamiento incorrecto, viola Single Responsibility Principle.

### D4: Mensajería solo a nivel proyecto y tarea
**Decisión:** Eliminar `TipoMensaje.MODULO` y `TipoMensaje.PRIVADO` del dominio. Mantener solo `PROYECTO` y `TAREA`.
**Rationale:** El product.md Área 9 solo define mensajería a nivel de proyecto y tarea. Los tipos MODULO y PRIVADO no están especificados. Incluirlos sería gold-plating.

### D5: Épica como Aggregate separado
**Decisión:** Agregar entidad `Epica` como aggregate raíz independiente. Una `Epica` contiene 0..* `HistoriaUsuario`. A su vez, `HistoriaUsuario` deriva en 0..* `Tarea`.
**Rationale:** El product.md trata épicas como primer-class citizen del backlog con priorización y estimación. Sin la entidad, no se puede modelar correctamente la jerarquía backlog → épica → historia → tarea.
**Alternativas consideradas:** Hacer épica un atributo de HistoriaUsuario — pierde la semántica de contenedor y no permite priorizar a nivel épica.

---

## Arquitectura Actualizada

### Bounded Contexts (DDD formales)

| Bounded Context | Agregado Raíz | Entidades | Value Objects | Eventos de Dominio |
|----------------|---------------|-----------|---------------|-------------------|
| **Identity & Access Management** | `User` | User | Email, PasswordHash, UserId | UserRegistered, UserRoleChanged, UserDeactivated |
| **Project Management** | `Project` | Project, Module, TeamAssignment | ProjectId, ModuleId, ProjectStatus | ProjectCreated, ModuleAdded, TeamAssigned |
| **Backlog Management** | `Epica` | Epica, HistoriaUsuario | HistoriaUsuarioId, Prioridad, EstimacionEsfuerzo | EpicaCreated, HistoriaUsuarioAdded, BacklogPrioritized |
| **Sprint Management** | `Sprint` | Sprint, SprintEvento | SprintId, Duracion, SprintStatus | SprintPlanned, SprintStarted, SprintClosed, DailyScrumRegistered |
| **Kanban Flow** | `Task` | Task, TaskStateTransition | TaskId, EstadoTarea, WIPCount | TaskMoved, WIPViolated, TaskBlocked |
| **Communication** | `Message` | Message | MessageId, TipoMensaje, Timestamp | MessageSent |
| **Artifact Management** | `Artifact` | Artifact, ArtifactVersion | ArtifactId, TipoArtefacto, VersionNumber | ArtifactUploaded, VersionCreated |

### Capas Clean Architecture

```
┌──────────────────────────────────────────────────────────────┐
│  Presentation Layer (React)                                   │
│  Pages / Components / Hooks / Stores / Services              │
├──────────────────────────────────────────────────────────────┤
│  API Layer (FastAPI Routers)                                  │
│  v1/ routes, Dependencies (auth, pagination), Middleware      │
├──────────────────────────────────────────────────────────────┤
│  Application Layer (Use Cases)                                │
│  CreateProjectUseCase, MoveTaskUseCase, PlanSprintUseCase     │
│  RegisterDailyScrumUseCase, UploadArtifactUseCase, etc.      │
│  DTOs, Mappers, Interfaces (ports)                            │
├──────────────────────────────────────────────────────────────┤
│  Domain Layer (Enterprise + Kernel)                           │
│  Entities, Value Objects, Aggregates, Domain Services         │
│  Repository Interfaces, Domain Events, Enums                  │
│  Domain Services: KanbanFlowService, WIPValidationService,    │
│                   MetricsCalculationService                   │
├──────────────────────────────────────────────────────────────┤
│  Infrastructure Layer (Adapters)                              │
│  Persistence: SQLAlchemyRepository implementations            │
│  Auth: JWTProvider, PasswordHasher                            │
│  Cache: RedisCache                                            │
│  Messaging: CeleryTaskQueue, WebSocketNotifier                │
│  Files: LocalFileStorage / S3Adapter                          │
└──────────────────────────────────────────────────────────────┘
```

---

## UML Actualizado

### Entidades del Dominio (corregido vs. original)

**Correcciones al diagrama de clases existente:**

1. `Usuario` → se elimina `validarLimiteWIP()` (pasa a KanbanFlowService)
2. `Rol` → se convierte a `«enumeration» Rol { ADMIN, PRODUCT_OWNER, SCRUM_MASTER, DEVELOPER }`
3. `Usuario` se relaciona con `Rol` como 1..1 (cada usuario tiene exactamente un rol global)
4. `Proyecto` → se elimina `limiteWIP` (el WIP es configurable a nivel de proyecto, pero se implementa como columna del proyecto, no como límite duro; solo hay un límite de 3 en EN_PROCESO por usuario)
5. Se agrega entidad `Epica` entre `Proyecto` y `HistoriaUsuario`
6. `HistoriaUsuario` se relaciona con `Modulo` (pertenece a un módulo)
7. `Mensaje` → se eliminan tipos `MODULO` y `PRIVADO`, solo `PROYECTO` y `TAREA`
8. Se agrega `TaskStateTransition` como entidad independiente:
   - id: UUID, taskId: UUID, fromEstado: EstadoTarea, toEstado: EstadoTarea, timestamp: DateTime, userId: UUID, reason: String?
9. `EstadoModulo` → se define como enumeration: `ACTIVO, INACTIVO`
10. `Sprint` se relaciona directamente con `Proyecto` (no a través de Módulo)

### Nuevas entidades a agregar:

| Entidad | Tipo | Bounded Context | Atributos |
|---------|------|----------------|-----------|
| `Epica` | Aggregate Root | Backlog Management | id, projectId, titulo, descripcion, prioridad, estado |
| `TaskStateTransition` | Entity | Kanban Flow | id, taskId, fromEstado, toEstado, timestamp, userId, reason |
| `ArtifactVersion` | Entity | Artifact Management | id, artifactId, version, contenidoURL, uploadedBy, createdAt |
| `TeamAssignment` | Value Object | Project Management | projectId, userId, rol (SM/Developer) |

### Enums completos:

| Enum | Valores |
|------|---------|
| `Rol` | ADMIN, PRODUCT_OWNER, SCRUM_MASTER, DEVELOPER |
| `EstadoTarea` | PENDIENTE, EN_PROCESO, BLOQUEADO, EN_REVISION, TERMINADO, CANCELADO |
| `EstadoSprint` | PLANIFICADO, EN_EJECUCION, FINALIZADO, CANCELADO |
| `EstadoProyecto` | ACTIVO, INACTIVO, FINALIZADO, CANCELADO |
| `EstadoModulo` | ACTIVO, INACTIVO |
| `Prioridad` | BAJA, MEDIA, ALTA, CRITICA |
| `TipoArtefacto` | REQUISITO, DIAGRAMA, ACTA, DOCUMENTO, CODIGO |
| `TipoMensaje` | PROYECTO, TAREA |
| `TipoEventoScrum` | SPRINT_PLANNING, DAILY_SCRUM, SPRINT_REVIEW, SPRINT_RETROSPECTIVE |

### Diagramas UML a crear:

1. **Diagrama de clases** — corregir el existente con los cambios arriba indicados
2. **Diagrama de secuencia — Transición de tarea Kanban**: Developer → Frontend → Backend → Domain → DB → Dashboard
3. **Diagrama de secuencia — Sprint Planning**: SM → Frontend → Backend → Backlog → Sprint → Notificación
4. **Diagrama de estado — Tarea**: PENDIENTE → EN_PROCESO ↔ BLOQUEADO → EN_REVISION → TERMINADO / CANCELADO
5. **Diagrama de estado — Sprint**: PLANIFICADO → EN_EJECUCION → FINALIZADO / CANCELADO
6. **Diagrama de actividad — Flujo backlog → sprint → kanban**: épica → historia → sprint planning → tareas → kanban

### Nuevos Value Objects:

| Value Object | Atributos | Validaciones |
|-------------|-----------|-------------|
| `Email` | value: String | Formato email, único en sistema |
| `PasswordHash` | value: String | Hash Argon2id, mínimo 8 chars |
| `EstimacionEsfuerzo` | value: int | 1-21 (story points, Fibonacci) |
| `UserId` | value: UUID | --- |
| `ProjectId` | value: UUID | --- |
| `TaskId` | value: UUID | --- |
| `SprintId` | value: UUID | --- |
| `EpicaId` | value: UUID | --- |
| `HistoriaUsuarioId` | value: UUID | --- |
| `WIPCount` | value: int | 0-3 |

### Eventos de Dominio:

| Evento | Bounded Context | Payload |
|--------|----------------|---------|
| `UserRegistered` | IAM | userId, email, rol, timestamp |
| `UserRoleChanged` | IAM | userId, oldRol, newRol, changedBy |
| `ProjectCreated` | Project Management | projectId, name, ownerId, timestamp |
| `TeamAssigned` | Project Management | projectId, userId, rol |
| `EpicaCreated` | Backlog Management | epicaId, projectId, titulo, timestamp |
| `BacklogPrioritized` | Backlog Management | projectId, order[], timestamp |
| `SprintPlanned` | Sprint Management | sprintId, projectId, duracion, objetivo |
| `SprintClosed` | Sprint Management | sprintId, timestamp |
| `TaskMoved` | Kanban Flow | taskId, fromEstado, toEstado, userId, timestamp |
| `WIPViolated` | Kanban Flow | userId, taskId, currentWIPCount, maxWIP, timestamp |
| `TaskBlocked` | Kanban Flow | taskId, reason, blockedBy, timestamp |
| `MessageSent` | Communication | messageId, projectId/taskId, senderId, timestamp |
| `ArtifactUploaded` | Artifact Management | artifactId, taskId, tipo, version, uploadedBy |

---

## Riesgos / Trade-offs

| Riesgo | Mitigación |
|--------|-----------|
| Separar docs/architecture.md puede perder contexto entre secciones | Mantener referencias cruzadas explícitas entre archivos (xref) |
| Cambiar el UML sin actualizar el JSON de Draw.io deja el diagrama desactualizado | Incluir tarea explícita de regenerar el JSON en el roadmap |
| Definir agregados sin experiencia DDD puede llevar a boundaries incorrectos | Usar patrones estándar: un aggregate = una unidad transaccional |
| Los ADRs pueden quedar desactualizados si no se mantienen | Incluir en el roadmap tarea de ADR inicial; los siguientes se crean con cada cambio |

---

## Migration Plan

1. Crear `product.md` en raíz (extrayendo secciones 1-4 de docs/architecture.md)
2. Crear `config.yaml` en raíz (extrayendo invariants + SLOs de openspec/config.yaml)
3. Reescribir `docs/architecture.md` (solo arquitectura pura, secciones 5-6)
4. Corregir diagrama de clases UML (Draw.io JSON)
5. Crear diagramas UML faltantes (5 nuevos diagramas)
6. Crear ADRs iniciales (5-7 ADRs)
7. Crear C4Model (3 diagramas)
8. Actualizar openspec/config.yaml para referenciar product.md y config.yaml raíz
9. Generar roadmap final en tasks.md

---

## Open Questions

1. ¿El límite WIP de 3 debe ser configurable por proyecto o es fijo? (act: configurable a nivel de proyecto, po default 3)
2. ¿Las épicas pueden tener prioridad independiente de sus historias? (act: sí, prioridad de épica propaga)
3. ¿El refresh token rotativo debe invalidar el anterior? (act: sí, rotación con invalidación)
4. ¿Las notificaciones WebSocket deben persistirse? (act: solo en memoria con Redis pub/sub)
5. ¿Los artefactos se almacenan en filesystem local o S3? (act: local para v1, interface para S3 futuro)

---

## Roadmap de Implementación

### Fase 1: Separación de documentación base
**Objetivo:** Separar docs/architecture.md en product.md + config.yaml + architecture.md
**Archivos:** `/product.md`, `/config.yaml`, `/docs/architecture.md`
**Dependencias:** Ninguna
**Criterios de aceptación:**
- product.md contiene visión, usuarios, funcionalidades, flujos, fuera de alcance
- config.yaml contiene invariants (8 reglas) y SLOs (7 métricas)
- architecture.md contiene stack, capas, bounded contexts, persistencia, NFRs

### Fase 2: Corrección del modelo de dominio
**Objetivo:** Auditar y corregir el diagrama de clases UML + agregar entidades faltantes
**Archivos:** `/docs/uml/Scrum-Diagrama de clases.json` (modificado)
**Dependencias:** Fase 1
**Criterios de aceptación:**
- Rol es enum, no clase
- Epica existe como entidad independiente
- TaskStateTransition existe
- validarLimiteWIP() eliminado de Usuario
- Relaciones y cardinalidades corregidas

### Fase 3: Diagramas UML complementarios
**Objetivo:** Crear 5 diagramas faltantes
**Archivos:** `/docs/uml/secuencia-transicion-kanban.json`, `/docs/uml/secuencia-sprint-planning.json`, `/docs/uml/estado-tarea.json`, `/docs/uml/estado-sprint.json`, `/docs/uml/actividad-backlog-to-kanban.json`
**Dependencias:** Fase 2
**Criterios de aceptación:**
- Cada diagrama representa fielmente los flujos documentados en product.md
- Transiciones válidas documentadas explícitamente

### Fase 4: ADRs
**Objetivo:** Documentar decisiones arquitectónicas clave
**Archivos:** `/docs/adr/0001-use-fastapi.md`, `/docs/adr/0002-use-postgresql.md`, `/docs/adr/0003-use-cqrs.md`, `/docs/adr/0004-use-celery-redis.md`, `/docs/adr/0005-use-react-tanstack-query.md`, `/docs/adr/0006-wip-validation-strategy.md`
**Dependencias:** Fase 1
**Criterios de aceptación:**
- Cada ADR sigue formato MADR (contexto, decisión, consecuencias)
- Alternativas consideradas documentadas

### Fase 5: C4Model
**Objetivo:** Crear diagramas C4 de contexto, contenedores y componentes
**Archivos:** `/docs/c4/context-diagram.md`, `/docs/c4/container-diagram.md`, `/docs/c4/component-diagram.md`
**Dependencias:** Fase 1, Fase 4
**Criterios de aceptación:**
- Context: actores + sistema GESTKRUN + sistemas externos
- Container: backend, frontend, DB, Redis, Celery, Nginx
- Component: dentro de backend (API, Application, Domain, Infrastructure)

### Fase 6: Roadmap final y tareas
**Objetivo:** Generar tasks.md con todo desglosado
**Archivos:** `/openspec/changes/architectural-audit/tasks.md`
**Dependencias:** Todas las fases anteriores
**Criterios de aceptación:**
- Tareas < 30 min cada una
- Backend + Frontend separados cuando aplique
- Incluye tareas de verificación