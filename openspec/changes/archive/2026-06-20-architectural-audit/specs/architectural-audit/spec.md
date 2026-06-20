# Spec: Architectural Audit

## Description
Revisión completa, corrección y normalización de toda la documentación del proyecto GESTKRUN para garantizar consistencia, completitud y alineación con Clean Architecture + DDD.

## Requirements

### RA-01: Separación de documentación
- `docs/architecture.md` debe dividirse en 3 archivos independientes:
  - `/product.md`: visión, usuarios, funcionalidades, flujos, fuera de alcance
  - `/config.yaml`: invariants del dominio + SLOs de rendimiento
  - `/docs/architecture.md`: stack, capas, bounded contexts, persistencia, NFRs
- Cada archivo debe mantener referencias cruzadas explícitas (xref) a los otros

### RA-02: Auditoría de inconsistencias
- Identificar y resolver las 10 inconsistencias listadas en design.md (I1-I10)
- Cada inconsistencia resuelta debe documentarse con justificación

### RA-03: Corrección del modelo de dominio
- Rol debe ser enumeration, no clase
- Epica debe existir como entidad independiente
- TaskStateTransition debe existir como entidad
- WIP validation debe estar en KanbanFlowService, no en Usuario
- Mensaje debe tener solo tipos PROYECTO y TAREA

### RA-04: Elementos faltantes
- Crear todos los elementos listados en design.md (F1-F24)
- Cada elemento debe justificarse con referencia al source of truth

## Invariants
- Ninguna modificación a documentos debe contradecir el source of truth existente
- Toda adición debe referenciar el requerimiento del product.md que la origina