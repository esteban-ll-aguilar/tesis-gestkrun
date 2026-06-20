# ADR 0002: PostgreSQL como Base de Datos

**Fecha:** 2026-06-20\
**Estado:** Aceptado

## Contexto
GESTKRUN requiere una base de datos relacional que soporte JSONB para metadatos flexibles, índices parciales para soft-delete, particionamiento para tablas de alta cardinalidad, y extensiones para búsqueda fuzzy y rangos temporales. Se evaluaron PostgreSQL 16, MySQL 8 y MongoDB 7.

## Decisión
Se adopta **PostgreSQL 16+** por:
- Soporte nativo de JSONB con índices GIN (datos semiestructurados de artefactos y métricas).
- Índices parciales para soft-delete (`WHERE deleted_at IS NULL`).
- Declarative partitioning por rango para tablas temporales.
- Extensiones clave: pg_trgm (búsqueda fuzzy), uuid-ossp (UUIDs), btree_gist (rangos temporales).
- Concurrencia superior (MVCC, VACUUM, replication slots).
- Madurez y rendimiento para cargas de trabajo OLTP con reportes agregados.

## Consecuencias
- Se requiere PgBouncer para connection pooling (transacciones cortas).
- Las migraciones deben considerar particionamiento (Alembic con comandos DDL nativos).
- Backup y restore requieren estrategia para tablas particionadas.

## Alternativas Consideradas
- **MySQL 8:** índices parciales limitados, particionamiento menos flexible, sin JSONB (solo JSON).
- **MongoDB 7:** documental, no relacional; forzaría modelado desnormalizado para relaciones del dominio.
