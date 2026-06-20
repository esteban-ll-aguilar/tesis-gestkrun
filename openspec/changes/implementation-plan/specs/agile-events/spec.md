# Spec: Agile Events

## Description
Registro y gestión de eventos ágiles: Daily Scrum, Sprint Review y Sprint Retrospective, vinculados al sprint activo.

## Requirements

### RAE-01: Daily Scrum
- Registro de fecha, notas, asistencia (miembros del equipo)
- Vinculado al sprint activo automáticamente
- Alertas si hay impedimentos nuevos reportados

### RAE-02: Sprint Review
- Documentación de feedback recibido
- Impedimentos identificados
- Cambios sugeridos al backlog

### RAE-03: Sprint Retrospective
- Acuerdos de mejora continua
- Acciones para próximo sprint
- Responsables asignados

### RAE-04: Validations
- Solo dentro de un sprint existente (invariante)
- Solo SM puede crear/editar eventos
- Eventos se listan en el detalle del sprint

### RAE-05: Frontend
- Formularios con campos dinámicos según tipo de evento
- Lista de eventos en timeline del sprint
- Asistencia pre-cargada (miembros del equipo del proyecto)