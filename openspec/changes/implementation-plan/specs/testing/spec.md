# Spec: Testing

## Description
Estrategia de testing completa: unitarios, integración y E2E con coberturas mínimas definidas.

## Requirements

### RTE-01: Backend unit tests
- Dominio: entidades, VOs, servicios de dominio, eventos
- Sin dependencias externas (mocks)
- Cobertura ≥ 90% del dominio
- pytest + pytest-asyncio

### RTE-02: Backend integration tests
- API endpoints con httpx AsyncClient
- Base de datos real con TestContainers (PostgreSQL en contenedor)
- Repositorios SQLAlchemy
- Cobertura ≥ 85% total backend

### RTE-03: Frontend unit tests
- Componentes con React Testing Library
- Hooks con renderHook
- Stores con Zustand test utilities
- Cobertura ≥ 75%

### RTE-04: Frontend integration tests
- MSW (Mock Service Worker) para API mock
- Flujos de página completos
- TanStack Query testing utilities

### RTE-05: E2E tests
- Playwright
- Flujos críticos: login, Kanban drag & drop, WIP validation, sprint planning
- 3 navegadores: Chrome, Firefox, Edge

### RTE-06: Test configuration
- pytest config en pyproject.toml
- Vitest config en vite.config.ts
- Playwright config
- Coverage reports (HTML + XML para CI)
- Test fixtures y factories