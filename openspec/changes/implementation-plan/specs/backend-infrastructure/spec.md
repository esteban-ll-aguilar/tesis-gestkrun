# Spec: Backend Infrastructure

## Description
Estructura base del backend FastAPI con configuración, logging, manejo de errores, health endpoints y Docker Compose.

## Requirements

### RBI-01: Project structure
- `app/api/v1/` — routers por recurso
- `app/core/` — settings, logging, exceptions, security
- `app/domain/` — entities, value_objects, repositories, services, events, enums
- `app/application/` — use_cases, dto, mappers, interfaces
- `app/infrastructure/` — persistence, cache, auth, messaging, storage
- `app/workers/` — celery tasks
- `tests/` — unit and integration tests
- `alembic/` — migrations

### RBI-02: Configuration
- Pydantic Settings (BaseSettings) para configuración
- Variables de entorno con .env
- Settings class única accesible via DI

### RBI-03: Logging
- structlog con correlation_id por request (contextvars)
- Formato JSON estructurado
- Request ID en cada log

### RBI-04: Exception handling
- Manejador centralizado con formato Problem+JSON (RFC 7807)
- Excepciones de dominio mapeadas a HTTP status codes
- HTTPException personalizadas por módulo

### RBI-05: Health endpoints
- GET /health — ok/not ok
- GET /ready — DB connection check
- GET /metrics — Prometheus metrics

### RBI-06: Docker Compose
- PostgreSQL 16, Redis, PgBouncer, Nginx
- Makefile con comandos: up, down, logs, shell, test, lint, migrate