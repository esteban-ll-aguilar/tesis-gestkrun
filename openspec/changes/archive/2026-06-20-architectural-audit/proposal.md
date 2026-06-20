## Why

La documentación del proyecto GESTKRUN existe como un único archivo híbrido (`docs/architecture.md`) que mezcla spec de producto, arquitectura, y requisitos no funcionales. No hay `product.md` independiente, `config.yaml` en la raíz, diagramas UML completos, ADRs, ni C4Model. Esta falta de separación y completitud introduce riesgos de inconsistencia durante la implementación: reglas de dominio duplicadas o ausentes, entidades UML sin mapeo arquitectónico, y flujos críticos (WIP, transiciones Kanban) sin diagramas de soporte. Esta auditoría ordena, separa, completa y alinea toda la documentación para que sea una fuente de verdad única, consistente y accionable.

## What Changes

- Separar conceptualmente `docs/architecture.md` en: `product.md` (spec), `docs/architecture.md` (arquitectura pura), y `config.yaml` (raíz, invariants + SLOs).
- Auditar y corregir el diagrama de clases UML existente (`docs/uml/Scrum-Diagrama de clases.json`).
- Crear diagramas UML faltantes: secuencia (transición WIP, sprint planning), estado (tarea, sprint), actividad (flujo de movimiento Kanban).
- Crear ADRs iniciales en `docs/adr/` (decisiones arquitectónicas clave ya tomadas).
- Crear C4Model base en `docs/c4/` (Context, Container, Component diagrams).
- Identificar elementos faltantes del dominio (entidades, enums, value objects, eventos, repositorios, casos de uso).
- Mejorar la arquitectura con Bounded Contexts formales y separación de capas Clean Architecture + DDD.
- Generar roadmap de implementación por fases.

## Capabilities

### New Capabilities
- `architectural-audit`: Revisión completa, corrección y normalización de toda la documentación del proyecto
- `domain-model`: Modelo de dominio completo con entidades, value objects, aggregates, enums y eventos
- `uml-diagrams`: Diagramas de clases, secuencia, estado y actividad
- `c4-model`: Diagramas C4 de contexto, contenedores y componentes
- `adr-documentation`: Architecture Decision Records para decisiones clave
- `implementation-roadmap`: Roadmap técnico detallado por fases

### Modified Capabilities
Ninguna (no existen specs previas en `openspec/specs/`)

## Impact

- `docs/architecture.md`: se reestructura — contenido de producto migra a `product.md`, invariants migran a `config.yaml`.
- `openspec/config.yaml`: permanece como referencia del proceso SDD; invariants se copian a `config.yaml` raíz.
- `docs/uml/`: se crean nuevos diagramas; el existente se audita y corrige.
- `docs/adr/` y `docs/c4/`: se crean desde cero.
- No hay impacto en código de backend/frontend porque esta fase es puramente documental.

## Non-goals

- No se implementa ningún código de backend o frontend.
- No se modifican archivos fuente de las aplicaciones (`tesis-gestkrun-api/`, `tesis-gestkrun-web/`).
- No se configuran herramientas de CI/CD ni infraestructura.
- No se generan migraciones de base de datos.
- No se realizan cambios en `openspec/config.yaml` ni en el proceso SDD definido.