## 1. Separación de documentación base

- [x] 1.1 Revisar y modificar `openspec/product.md` extrayendo secciones 1-4 de docs/architecture.md (visión, usuarios, funcionalidades, flujos, fuera de alcance)
- [x] 1.2 Revisar y modificar  `openspec/config.yaml` con invariants del dominio (8 reglas) y SLOs (7 métricas) desde openspec/config.yaml
- [x] 1.3 Reescribir `/docs/architecture.md` dejando solo stack, capas, bounded contexts, persistencia y NFRs
- [x] 1.4 Agregar referencias cruzadas (xref) entre product.md, config.yaml y docs/architecture.md
- [x] 1.5 Verificar que no haya pérdida de información vs el architecture.md original

## 2. Corrección del modelo de dominio (UML)

- [x] 2.1 Convertir clase `Rol` a `«enumeration» Rol` con valores ADMIN, PRODUCT_OWNER, SCRUM_MASTER, DEVELOPER
- [x] 2.2 Agregar entidad `Epica` con atributos: id, projectId, titulo, descripcion, prioridad, estado
- [x] 2.3 Agregar entidad `TaskStateTransition` con atributos: id, taskId, fromEstado, toEstado, timestamp, userId, reason
- [x] 2.4 Eliminar método `validarLimiteWIP()` de Usuario
- [x] 2.5 Reducir `TipoMensaje` a solo PROYECTO y TAREA (eliminar MODULO y PRIVADO)
- [x] 2.6 Agregar `«enumeration» EstadoModulo` con valores ACTIVO, INACTIVO
- [x] 2.7 Corregir relación Sprint → Proyecto (eliminar Sprint → Módulo)
- [x] 2.8 Agregar relación HistoriaUsuario → Modulo
- [x] 2.9 Corregir cardinalidades según design.md
- [x] 2.10 Regenerar JSON de Draw.io con todas las correcciones

## 3. Diagramas UML complementarios

- [x] 3.1 Crear diagrama de secuencia — Transición Kanban (movimiento de tarea con validación WIP)
- [x] 3.2 Crear diagrama de secuencia — Sprint Planning (backlog → sprint → tareas)
- [x] 3.3 Crear diagrama de estado — Tarea (6 estados, transiciones válidas)
- [x] 3.4 Crear diagrama de estado — Sprint (4 estados, transiciones)
- [x] 3.5 Crear diagrama de actividad — Backlog a Kanban (swimlanes PO, SM, Sistema)

## 4. ADRs

- [x] 4.1 ADR 0001: FastAPI como framework backend
- [x] 4.2 ADR 0002: PostgreSQL como base de datos
- [x] 4.3 ADR 0003: CQRS para lecturas complejas
- [x] 4.4 ADR 0004: Celery + Redis para tareas async
- [x] 4.5 ADR 0005: React + TanStack Query + Zustand
- [x] 4.6 ADR 0006: Estrategia de validación WIP
- [x] 4.7 ADR 0007: Particionamiento de tablas temporales

## 5. C4Model

- [x] 5.1 Crear diagrama de Context (nivel 1): personas + GESTKRUN + sistemas externos
- [x] 5.2 Crear diagrama de Container (nivel 2): SPA, API, DB, Redis, Celery, Nginx
- [x] 5.3 Crear diagrama de Component (nivel 3): capas internas del backend FastAPI

## 6. Actualización de openspec/config.yaml

- [x] 6.1 Actualizar referencias en openspec/config.yaml para apuntar a product.md y config.yaml raíz
- [x] 6.2 Verificar que los invariants en openspec/config.yaml sigan siendo consistentes con config.yaml raíz

## 7. Verificación final de consistencia

- [x] 7.1 Verificar que todo lo definido en product.md tenga soporte en docs/architecture.md
- [x] 7.2 Verificar que todo lo definido en docs/architecture.md tenga soporte en UML
- [x] 7.3 Verificar que todo el UML tenga soporte en el modelo de dominio
- [x] 7.4 Verificar que no existan contradicciones entre product.md, config.yaml, architecture.md, UML y ADRs
- [x] 7.5 Verificar que no existan entidades sin uso en UML
- [x] 7.6 Verificar que todos los diagramas (C4, UML) sean consistentes entre sí