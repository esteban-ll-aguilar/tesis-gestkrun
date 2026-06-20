# GESTKRUN — Product Specification

> **Infraestructura de software para la gestión de proyectos bajo el marco Scrumban:**  
> *en la consistencia del flujo de trabajo y métricas de desempeño del proceso.*

**Autor:** Esteban León Aguilar  
**Institución:** Universidad Nacional de Loja — Facultad de la Energía, las Industrias y los Recursos Naturales no Renovables  
**Versión:** 1.0.0  
**Fecha:** 2026-06-18  
**Estado:** Aprobado para desarrollo

---

## Sección 1 — Visión del Producto

**GESTKRUN** es una plataforma web que unifica la gestión de proyectos de desarrollo de software bajo el marco híbrido **Scrumban**, combinando la planificación iterativa de Scrum con el flujo visual y los límites de trabajo en progreso (WIP) de Kanban. Está diseñada para equipos de desarrollo de software que sufren fragmentación de herramientas, pérdida de trazabilidad entre artefactos ágiles y falta de visibilidad sobre cuellos de botella.

Resuelve el problema de la **desconexión técnica entre backlog, sprint y tablero Kanban** que genera inconsistencias en las métricas de proceso (lead time, cycle time, velocidad) y permite la violación no detectada de restricciones WIP, degradando la calidad de las decisiones de gestión conforme a SWEBOK v4 e ISO/IEC 25010.

---

## Sección 2 — Usuarios y Casos de Uso

| Usuario | Descripción | Casos de uso |
|---|---|---|
| **Administrador** | Gestor global de la plataforma encargado de la gobernanza de usuarios y roles. | 1. Crear y gestionar cuentas de usuario globales. 2. Asignar roles globales (PO, SM, Developer). 3. Activar/desactivar cuentas. 4. Visualizar proyectos activos a nivel global. |
| **Product Owner (PO)** | Responsable de maximizar el valor del producto y gestionar el backlog priorizado. | 1. Crear proyectos y estructurarlos en módulos. 2. Crear y priorizar épicas e historias de usuario. 3. Asignar Scrum Master y Developers al proyecto. 4. Visualizar dashboard con métricas de velocidad e impedimentos. |
| **Scrum Master (SM)** | Facilitador del proceso ágil y garante del flujo de trabajo Scrumban. | 1. Configurar Sprints (duración, objetivo, selección de tareas). 2. Facilitar eventos ágiles (Daily, Review, Retro). 3. Gestionar impedimentos y tareas bloqueadas. 4. Cerrar Sprints al finalizar la iteración. |
| **Developer** | Ejecutor técnico del desarrollo del producto, autogestionado en el flujo. | 1. Visualizar y mover tarjetas en el tablero Kanban respetando WIP. 2. Registrar progreso y comentarios en tareas. 3. Adjuntar artefactos (documentos, diagramas, actas). 4. Comunicarse vía mensajería asíncrona por proyecto/tarea. |

---

## Sección 3 — Funcionalidades

### Área 1: Autenticación y Gestión de Usuarios
- El usuario puede autenticarse con email y contraseña vía JWT (access + refresh token).
- El usuario puede recuperar su contraseña mediante flujo seguro por email.
- El Administrador puede listar, buscar, filtrar y activar/desactivar cuentas de usuario.
- El Administrador puede asignar y modificar roles globales (PO, SM, Developer).
- El sistema valida sesiones activas y revoca tokens en logout o cambio de rol.

### Área 2: Gestión de Proyectos y Módulos
- El Product Owner puede crear proyectos con nombre, descripción y fecha de inicio.
- El Product Owner puede estructurar el proyecto en módulos lógicos.
- El Product Owner puede asignar Scrum Master y Developers al proyecto.
- El Product Owner puede gestionar el estado activo/inactivo del proyecto.
- El sistema restringe que solo usuarios con rol global PO puedan crear proyectos.

