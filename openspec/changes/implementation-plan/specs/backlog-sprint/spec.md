# Spec: Backlog & Sprint Management

## Description
Gestión del Product Backlog (épicas, historias de usuario, priorización) y planificación/gestión de Sprints.

## Requirements

### RBS-01: Epics
- CRUD de épicas por proyecto
- Atributos: título, descripción, prioridad, estado, orden
- Priorización drag & drop (reordenamiento)

### RBS-02: User Stories
- CRUD de historias de usuario dentro de épica
- Atributos: título, descripción, criterios de aceptación, prioridad, estimación (story points 1-21 Fibonacci)
- Asociación a módulo del proyecto

### RBS-03: Backlog prioritization
- Drag & drop para reordenar épicas e historias
- Estado "priorizado" / "no priorizado"
- Sistema bloquea Sprint Planning si backlog no priorizado
- Cálculo automático de estimación acumulada

### RBS-04: Sprint Planning
- Definir duración y objetivo
- Seleccionar historias del backlog para el sprint
- Backlog debe estar priorizado (validación)
- Confirmación genera: sprint en PLANIFICADO + tareas en Pendiente

### RBS-05: Sprint lifecycle
- Estados: PLANIFICADO → EN_EJECUCION → FINALIZADO | CANCELADO
- Iniciar sprint: transición a EN_EJECUCION
- Cerrar sprint: bloquea nuevas transiciones
- Solo SM puede iniciar/cerrar sprints

### RBS-06: Sprint events
- Registro de Daily Scrum, Sprint Review, Sprint Retrospective
- Campos: notas, asistencia, fecha, duración
- Vinculados al sprint activo automáticamente