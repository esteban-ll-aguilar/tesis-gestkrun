# Spec: Dashboard & Metrics

## Description
Dashboard con métricas de rendimiento del equipo: velocidad del sprint, lead time, cycle time, throughput y conteo de tareas por estado.

## Requirements

### RDM-01: Metrics calculated
- Velocidad del equipo por sprint (story points completados)
- Lead time: tiempo desde creación hasta terminado
- Cycle time: tiempo desde primer EN_PROCESO hasta TERMINADO
- Throughput: tareas completadas por unidad de tiempo
- Conteo de tareas por estado del Kanban

### RDM-02: Materialized views
- mv_dashboard_metrics: refresco cada 5 min vía Celery
- mv_sprint_velocity: refresco cada 5 min vía Celery
- Queries de lectura desde MV para latencia < 3s

### RDM-03: Endpoints
- GET /dashboard/{projectId}/metrics — métricas generales
- GET /dashboard/{projectId}/velocity — velocidad por sprint

### RDM-04: Frontend
- Dashboard con cards de métricas
- Gráficos (Recharts/Tremor): velocidad (bar), lead/cycle time (line), throughput (area)
- Conteo de tareas por estado (donut/pie)
- Alerta de tareas bloqueadas activas
- Carga < 2s desde MV