### Área 3: Product Backlog
- El Product Owner puede crear, editar y eliminar épicas e historias de usuario.
- El Product Owner puede priorizar el backlog mediante reordenamiento drag & drop.
- El Product Owner puede asociar historias a módulos específicos del proyecto.
- El sistema bloquea el backlog para Sprint Planning si no está priorizado.
- El sistema calcula automáticamente la estimación de esfuerzo acumulado.

### Área 4: Planificación y Gestión de Sprints
- El Scrum Master puede crear Sprints con duración definida (ej. 2 semanas) y objetivo.
- El Scrum Master puede seleccionar tareas del backlog listas para el sprint activo.
- El Scrum Master puede definir el objetivo del sprint.
- El Scrum Master puede cerrar el sprint, bloqueando nuevas transiciones de tareas.
- El sistema valida que solo tareas de historias priorizadas puedan entrar al sprint.

### Área 5: Tablero Kanban Scrumban
- El usuario (Developer, SM, PO) puede visualizar tareas en columnas: Pendiente, En Proceso, Bloqueado, En Revisión, Terminado, Cancelado.
- El usuario puede mover tarjetas entre columnas vía drag & drop.
- El sistema valida automáticamente el límite WIP de máximo 3 tareas en "En Proceso" por usuario.
- El sistema bloquea inmediatamente la acción en frontend y backend si se viola WIP.
- El sistema registra timestamp de cada transición para cálculo de cycle time.
- El sistema actualiza métricas en tiempo real tras cada movimiento de tarjeta.

### Área 6: Gestión de Impedimentos
- El Scrum Master puede filtrar rápidamente tareas en estado "Bloqueado".
- El Scrum Master puede registrar la causa del bloqueo en la tarea.
- El Scrum Master puede asignar responsable de desbloqueo.
- El sistema notifica al equipo cuando una tarea cambia a estado Bloqueado.

### Área 7: Eventos Ágiles
- El Scrum Master puede registrar notas y asistencia del Daily Scrum.
- El Scrum Master puede documentar feedback e impedimentos en Sprint Review.
- El Scrum Master puede registrar acuerdos de mejora en Sprint Retrospective.
- El sistema vincula automáticamente los eventos al Sprint activo.

### Área 8: Gestión de Artefactos
- El Developer puede cargar documentos, diagramas o actas directamente en la tarjeta de tarea.
- El sistema mantiene versionado histórico de cada artefacto.
- El sistema permite visualizar versiones previas y descargar la más reciente.
- El sistema categoriza artefactos por tipo: Requisito, Diagrama, Acta, Documento, Código.

### Área 9: Mensajería Asíncrona
- El usuario puede enviar y recibir mensajes de texto a nivel de proyecto.
- El usuario puede enviar mensajes de texto a nivel de tarea específica.
- El sistema mantiene historial de conversación con paginación cursor-based.
- El sistema notifica en tiempo real nuevos mensajes vía WebSockets.

### Área 10: Dashboard y Métricas
- El Product Owner y Scrum Master pueden visualizar velocidad del equipo por sprint.
- El sistema muestra conteo de tareas en cada estado del tablero Kanban.
- El sistema alerta sobre tareas bloqueadas activas.
- El sistema calcula y visualiza lead time, cycle time y throughput.
- El sistema genera materialized views para reportes de rendimiento.

### Estados del sistema
- El sistema muestra estado de carga (skeleton) mientras carga el tablero Kanban.
- El sistema muestra alerta visual y sonora al alcanzar el límite WIP (2/3 tareas).
- El sistema muestra mensaje de error claro si se viola una regla de dominio (WIP, trazabilidad).
- El sistema muestra estado vacío cuando no hay Sprints activos.
- El sistema muestra indicador de sincronización cuando hay operaciones pendientes (optimistic UI).

