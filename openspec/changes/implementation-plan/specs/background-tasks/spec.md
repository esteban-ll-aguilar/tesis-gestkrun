# Spec: Background Tasks

## Description
Tareas asíncronas con Celery + Redis para refresco de materialized views, notificaciones y auditoría WIP.

## Requirements

### RBT-01: Celery setup
- Redis como broker y result backend
- Workers independientes
- Beat scheduler para tareas periódicas
- Retry con backoff exponencial

### RBT-02: Periodic tasks
- Refresh materialized views (cada 5 min)
- WIP audit report (diario)
- Cleanup de tokens expirados (diario)

### RBT-03: Event-driven tasks
- Notificaciones al equipo (nueva tarea, cambio de estado, bloqueo)
- Envío de emails (recovery password, notificaciones)

### RBT-04: Monitoring
- Flower para monitoreo de workers
- Métricas de Celery expuestas en /metrics
- Alertas de workers caídos