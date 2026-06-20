# Spec: Persistence Layer

## Description
Migraciones Alembic, repositorios SQLAlchemy, índices, particionamiento, materialized views, soft-delete y audit trail.

## Requirements

### RPL-01: Migrations
- Una migración inicial con todas las tablas
- Migration versionado semántico
- Rollback soportado

### RPL-02: Tables
users, roles (seed data), projects, project_assignments, modules, epicas, historias_usuario, sprints, sprint_eventos, tasks, task_state_transitions, messages, artifacts, artifact_versions

### RPL-03: Indexes
- users: unique(email) WHERE deleted_at IS NULL
- tasks: (assigned_to, estado) WHERE deleted_at IS NULL — WIP count
- tasks: (sprint_id, estado) WHERE deleted_at IS NULL — board
- task_state_transitions: (task_id, timestamp) — history
- messages: (proyecto_id, fecha_envio) — chat
- messages: (task_id, fecha_envio) — chat
- epicas: (project_id, orden) — backlog
- historias_usuario: (epica_id, orden) — backlog ordering

### RPL-04: Partitioning
- task_state_transitions: RANGE mensual en timestamp
- audit_log: RANGE mensual en created_at

### RPL-05: Soft delete
- Campo deleted_at en todas las entidades principales
- Índices parciales WHERE deleted_at IS NULL

### RPL-06: Audit trail
- Campos created_at, updated_at, created_by, updated_by en todas las tablas
- Triggers o aplicación para mantenerlos

### RPL-07: Materialized views
- mv_dashboard_metrics: project_id, sprint_id, total_tasks, tasks_by_status, lead_time_avg, cycle_time_avg, throughput, wip_violations_count
- mv_sprint_velocity: sprint_id, project_id, planned_points, completed_points, velocity_percentage