### Fuera del alcance (v1)
- No incluye integración con repositorios de código externos (GitHub, GitLab, Bitbucket) vía webhooks.
- No incluye videollamadas ni envío de archivos multimedia en el chat (mensajería puramente textual).
- No incluye reportes avanzados de recursos humanos ni seguimiento de horas laborables.
- No incluye notificaciones push móvil (solo web notifications).
- No incluye exportación a PDF/Excel de reportes (solo visualización web).
- No incluye integración con calendarios externos (Google Calendar, Outlook).

---

## Sección 4 — Flujos de Usuario

### Flujo principal — Movimiento de tarea en Kanban (Developer)
1. El Developer abre el proyecto → visualiza el tablero Kanban del sprint activo.
2. Identifica una tarea asignada en columna "Pendiente".
3. Arrastra la tarjeta hacia "En Proceso".
4. El frontend ejecuta optimistic update (mueve la tarjeta visualmente).
5. El backend recibe la petición PATCH /tasks/{id}/transition.
6. El backend valida: ¿el Developer tiene < 3 tareas en EN_PROCESO? ¿la tarea pertenece al sprint activo?
7. Si ambas validaciones pasan: actualiza estado, registra timestamp, recalcula métricas, emite evento.
8. El frontend confirma el movimiento y actualiza métricas en dashboard.
9. Si WIP se alcanza (3/3), el sistema muestra banner de alerta amarillo al Developer.

### Flujo de error — Violación de límite WIP
1. El Developer intenta mover una 4ta tarea a "En Proceso".
2. El backend detecta violación de invariante de dominio (WIP > 3).
3. El backend responde 422 Unprocessable Entity con detalle: "Límite WIP alcanzado. Completa una tarea en progreso antes de iniciar otra."
4. El frontend realiza rollback del optimistic update (la tarjeta vuelve a "Pendiente").
5. El frontend muestra toast de error persistente con la causa y sugerencia de acción.
6. El sistema registra el intento de violación en audit log para métricas de proceso.

### Flujo principal — Sprint Planning (Scrum Master)
1. El Scrum Master accede al módulo "Planificar Sprint".
2. El sistema muestra el Product Backlog priorizado filtrado por historias "listas para desarrollo".
3. El Scrum Master define duración del sprint (ej. 14 días) y objetivo.
4. El Scrum Master selecciona historias del backlog arrastrándolas al sprint.
5. El sistema valida que el backlog esté priorizado; si no, bloquea la acción.
6. El Scrum Master confirma la creación del sprint.
7. El sistema genera el sprint, crea las tareas derivadas en el tablero Kanban (columna Pendiente) y notifica al equipo.

### Flujo de error — Backlog no priorizado
1. El Scrum Master intenta crear un sprint sin priorizar el backlog.
2. El sistema detecta que el orden de priorización no está definido.
3. El sistema responde con bloqueo visual: "El Product Backlog debe estar priorizado antes del Sprint Planning. Contacta al Product Owner."
4. El flujo se detiene hasta que el PO realice la priorización.

### Flujo principal — Registro de Daily Scrum (Scrum Master)
1. El Scrum Master accede al sprint activo → selecciona "Daily Scrum".
2. El sistema muestra lista de asistencia automática (miembros del equipo del sprint).
3. El Scrum Master registra novedades, impedimentos reportados y acuerdos.
4. El Scrum Master guarda el registro.
5. El sistema vincula las notas al sprint y genera alertas si hay impedimentos nuevos.

---

## Sección 5 — Arquitectura

### Stack Tecnológico

