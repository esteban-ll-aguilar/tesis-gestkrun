# ADR 0003: CQRS para Lecturas Complejas

**Fecha:** 2026-06-20\
**Estado:** Aceptado

## Contexto
Los dashboards de métricas, reportes de velocidad y visualización de backlog requieren queries agregadas que difieren significativamente de los modelos de escritura (transiciones, creación de tareas). Mezclar ambas cargas en los mismos modelos ORM genera queries complejas, lentas y difícilmente optimizables.

## Decisión
Se implementa **CQRS ligero**:
- **Commands:** modelos de escritura (ORM SQLAlchemy con aggregates DDD).
- **Queries:** modelos de lectura separados (SQLAlchemy Core, queries planas, materialized views).
- **Eventual consistency** para dashboards: materialized views refrescadas cada 5 minutos vía Celery.
- No se usa event store separado; el event sourcing ligero de `task_state_transitions` sirve como fuente para cálculos.

## Consecuencias
- Los dashboards pueden tener hasta 5 minutos de desfase (aceptado para v1).
- Se duplica la definición de modelos (escritura + lectura) pero con responsabilidades claras.
- Las materialized views requieren índices específicos para queries de dashboard.
- Los refrescos concurrentes deben manejarse con `REFRESH MATERIALIZED VIEW CONCURRENTLY`.

## Alternativas Consideradas
- **CQRS completo con Event Store:** sobreingeniería para v1; no hay eventos externos ni múltiples consumidores.
- **Modelo único ORM:** las queries de dashboard serían lentas y difíciles de optimizar sin afectar writes.
