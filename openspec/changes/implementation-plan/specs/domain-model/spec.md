# Spec: Domain Model

## Description
Implementación del modelo de dominio completo con entidades, value objects, enums, eventos de dominio, servicios de dominio e interfaces de repositorio.

## Requirements

### RDM-01: Entities
User, Project, Module, Epica, HistoriaUsuario, Sprint, SprintEvento, Task, TaskStateTransition, Message, Artifact, ArtifactVersion

### RDM-02: Value Objects
Email (validación formato), PasswordHash (Argon2id), EstimacionEsfuerzo (1-21 Fibonacci), UserId, ProjectId, TaskId, SprintId, EpicaId, HistoriaUsuarioId, WIPCount (0-3)

### RDM-03: Enums
Rol (ADMIN, PRODUCT_OWNER, SCRUM_MASTER, DEVELOPER), EstadoTarea, EstadoSprint, EstadoProyecto, EstadoModulo, Prioridad, TipoArtefacto, TipoMensaje, TipoEventoScrum

### RDM-04: Domain Events (13)
UserRegistered, UserRoleChanged, UserDeactivated, ProjectCreated, ModuleAdded, TeamAssigned, EpicaCreated, BacklogPrioritized, SprintPlanned, SprintClosed, TaskMoved, WIPViolated, TaskBlocked, MessageSent, ArtifactUploaded

### RDM-05: Repository interfaces
IUserRepository, IProjectRepository, IModuleRepository, IEpicaRepository, IHistoriaUsuarioRepository, ISprintRepository, ITaskRepository, IMessageRepository, IArtifactRepository

### RDM-06: Domain Services
WIPValidationService (contar tareas EN_PROCESO por usuario), KanbanFlowService (gestión de estado de tareas), MetricsCalculationService (lead time, cycle time)

### RDM-07: Invariants de dominio
- WIP ≤ 3 por Developer
- Tarea no avanza sin sprint activo
- Tarea deriva de Historia de Usuario
- Solo PO prioriza backlog
- Solo SM cierra sprints
- Admin no crea proyectos
- Eventos ágiles solo dentro de sprint existente