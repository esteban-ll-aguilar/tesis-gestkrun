# Spec: ADR Documentation

## Description
Architecture Decision Records iniciales para decisiones técnicas clave de GESTKRUN.

## Requirements

### RADR-01: ADR 0001 — FastAPI como framework backend
- Contexto: necesidad de framework ASGI moderno con validación nativa
- Decisión: FastAPI sobre Django REST Framework o Flask
- Consecuencias: tipado fuerte con Pydantic, async nativo, OpenAPI automático

### RADR-02: ADR 0002 — PostgreSQL como base de datos
- Contexto: necesidad de JSONB, índices parciales, particionamiento, concurrencia
- Decisión: PostgreSQL 16+ sobre MySQL o MongoDB
- Consecuencias: extensibilidad con pg_trgm, uuid-ossp, btree_gist

### RADR-03: ADR 0003 — CQRS para lecturas complejas
- Contexto: dashboards y reportes requieren queries optimizadas diferentes a writes
- Decisión: CQRS ligero (sin event store separado, solo materialized views)
- Consecuencias: modelos de lectura separados, eventual consistency en dashboards

### RADR-04: ADR 0004 — Celery + Redis para tareas async
- Contexto: métricas, notificaciones, refresco de materialized views
- Decisión: Celery con Redis como broker/result backend
- Consecuencias: workers independientes, retry con backoff, monitoreo con Flower

### RADR-05: ADR 0005 — React + TanStack Query + Zustand
- Contexto: SPA con estado servidor intensivo y drag & drop Kanban
- Decisión: React 18 + TanStack Query (caché servidor) + Zustand (estado global mínimo)
- Consecuencias: optimistic updates, sincronización automática, estado UI ligero

### RADR-06: ADR 0006 — Estrategia de validación WIP
- Contexto: invariante crítica WIP ≤ 3 tareas EN_PROCESO por Developer
- Decisión: validación en backend (domain service) + frontend optimistic + rollback
- Consecuencias: consistencia fuerte, UX con feedback inmediato, audit log de violaciones

### RADR-07: ADR 0007 — Particionamiento de tablas temporales
- Contexto: task_state_transitions y eventos crecen rápido
- Decisión: particionamiento por rango mensual en PostgreSQL declarative partitioning
- Consecuencias: DROP de particiones viejas, queries por rango de fechas optimizadas

## Invariants
- Cada ADR debe seguir formato MADR (Markdown Any Decision Records)
- Incluir secciones: Context, Decision, Consequences, Alternatives Considered