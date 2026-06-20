# Spec: Domain Model

## Description
Modelo de dominio completo de GESTKRUN con entidades, value objects, aggregates, enums y eventos de dominio, alineado con DDD y Clean Architecture.

## Requirements

### RD-01: Entidades del dominio
- User (IAM): id, nombre, email, contraseña, rol, fechaRegistro
- Project (Project Management): id, nombre, descripcion, estado, fechaInicio
- Module (Project Management): id, projectId, nombre, descripcion, estado
- Epica (Backlog Management): id, projectId, titulo, descripcion, prioridad, estado
- HistoriaUsuario (Backlog Management): id, epicaId, moduloId, titulo, descripcion, criteriosAceptacion, prioridad, estimacion
- Sprint (Sprint Management): id, projectId, nombre, objetivo, duracion, fechaInicio, fechaFin, estado
- SprintEvento (Sprint Management): id, sprintId, tipo, fecha, notas, duracion
- Task (Kanban Flow): id, historiaUsuarioId, sprintId, assignedTo, titulo, descripcion, estado, fechaCreacion, fechaLimite
- TaskStateTransition (Kanban Flow): id, taskId, fromEstado, toEstado, timestamp, userId, reason
- Message (Communication): id, proyectoId/taskId, senderId, contenido, fechaEnvio, tipo
- Artifact (Artifact Management): id, taskId, nombre, tipo, version, contenidoURL
- ArtifactVersion (Artifact Management): id, artifactId, version, contenidoURL, uploadedBy, createdAt

### RD-02: Value Objects
- Email: validación de formato, único en sistema
- PasswordHash: hash Argon2id, mínimo 8 caracteres
- EstimacionEsfuerzo: entero 1-21 (Fibonacci), opcional
- UserId, ProjectId, TaskId, SprintId, EpicaId, HistoriaUsuarioId: UUID tipados
- WIPCount: entero 0-3, inmutable

### RD-03: Aggregates
- User aggregate: User entity (root), Email, PasswordHash (VOs)
- Project aggregate: Project (root), Module (entity), TeamAssignment (VO)
- Epica aggregate: Epica (root), HistoriaUsuario (entity)
- Sprint aggregate: Sprint (root), SprintEvento (entity)
- Task aggregate: Task (root), TaskStateTransition (entity)
- Message aggregate: Message (root)
- Artifact aggregate: Artifact (root), ArtifactVersion (entity)

### RD-04: Enums
- Rol: ADMIN, PRODUCT_OWNER, SCRUM_MASTER, DEVELOPER
- EstadoTarea: PENDIENTE, EN_PROCESO, BLOQUEADO, EN_REVISION, TERMINADO, CANCELADO
- EstadoSprint: PLANIFICADO, EN_EJECUCION, FINALIZADO, CANCELADO
- EstadoProyecto: ACTIVO, INACTIVO, FINALIZADO, CANCELADO
- EstadoModulo: ACTIVO, INACTIVO
- Prioridad: BAJA, MEDIA, ALTA, CRITICA
- TipoArtefacto: REQUISITO, DIAGRAMA, ACTA, DOCUMENTO, CODIGO
- TipoMensaje: PROYECTO, TAREA
- TipoEventoScrum: SPRINT_PLANNING, DAILY_SCRUM, SPRINT_REVIEW, SPRINT_RETROSPECTIVE

### RD-05: Eventos de dominio
- UserRegistered, UserRoleChanged, ProjectCreated, TeamAssigned
- EpicaCreated, BacklogPrioritized, SprintPlanned, SprintClosed
- TaskMoved, WIPViolated, TaskBlocked, MessageSent, ArtifactUploaded
- Cada evento debe incluir timestamp y payload mínimo

### RD-06: Repository interfaces
- IUserRepository, IProjectRepository, ISprintRepository
- ITaskRepository, IEpicaRepository, IMessageRepository, IArtifactRepository
- Métodos: getById, save, delete, find (por criterios de dominio)

## Invariants
- Un Developer no puede tener > 3 tareas EN_PROCESO (WIP)
- Una tarea no puede avanzar sin sprint activo
- Una tarea debe derivar de una Historia de Usuario
- Solo PO prioriza backlog, solo SM cierra sprints
- Admin no crea proyectos ni tareas
- Eventos ágiles solo dentro de un sprint existente