| Componente | Tecnología | Función |
|---|---|---|
| **Frontend** | React 18 + TypeScript 5.3 + Vite + Tailwind CSS | Interfaz de usuario, tablero Kanban, dashboards, formularios |
| **State Management** | Zustand + TanStack Query v5 | Estado global y sincronización de datos del servidor |
| **Backend** | Python 3.12 + FastAPI 0.110 | API RESTful, validación Pydantic v2, inyección de dependencias |
| **ORM / DB Access** | SQLAlchemy 2.0 (async) + Alembic | Modelado declarativo, migraciones, queries optimizadas |
| **Base de datos** | PostgreSQL 16 + PgBouncer | Datos relacionales, JSONB, índices parciales, connection pooling |
| **Cache / Broker** | Redis | Caché de sesiones, pub/sub para notificaciones, Celery broker |
| **Background Tasks** | Celery + Redis | Cálculo de métricas, refresh de materialized views, notificaciones |
| **Auth** | python-jose + passlib + OAuth2PasswordBearer | JWT (access + refresh), RBAC, hashing seguro |
| **API Docs** | FastAPI native (OpenAPI 3.1) + Redoc | Documentación interactiva auto-generada |
| **Reverse Proxy** | Nginx | SSL termination, rate limiting, compresión, servicio de estáticos |
| **Monitoreo** | Prometheus + Grafana + Loki | Métricas de aplicación, logs estructurados, alertas |
| **Deploy** | Docker + Docker Compose + GitHub Actions | Contenedores, CI/CD automatizado, despliegue a staging |

### Flujo de datos

```
Usuario → React (Vite) → Nginx → FastAPI (Uvicorn/Gunicorn)
                                    ↓
                              SQLAlchemy (async)
                                    ↓
                              PostgreSQL 16  ←→  PgBouncer
                                    ↓
                              Redis (Cache + Pub/Sub)
                                    ↓
                              Celery Workers (Background)
```

### Arquitectura de capas (Clean Architecture + DDD)

```
┌─────────────────────────────────────────────────────────────┐
│  Presentation Layer (React + TanStack Query + Zustand)     │
├─────────────────────────────────────────────────────────────┤
│  API Layer (FastAPI Routers + Dependency Injection)        │
├─────────────────────────────────────────────────────────────┤
│  Application Layer (Use Cases / Services)                  │
│  - SprintPlanningService                                   │
│  - WIPValidationService                                    │
│  - MetricsCalculationService                               │
│  - KanbanTransitionService                                 │
├─────────────────────────────────────────────────────────────┤
│  Domain Layer (Entities, Value Objects, Aggregates)        │
│  - User, Project, Sprint, Task, HistoriaUsuario            │
│  - EstadoTarea, EstadoSprint, Prioridad, Rol               │
│  - Domain Events: TaskTransitioned, WIPViolated            │
├─────────────────────────────────────────────────────────────┤
│  Infrastructure Layer (Repositories, DB, Cache, Email)     │
│  - SQLAlchemyRepository, RedisCache, CeleryTaskQueue       │
└─────────────────────────────────────────────────────────────┘
```

### Bounded Contexts (DDD)

1. **Identity & Access Management**: Usuarios, roles, autenticación, autorización.
2. **Project Management**: Proyectos, módulos, equipos, asignaciones.
3. **Backlog Management**: Épicas, historias de usuario, priorización.
4. **Sprint Management**: Sprints, eventos ágiles, planificación.
5. **Kanban Flow Management**: Tablero, transiciones de estado, validación WIP, métricas.
6. **Communication**: Mensajería asíncrona por proyecto y tarea.
7. **Artifact Management**: Documentos, versionado, almacenamiento.

### Estrategia de persistencia

- **Aggregates principales**: `Project`, `Sprint`, `Task`, `User`, `HistoriaUsuario`.
- **Cada aggregate tiene su propio repositorio** con interfaz en dominio e implementación en infraestructura.
- **Event sourcing ligero** para transiciones de estado de tareas (tabla `task_state_transitions`).
- **Soft delete** en todas las entidades con `deleted_at` + índices parciales.
- **Audit trail** vía triggers en PostgreSQL para campos `created_at`, `updated_at`, `created_by`, `updated_by`.

---

## Sección 6 — Requisitos No Funcionales

