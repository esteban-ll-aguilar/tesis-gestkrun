# Spec: Kanban Board

## Description
Tablero Kanban con drag & drop, 6 columnas, validación WIP, gestión de impedimentos, y actualización en tiempo real de métricas.

## Requirements

### RKB-01: Board structure
- 6 columnas: Pendiente, En Proceso, Bloqueado, En Revisión, Terminado, Cancelado
- Tarjetas con: título, asignado, prioridad, fecha límite
- Conteo de tareas por columna

### RKB-02: Drag & Drop
- @dnd-kit para drag & drop
- Optimistic update inmediato (mover tarjeta visualmente)
- Rollback si backend rechaza
- Restricciones: solo columnas destino válidas según estado

### RKB-03: WIP validation
- Límite: máximo 3 tareas EN_PROCESO por usuario
- Frontend: deshabilitar drop si ya tiene 3
- Backend: validación síncrona con WIPValidationService
- Alerta amarilla al llegar a 2/3

### RKB-04: Task transition
- PATCH /tasks/{id}/transition con validación
- Transiciones válidas documentadas en diagrama de estado
- TaskStateTransition registrada automáticamente

### RKB-05: Impediments
- Botón "Bloquear" en tarjeta
- Formulario: causa, responsable de desbloqueo
- Filtro de tareas bloqueadas (Scrum Master)
- Notificación al equipo al bloquear

### RKB-06: Real-time updates
- Métricas de tablero actualizadas tras cada transición
- WebSocket para notificaciones de cambios simultáneos