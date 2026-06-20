# Diagrama de Estado — Ciclo de Vida de Tarea

```mermaid
stateDiagram-v2
    [*] --> PENDIENTE
    PENDIENTE --> EN_PROCESO : Iniciar
    EN_PROCESO --> BLOQUEADO : Bloquear
    EN_PROCESO --> EN_REVISION : Completar
    BLOQUEADO --> EN_PROCESO : Desbloquear
    EN_REVISION --> EN_PROCESO : Rechazar
    EN_REVISION --> TERMINADO : Aprobar
    PENDIENTE --> CANCELADO : Cancelar
    EN_PROCESO --> CANCELADO : Cancelar
    BLOQUEADO --> CANCELADO : Cancelar
    EN_REVISION --> CANCELADO : Cancelar
    TERMINADO --> [*]
    CANCELADO --> [*]
```

### Transiciones válidas

| Desde | Hacia | Condición | Actor |
|-------|-------|-----------|-------|
| PENDIENTE | EN_PROCESO | WIP < 3 | Developer |
| PENDIENTE | CANCELADO | — | SM/PO |
| EN_PROCESO | BLOQUEADO | — | Developer/SM |
| EN_PROCESO | EN_REVISION | — | Developer |
| EN_PROCESO | CANCELADO | — | SM/PO |
| BLOQUEADO | EN_PROCESO | WIP < 3 | Developer/SM |
| BLOQUEADO | CANCELADO | — | SM/PO |
| EN_REVISION | EN_PROCESO | WIP < 3 | Developer |
| EN_REVISION | TERMINADO | — | PO/SM |
| EN_REVISION | CANCELADO | — | SM/PO |


```