### Rendimiento
- El cambio de estado de una tarea (drag & drop) debe reflejarse visualmente en < 100ms (optimistic UI).
- La validación WIP en backend debe responder en < 50ms.
- El Dashboard del proyecto debe cargarse completamente en < 2s con conexión estándar.
- Las métricas agregadas (lead time, cycle time) deben servirse desde materialized views con latencia < 3s.
- La lista de backlog con > 500 historias debe paginarse con cursor-based (50 items/página) en < 200ms.

### Seguridad
- Autenticación con JWT: access token de 15 min, refresh token de 7 días en httpOnly cookie.
- RBAC estricto: control de acceso a rutas y recursos según rol global y rol de proyecto.
- Rate limiting: 100 req/min por usuario en endpoints generales, 20 req/min en autenticación.
- Hashing de contraseñas con Argon2id (configuración OWASP recomendada).
- Sanitización de inputs para prevenir XSS e inyección SQL (SQLAlchemy ORM + Pydantic validación).
- Registro de logs de auditoría para cambios críticos: transiciones de estado, eliminación de artefactos, cambios de rol.
- Secrets management: variables de entorno en `.env` nunca commiteadas; uso de Docker secrets en producción.

### Fiabilidad y Consistencia
- Validación WIP estricta **desde el backend**; el frontend solo es capa de presentación.
- Transacciones atómicas para operaciones complejas (crear sprint + derivar tareas + asignar a tablero).
- Manejo de excepciones centralizado con formato Problem+JSON (RFC 7807).
- Retry automático con backoff exponencial en operaciones de Celery.
- Health checks en `/health`, `/ready` y `/metrics` para orquestación de contenedores.

### Compatibilidad y Accesibilidad
- Compatible con Chrome, Firefox, Edge y Safari en últimas 2 versiones.
- Responsive Design: escritorio (primario) y tablet (secundario). No móvil nativo en v1.
- Cumplimiento WCAG 2.1 nivel AA: contraste de colores, navegación por teclado, etiquetas ARIA en tablero Kanban.
- Internacionalización: español (primario) e inglés (secundario).

### Escalabilidad
- Arquitectura stateless: cualquier instancia de FastAPI puede atender cualquier request.
- Horizontal scaling: múltiples workers Uvicorn detrás de Nginx load balancer.
- PostgreSQL: read replicas para consultas de reportes y dashboards (CQRS).
- Redis: cache de sesiones y resultados de métricas frecuentes (TTL 5 min).
- Celery: workers independientes para procesamiento asíncrono de métricas y notificaciones.

### Mantenibilidad
- Cobertura de tests: mínimo 85% backend, 75% frontend.
- Documentación de API auto-generada y siempre actualizada (OpenAPI 3.1).
- ADRs para decisiones arquitectónicas críticas (elección de FastAPI, estrategia WIP, particionamiento).
- C4 Model para documentación visual de arquitectura.
- Conventional Commits + semantic versioning para releases.
- Monorepo estructurado: `/backend`, `/frontend`, `/docs`, `/infra`, `/scripts`.

---

## Checklist final

- [x] **Visión** — Define el producto, el problema y la solución en 2 oraciones claras.
- [x] **Usuarios** — 4 actores descritos con acciones concretas y permisos diferenciados.
- [x] **Funcionalidades** — 10 áreas funcionales + estados + fuera de alcance definidos.
- [x] **Flujos** — 4 flujos documentados (felices + errores) con pasos numerados.
- [x] **Arquitectura** — Stack elegido, flujo de datos, capas Clean Architecture, bounded contexts DDD.
- [x] **Requisitos** — Rendimiento, seguridad, fiabilidad, accesibilidad, escalabilidad, mantenibilidad con métricas concretas.
- [x] **Invariants** — Reglas de dominio que nunca deben violarse documentadas en `config.yaml`.
- [x] **Optimización BD** — Índices, particionamiento, materialized views, connection pooling, soft-delete, audit trail.

---

*Documento generado siguiendo la metodología Spec-First adaptada al contexto académico de la Universidad Nacional de Loja.*
