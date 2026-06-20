# Spec: C4 Model

## Description
Diagramas C4 de Context, Container y Component para GESTKRUN.

## Requirements

### RC4-01: Context Diagram (Nivel 1)
- Personas: Administrador, Product Owner, Scrum Master, Developer
- Sistema: GESTKRUN (caja negra)
- Sistemas externos: PostgreSQL, Redis, Email SMTP, Navegador Web
- Relaciones: cada persona con el sistema y sistemas externos

### RC4-02: Container Diagram (Nivel 2)
- Contenedores: React SPA, FastAPI REST API, PostgreSQL DB, Redis Cache/Broker, Celery Workers, Nginx Reverse Proxy
- Relaciones entre contenedores con protocolo/tecnología
- Tecnología de cada contenedor

### RC4-03: Component Diagram (Nivel 3) — Backend
- Componentes dentro de FastAPI:
  - API Layer: Routers v1, Middleware, Dependencies
  - Application Layer: Use Cases, DTOs
  - Domain Layer: Entities, VOs, Services, Repository Interfaces, Events
  - Infrastructure Layer: SQLAlchemy Repositories, JWT Provider, Redis Cache, Celery Queue, File Storage
- Interfaces entre componentes

## Invariants
- Debe reflejar fielmente el stack tecnológico de architecture.md
- Los bounded contexts deben mapearse a módulos/paquetes dentro del diagrama de componentes