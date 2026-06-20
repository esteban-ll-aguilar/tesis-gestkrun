# ADR 0005: React + TanStack Query + Zustand

**Fecha:** 2026-06-20\
**Estado:** Aceptado

## Contexto
El frontend de GESTKRUN debe manejar estado del servidor intensivo (caché de queries, optimistic updates en drag & drop), estado global mínimo (usuario autenticado, tema) y actualizaciones en tiempo real vía WebSockets. Se evaluaron varias combinaciones de bibliotecas de estado.

## Decisión
- **React 18+** con TypeScript 5.3 (strict mode) como framework UI.
- **TanStack Query v5** para caché de datos del servidor, sincronización, optimistic updates y rollback.
- **Zustand** para estado global mínimo (auth, UI preferences).
- **Vite** como build tool (HMR rápido, tree-shaking).
- **Tailwind CSS + shadcn/ui** para diseño atómico y componentes accesibles.

## Consecuencias
- Los optimistic updates requieren implementar lógica de rollback en TanStack Query.
- Las mutaciones deben invalidar las queries relevantes automáticamente.
- El estado de WebSockets se maneja con TanStack Query (invalidation en tiempo real).
- Zustand se mantiene pequeño (< 3 stores) para evitar complejidad.

## Alternativas Consideradas
- **Redux Toolkit + RTK Query:** más boilerplate, mayor bundle, curva de aprendizaje más alta.
- **Redux + Axios:** sin caché inteligente ni optimistic updates nativos.
- **Recoil / Jotai:** experimentales, menor ecosistema.
