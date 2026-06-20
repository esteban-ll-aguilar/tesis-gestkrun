# ADR 0007: Particionamiento de Tablas Temporales

**Fecha:** 2026-06-20\
**Estado:** Aceptado

## Contexto
Las tablas `task_state_transitions`, eventos de dominio y métricas agregadas crecen sin límite predecible. Sin particionamiento, las queries sobre rangos de tiempo se degradan, los índices crecen desmesuradamente y el mantenimiento (VACUUM, REINDEX) se vuelve costoso.

## Decisión
Se implementa **particionamiento por rango mensual** usando PostgreSQL declarative partitioning en:
- `task_state_transitions`: particionada por `timestamp` (mensual).
- `event_store`: particionada por `created_at` (mensual).
- `audit_log`: particionada por `created_at` (mensual).

Cada partición se crea automáticamente mediante un job de cron/Celery beat que crea la partición del próximo mes 7 días antes.

## Consecuencias
- Las queries deben incluir filtro por rango de fechas para aprovechar partition pruning.
- Las migraciones (Alembic) deben crear la tabla base con `PARTITION BY RANGE`.
- Las particiones viejas (> 12 meses) se pueden eliminar con `DROP TABLE` (sin pérdida de datos si se archivan).
- Los índices se crean por partición (índices locales).

## Alternativas Consideradas
- **Particionamiento por lista:** no aplica (no hay categorías discretas).
- **Tablas separadas manualmente (sharding):** alto costo operativo, no necesario en v1.
- **Sin particionamiento:** riesgo de degradación de performance a los 6-12 meses.
