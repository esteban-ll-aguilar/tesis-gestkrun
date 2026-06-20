# ADR 0006: Estrategia de Validación WIP

**Fecha:** 2026-06-20\
**Estado:** Aceptado

## Contexto
La invariante más crítica de GESTKRUN es el límite WIP: un Developer no puede tener más de 3 tareas en estado EN_PROCESO. La validación debe ser consistente, rápida y con buena experiencia de usuario.

## Decisión
Se implementa validación en **tres capas**:
1. **Frontend (optimistic + preventivo):** al iniciar drag, se consulta el conteo actual de tareas EN_PROCESO del usuario. Si ya tiene 3, se deshabilita el drop en la columna "En Proceso".
2. **Backend (domain service):** `WIPValidationService` cuenta las tareas del usuario en EN_PROCESO. Si >= 3, rechaza con 422.
3. **Base de datos (constraint blanda):** índice parcial único no aplica (el límite es por usuario, no global). La BD registra el intento en audit log.

El flujo completo:
- Frontend: optimistic update inmediato.
- Backend: validación síncrona (target < 50ms).
- Si falla: frontend hace rollback del optimistic update, muestra toast de error.
- Audit log del intento de violación para métricas.

## Consecuencias
- La validación es **consistente desde el backend**; el frontend solo mejora UX.
- El conteo de tareas EN_PROCESO debe ser una query rápida (índice en `task.assigned_to + task.estado`).
- Posible race condition: dos requests simultáneas. Se mitiga con bloqueo optimista o SERIALIZABLE isolation.

## Alternativas Consideradas
- **CHECK constraint en BD:** no soporta subqueries ni lógica cross-table.
- **Bloqueo pesimista en BD:** sobreingeniería para v1; latencia adicional.
