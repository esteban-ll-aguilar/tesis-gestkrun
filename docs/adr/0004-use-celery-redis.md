# ADR 0004: Celery + Redis para Tareas Asíncronas

**Fecha:** 2026-06-20\
**Estado:** Aceptado

## Contexto
GESTKRUN requiere procesamiento asíncrono para: refresco de materialized views, cálculo de métricas agregadas, envío de notificaciones, y auditoría WIP. Las alternativas incluyen Celery + Redis, Huey, o task graph nativo de FastAPI (BackgroundTasks).

## Decisión
Se adopta **Celery + Redis**:
- **Redis** como message broker y result backend (ya está en el stack para caché/pub-sub).
- **Celery** para tareas programadas (beat) y asíncronas.
- Workers independientes para escalar el procesamiento de métricas.
- Retry automático con backoff exponencial en tareas críticas.

## Consecuencias
- Redis se usa para 3 propósitos: caché, pub/sub (WebSockets), y broker Celery. Requiere monitoreo de memoria.
- Las tareas deben ser idempotentes para soportar retries.
- Flower se usa para monitoreo de workers.

## Alternativas Consideradas
- **FastAPI BackgroundTasks:** no soporta tareas programadas, ni retry, ni workers separados.
- **Huey:** más liviano que Celery pero con menos soporte para tareas programadas complejas.
