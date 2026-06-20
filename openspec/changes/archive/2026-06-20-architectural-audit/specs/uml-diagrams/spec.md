# Spec: UML Diagrams

## Description
Diagramas UML completos para GESTKRUN: clases, secuencia (2), estado (2) y actividad (1).

## Requirements

### RU-01: Diagrama de clases (corregido)
- Basado en el JSON existente en `docs/uml/Scrum-Diagrama de clases.json`
- Aplicar correcciones del design.md:
  - Rol como «enumeration»
  - Agregar Epica
  - Agregar TaskStateTransition
  - Eliminar validarLimiteWIP() de Usuario
  - Corregir TipoMensaje (solo PROYECTO, TAREA)
  - Agregar EstadoModulo como enumeration
  - Sprint → Proyecto (no → Módulo)
  - HistoriaUsuario → Módulo

### RU-02: Diagrama de secuencia — Transición Kanban
- Actor: Developer
- Flujo: Frontend (optimistic update) → Backend (PATCH /tasks/{id}/transition)
- Validación WIP en Domain Service → respuesta success/error
- Rollback en frontend si error
- Emisión de evento TaskMoved / WIPViolated
- Actualización de métricas en dashboard

### RU-03: Diagrama de secuencia — Sprint Planning
- Actor: Scrum Master
- Flujo: Frontend → Backlog validación (priorizado) → creación Sprint
- Derivación de tareas desde historias seleccionadas
- Notificación al equipo

### RU-04: Diagrama de estado — Tarea
- Estados: PENDIENTE, EN_PROCESO, BLOQUEADO, EN_REVISION, TERMINADO, CANCELADO
- Transiciones válidas:
  - PENDIENTE → EN_PROCESO
  - EN_PROCESO → BLOQUEADO, EN_REVISION
  - BLOQUEADO → EN_PROCESO
  - EN_REVISION → EN_PROCESO, TERMINADO
  - Cualquier estado → CANCELADO

### RU-05: Diagrama de estado — Sprint
- Estados: PLANIFICADO, EN_EJECUCION, FINALIZADO, CANCELADO
- Transiciones: PLANIFICADO → EN_EJECUCION → FINALIZADO
- Cualquiera → CANCELADO (solo si no está FINALIZADO)

### RU-06: Diagrama de actividad — Backlog a Kanban
- Swimlanes: PO, SM, Sistema
- Flujo: PO crea épica → PO añade historias → PO prioriza → SM planifica sprint → SM selecciona historias → Sistema deriva tareas → Tareas aparecen en Kanban
- Puntos de decisión: backlog priorizado? sprint activo?

## Invariants
- Los diagramas deben ser consistentes con product.md, architecture.md y el modelo de dominio
- Las transiciones inválidas deben estar explícitamente excluidas